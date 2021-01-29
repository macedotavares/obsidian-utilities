import logging
import math
import os
import sqlite3
import sys


class SimilarityLite():

    def __init__(
            self, db_path, stop_words, tokenizer_func, idf_cutoff, 
            delete_existing_table=False):

        assert isinstance(db_path, str)
        assert isinstance(stop_words, (list, set))
        assert hasattr(tokenizer_func, '__call__')
        assert isinstance(idf_cutoff, float)

        self.stop_words = set(stop_words)
        self.tokenizer = tokenizer_func
        self.idf_cutoff = idf_cutoff

        if delete_existing_table:
            if os.path.exists(db_path):
                logging.info("Deleting existing table because you told me to...")
                os.remove(db_path)

        self.db_conn = sqlite3.connect(db_path)
        self.total_doc_count = None

        raw_docs_creation_query = """
            CREATE TABLE raw_docs (
                id text PRIMARY KEY ON CONFLICT REPLACE, doc_text text
            )
        """

        # INTEGER PRIMARY KEY is an alias for row_id or something.  It will autoincrement
        terms_creation_query = """
            CREATE TABLE terms (id INTEGER PRIMARY KEY, term text)
        """
        terms_index_creation_query = """
            CREATE INDEX idx_terms_term ON terms (term)
        """

        postings_creation_query = """
            CREATE TABLE postings (
                term_id integer, doc_id text,
                UNIQUE (term_id, doc_id) ON CONFLICT REPLACE
            )
        """
        postings_index_creation_query = """
            CREATE INDEX idx_postings_doc_id ON postings (doc_id)
        """

        idfs_creation_query = """
            CREATE TABLE idfs (
                term_id integer PRIMARY KEY ON CONFLICT REPLACE,
                doc_freq integer,
                idf real
            )
        """

        try:
            if delete_existing_table:
                self._write_query(raw_docs_creation_query, ())
                self._write_query(terms_creation_query, ())
                self._write_query(terms_index_creation_query, ())
                self._write_query(postings_creation_query, ())
                self._write_query(postings_index_creation_query, ())
                self._write_query(idfs_creation_query, ())
        except sqlite3.OperationalError:
            logging.info("Tables already exists. Proceeding...")
            raise

    def get_terms_from_docs(self, docs):
        terms_in_docs = set()
        for doc in docs:
            tokenized = self._tokenize(doc["doc_text"])
            terms_in_docs.update(tokenized)
        return terms_in_docs

    def _tokenize(self, text):
        pre_filter = self.tokenizer(text)
        post_filter = [x for x in pre_filter if x not in self.stop_words]
        return post_filter

    def get_term_ids_mapping_from_docs(self, docs):
        """
        Returns a dict of format text: id
        """
        mapping = {}
        terms_in_docs = tuple(self.get_terms_from_docs(docs))
        terms_query = """
            SELECT id, term FROM terms WHERE term IN (%s)
        """ % ",".join(['?' for _ in terms_in_docs])
        terms_results = self._get_rows_from_query(terms_query, terms_in_docs)
        for r in terms_results:
            mapping[r[1]] = r[0]
        return mapping

    def add_terms_from_docs(self, docs):
        self.add_terms(self.get_terms_from_docs(docs))

    def add_or_update_docs(self, docs, update_stats=False):
        #if len(docs) > 200:
           # logging.warn("You are probably using too many docs at one time.")
        assert isinstance(docs, list)
        insert_query = """
            INSERT INTO raw_docs (id, doc_text) VALUES (?, ?)
        """
        insert_data = []
        for doc in docs:
            insert_data.append((doc["id"], doc["doc_text"]))
        self._write_query(insert_query, insert_data, many=True)

        # Potentially expensive operations, thus not required to do whenever document is added
        if update_stats:
            self.update_doc_count()
            self.add_terms_from_docs(docs)
            self.update_postings(docs)
            ids_of_new_terms = list(self.get_term_ids_mapping_from_docs(docs).values())
            self.update_idfs(ids_of_new_terms)

    def update_postings(self, docs):
        term_ids_mapping = self.get_term_ids_mapping_from_docs(docs)
        insert_query = "INSERT INTO postings (term_id, doc_id) VALUES (?, ?)"
        insert_data = []
        for doc in docs:
            tokens = self._tokenize(doc["doc_text"])
            for token in tokens:
                term_id = term_ids_mapping[token]
                insert_data.append((term_id, doc["id"]))
        self._write_query(insert_query, insert_data, many=True)

    def update_doc_count(self):
        doc_count_query = """
            SELECT count(1) FROM raw_docs
        """
        results = self._get_rows_from_query(doc_count_query, ())
        count = results[0][0]
        self.total_doc_count = count

    def update_idfs(self, term_ids):
        if len(term_ids) > 0:
            assert isinstance(term_ids[0], int)
        count_query = """
            SELECT count(distinct(doc_id)), term_id 
            FROM postings WHERE term_id IN (%s) GROUP BY term_id
        """ % ','.join(['?' for _ in term_ids])
        results = self._get_rows_from_query(count_query, term_ids)

        insert_query = """
            INSERT INTO idfs (term_id, doc_freq, idf) VALUES (?, ?, ?)
        """
        insert_data = []
        for r in results:
            term_id = r[1]
            doc_freq = r[0]
            idf = math.log(self.total_doc_count * 1.0 / doc_freq)
            insert_data.append((term_id, doc_freq, idf))
        self._write_query(insert_query, insert_data, many=True)

    def update_all_idfs(self):
        update_query = """
            UPDATE idfs SET idf = ? / (doc_freq * 1.0)
        """
        self._write_query(update_query, (self.total_doc_count))

    def add_terms(self, terms):
        terms = set(terms)
        # We have to put the right number of question marks into the IN clause
        terms_query = """
            SELECT id, term FROM terms WHERE term IN (%s)
        """ % ",".join(['?' for _ in terms])
        results = self._get_rows_from_query(terms_query, tuple(terms))
        existing_terms = set([r[1] for r in results])

        insert_query = """
            INSERT INTO terms (term) VALUES (?)
        """
        insert_data = []
        for term in terms:
            if term in existing_terms:
                continue
            else:
                insert_data.append((term,))
        self._write_query(insert_query, insert_data, many=True)

    def _write_query(self, query, data, many=False):
        """wrapper around writes"""
        if many:
            self.db_conn.cursor().executemany(query, data)
        else:
            self.db_conn.cursor().execute(query, data)
        self.db_conn.commit()

    def _get_rows_from_query(self, query, data):
        """Just returns tuples of rows in memory"""
        to_return = []
        results = self.db_conn.cursor().execute(query, data)
        for result in results:
            to_return.append(result)
        return to_return

    def get_similar_docs(self, user_search_query, num_results=11):
        tokenized_query = self.tokenizer(user_search_query)
        question_marks = ",".join("?" for term in tokenized_query)

        weights_of_searched_doc_query = """
            SELECT idfs.term_id, idfs.idf
            FROM idfs JOIN terms
            ON idfs.term_id = terms.id
            JOIN postings
            ON postings.term_id = idfs.term_id
            WHERE terms.term IN (%s)
        """ % question_marks
        weights_results = self._get_rows_from_query(
            weights_of_searched_doc_query,
            tokenized_query
        )
        weights_of_searched = {}
        for term_id, idf in weights_results:
            weights_of_searched[term_id] = idf

        # TODO actually use idf, not freq
        docs_sharing_terms_query = """
            SELECT p.doc_id, p.term_id, idfs.idf, terms.term
            FROM postings p
            JOIN idfs
            ON p.term_id = idfs.term_id
            JOIN terms
            ON terms.id = idfs.term_id
            AND terms.term IN (%s)
            WHERE idf > ?
        """ % question_marks
        shared_term_results = self._get_rows_from_query(
            docs_sharing_terms_query,
            tuple(tokenized_query + [self.idf_cutoff])
        )

        scores_accumulator = {}
        sum_squares = {}
        sum_squares["searched_doc_pseudo_id"] = 0
        for idf in list(weights_of_searched.values()):
            sum_squares["searched_doc_pseudo_id"] += idf ** 2

        for doc_id, term_id, idf, term in shared_term_results:
            if doc_id not in sum_squares:
                sum_squares[doc_id] = 0
            if doc_id not in scores_accumulator:
                scores_accumulator[doc_id] = 0
            sum_squares[doc_id] += idf ** 2
            if term_id in weights_of_searched:
                # TODO use term frequency and not just IDF?
                scores_accumulator[doc_id] += weights_of_searched[term_id] ** 2
        
        for doc_id, score in scores_accumulator.items():
            candidate_norm = sum_squares[doc_id] ** .5
            searched_doc_norm = sum_squares["searched_doc_pseudo_id"] ** .5
            scores_accumulator[doc_id] = score / candidate_norm / searched_doc_norm

        score_list = [(doc_id, score) for doc_id, score in scores_accumulator.items()]
        score_list.sort(key=lambda x: x[1], reverse=True)
        return score_list[:num_results]



