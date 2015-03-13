from graph import Graph

class KeywordGraph(Graph):
	"""KeywordGraph extends the Graph baseclass to handle the 
    construction of a graph based on keywords."""

	def __init__(self, filtered_tokens, tokens, window_check, window_length, initial_score):
		"""Constructs a graph using the tokens as nodes and the window check 
		to define weighted edges between each node."""
		self.word_graph = {}
		for node in filtered_tokens:
			other_nodes = [other_node for other_node in filtered_tokens if other_node != node]
			for other_node in other_nodes:
				if window_check(node, other_node, tokens, window_length):
					try:
						self.word_graph[node]['edges'][other_node] = 1
					except KeyError:
						self.word_graph[node] = {'score': initial_score, 'edges': {other_node: 1} }