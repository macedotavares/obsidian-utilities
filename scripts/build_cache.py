#!/usr/bin/python3
#-*- coding: utf-8 -*-
 
import os, sys, string
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer 
import gensim
import pickle

ps = PorterStemmer() 

vault_path = os.path.expanduser(os.environ['vault_path'])
cache_path = "./cache.p"
exclude = set(['.git', '.obsidian', '.trash'])

vault_list = []

def preprocess(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    for w in text.split(" "):
        if len(w) > 1:
            text += w
    return text

def read_file(file_path):
    f = open(file_path)
    content = f.read()
    content = preprocess(content)
    f.close()
    return content # String

for root, dirs, files in os.walk(vault_path):
    dirs[:] = [d for d in dirs if d not in exclude] # excluding directories listed above
    for file_name in files:
        if file_name[-3:]==".md":
            content = read_file(os.path.join(root, file_name))
            content = [w.lower() for w in word_tokenize(content)]
            content = [ps.stem(w) for w in content]
            vault_list.append([file_name, content])

vault_content = [note[1] for note in vault_list]
dictionary = gensim.corpora.Dictionary(vault_content)
corpus = [dictionary.doc2bow(doc) for doc in vault_content]
tf_idf = gensim.models.TfidfModel(corpus)

cache = {"vault list":vault_list,"vault content":vault_content, "dictionary": dictionary, "corpus":corpus, "tf-idf":tf_idf}

pickle.dump( cache, open( cache_path, "wb" ) )
#Saving the Python object in a .p (pickle file)

sys.stdout.write("Done.")