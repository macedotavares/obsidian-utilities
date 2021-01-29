#!/usr/bin/python3
#-*- coding: utf-8 -*-

import os, sys, re, string
import random
import similarity_lite

stop_words = ["the", "a"]
tokenizer_func = lambda x: x.strip().split()

rootdir = os.path.expanduser(os.environ['vault_path'])
target = os.environ['file']

debugging=False

md_regex = re.compile(r'.*md$')
tag_regex = re.compile(r'#([-_\d\w]+)')
link_regex = re.compile(r'\[\[(.*?)[|#]')

def debug(description,var):
	if debugging:
		sys.stdout.write(description+': '+str(var)+'\n')

def read(file):
    with open(file, 'r') as f:
        content = f.read()
        f.close()
    return content.lower()

similarity_obj = similarity_lite.SimilarityLite(
	db_path='/tmp/simlite.db',
	stop_words=stop_words,
	tokenizer_func=tokenizer_func,
	idf_cutoff=.2,
	delete_existing_table=True
)

docs = []
docs_by_id = {}

#for i, text in enumerate(sentences):
#	doc = {"id": str(i), "doc_text": text}
#	docs.append(doc)
#	docs_by_id[str(i)] = doc

index = 0
for root, dirs, files in os.walk(rootdir):
	for other_file in files:
		if other_file != target:
			if md_regex.match(other_file):
				other_file_path = os.path.join(root, other_file)
				doc = {"id": str(index), "doc_text": read(other_file_path)}
				docs.append(doc)
				docs_by_id[str(index)] = other_file[:-3]
				index += 1

similarity_obj.add_or_update_docs(docs, update_stats=True)

search_query = read(target)
similar_docs = similarity_obj.get_similar_docs(search_query)

results = ""

for doc_id, similarity in similar_docs[1:11]:
	results += "[[" + docs_by_id[doc_id] + "]]\n"

	
sys.stdout.write(results)
