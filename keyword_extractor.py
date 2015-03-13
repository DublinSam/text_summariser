"""keyword_extractor defines a series of functions that enable the most important 
words in a document to be identified.  Example usage is provided at the bottom, which
prints out the keywords of all text files in the current directory.
author: Sam Albanie
"""

import nltk
import os 
from nltk.corpus import stopwords
import scipy as sp
import numpy as np
import scipy.spatial as spatial
from graph_utils import Graph

def get_tokens(filename):
	"""returns a dictionary of the raw and filtered string tokens retrieved
	from the given filename."""
	with open(filename, "r") as f:
		input_text = f.read()
	tokens = {}
	tokens['raw'] = nltk.word_tokenize(input_text)
	tokens['filtered'] = filter_tokens(tokens['raw'])
	return tokens

def filter_tokens(tokens):
	"""takes as input a list of string tokens and removes stop
	words and common punctuation before returning the cleaned list."""
	tokens = list(set(tokens))
	punctuation = [",", ".", "'s", "``", "''", "$", "said"]
	stop_words = stopwords.words('english')
	tokens = [token for token in tokens if token.lower() not in stop_words]
	tokens = [token for token in tokens if token not in punctuation]
	return tokens

def get_indices(target, my_list):
	"""returns all indices of a target element in a list as a
	column vector."""
	all_indices = [i for i, x in enumerate(my_list) if x == target]
	return np.atleast_2d(all_indices).T

def window_check(t1, t2, my_list, N):
    """returns 1 if the two tokens t1 and t2 are within
    N tokens of each other in my_list, 0 otherwise."""
    t1_indices = get_indices(t1, my_list)
    t2_indices = get_indices(t2, my_list)
    distances = spatial.distance.cdist(t1_indices, t2_indices, 'cityblock')
    if (np.amin(distances) < N):
        return 1
    return 0

def find_keywords(filename, num_keywords, window_length=5, initial_score=1):
	tokens = get_tokens(filename)
	graph =  Graph(tokens['filtered'], tokens['raw'], window_check, window_length, initial_score)
	graph.run_text_rank()
	scores = {}
	for node in graph.text_graph:
		scores[node] = graph.text_graph[node]["score"]
	keywords = sorted(scores, key=scores.get, reverse=True)[:num_keywords]
	return keywords
	
for filename in os.listdir('./sample_text'):
     if filename.endswith(".txt"):
     	filename = './sample_text/' + filename
     	keywords = find_keywords(filename, 10)
     	print(keywords)
