#!/usr/bin/python3
#-*- coding: utf-8 -*-

import os, sys, string
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer 
import pickle
import gensim
import numpy as np

ps = PorterStemmer() 

######### SETUP #########

file_to_match = os.environ['file']
max_results = int(os.environ['related_max_results'])
ignore_words = os.environ['related_ignore_words'].split(" ")
cache_path = os.path.expanduser("./cache.p")

######### FUNCTIONS #########

def preprocess(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    for w in text.split(" "):
        if w not in ignore_words:
            if len(w) > 1:
                text += w
    return text

def read_file(file_path):
    f = open(file_path)
    content = f.read()
    content = preprocess(content)
    f.close()
    return content # String

######### FLOW #########

cache = pickle.load( open( cache_path, "rb" ) )
vault_list = cache["vault list"]
vault_content = cache["vault content"]
dictionary = cache["dictionary"]
corpus = cache["corpus"]
tf_idf = cache["tf-idf"]

sims = gensim.similarities.Similarity(\
										'./index/',\
										tf_idf[corpus], \
										num_features=len(dictionary))

with open (file_to_match) as f:
    query = [w.lower() for w in word_tokenize(f.read())]
    query = [ps.stem(w) for w in query]

query_bow = dictionary.doc2bow(query)

query_tf_idf = tf_idf[query_bow]

query_sims = sims[query_tf_idf]
query_sims = sorted(enumerate(query_sims), key=lambda item: -item[1])
top_matches= query_sims[1:max_results+1]
top_matches_index = [doc[0] for doc in query_sims[1:max_results+1]]

results = ""
for i in top_matches_index:
	results += "[["+vault_list[i][0][:-3]+"]]"+"\n"

sys.stdout.write(results)