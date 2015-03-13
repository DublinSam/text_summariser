"""sentence_extractor defines a series of functions that enable the most important 
sentences in a document to be identified.  Example usage is provided at the bottom, 
which prints out the key sentences of all text files in the current directory.
author: Sam Albanie
"""

import nltk
import nltk.data
import os 
import math
from nltk.corpus import stopwords
import scipy as sp
import numpy as np
import scipy.spatial as spatial
from filter_utils import filter_tokens
from sentence_graph import SentenceGraph

def get_sentences(filename):
	"""retrieves the sentences contained in the textfile specified by
	the filename argument."""
	with open(filename, "r") as f:
		text = f.read()
	sentence_detector = nltk.data.load('tokenizers/punkt/english.pickle')
	sentences = sentence_detector.tokenize(text.strip())
	return sentences

def get_tokens(sentence):
    tokens = nltk.word_tokenize(sentence)
    tokens = filter_tokens(tokens)
    return tokens

def get_similarity(sentence1, sentence2):
	"""Returns the lexical similarity between the input sentences."""
	tokens1, tokens2 = get_tokens(sentence1), get_tokens(sentence2)
	numerator = len(set(tokens1) & set(tokens2))
	# To prevent issues with dividng by zero, we adjust the normalization.
	denominator = math.log(len(set(tokens1)) + 1) + math.log(len(set(tokens1)) + 1)
	if denominator == 0:
		denominator = 1
	similarity = numerator / denominator
	return similarity

def find_key_sentences(filename, num_sentences):
    sentences = get_sentences(filename)
    graph =  SentenceGraph(sentences, get_similarity)
    graph.run_text_rank()
    scores = {}
    for node in graph.word_graph:
        scores[node] = graph.word_graph[node]["score"]
    key_sentences = sorted(scores, key=scores.get, reverse=True)[:num_sentences]
    return key_sentences
	
for filename in os.listdir('./sample_text'):
     if filename.endswith(".txt"):
     	filename = './sample_text/' + filename
     	keywords = find_key_sentences(filename, 10)
     	print(keywords)
