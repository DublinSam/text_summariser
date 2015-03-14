import nltk
from nltk.corpus import stopwords

def filter_tokens(tokens):
	"""takes as input a list of string tokens and removes stop
	words and common punctuation before returning the cleaned list."""
	tokens = list(set(tokens))
	punctuation = [",", ".", "'s", "``", "''", "$"]
	stop_words = stopwords.words('english')
	tokens = [token for token in tokens if token.lower() not in stop_words]
	tokens = [token for token in tokens if token not in punctuation]
	tokens = nounify(tokens)
	return tokens

def nounify(tokens):
	"""takes as input a list of tokens and returns only those that are 
	nouns."""
	nouns = []
	tagged_tokens = nltk.pos_tag(tokens)
	for pair in tagged_tokens:
		if pair[1] == 'NN' or pair[1] == 'NNP':
			nouns.append(pair[0])
	return nouns