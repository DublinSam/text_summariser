"""graph_utils defines the Graph class which offers methods for 
building and querying graphs.
author: Sam Albanie
"""

class Graph:

	def __init__(self, filtered_tokens, tokens, window_check, window_length, initial_score):
		"""Constructs a graph using the tokens as nodes and the window check 
		to define weighted edges between each node."""
		self.text_graph = {}
		for node in filtered_tokens:
			other_nodes = [other_node for other_node in filtered_tokens if other_node != node]
			for other_node in other_nodes:
				if window_check(node, other_node, tokens, window_length):
					try:
						self.text_graph[node]['edges'][other_node] = 1
					except KeyError:
						self.text_graph[node] = {'score': initial_score, 'edges': {other_node: 1} }


	def find_in_nodes(self, target_node):
		"""for the given target_node, returns its predecessors in the graph."""
		in_nodes = []
		for node, node_props in self.text_graph.items():
			if target_node in node_props['edges']:
				in_nodes.append(node)
		return in_nodes

	def find_out_nodes(self, target_node):
		"""for the given target_node, returns its sucessors in the graph."""
		out_nodes = self.text_graph[target_node]['edges'].keys()
		return list(out_nodes)

	def get_edge_weight(self, from_node, to_node):
		return self.text_graph[from_node]['edges'][to_node]

	def update_score(self, damping, current_node):
		"""takes as input a damping factor (between 0 and 1) and a node for which the 
		score is to be updated.  It applies the TextRank algorithm to update the 
		score at the current_node.""" 
		old_score = self.text_graph[current_node]["score"]
		in_nodes = self.find_in_nodes(current_node)
		score = 1 - damping
		for in_node in in_nodes:
			edge_weight = self.get_edge_weight(in_node, current_node)
			out_nodes = self.find_out_nodes(in_node)
			denominator = 0
			for out_node in out_nodes:
				denominator = denominator + self.get_edge_weight(in_node, out_node)
			numerator = self.get_edge_weight(in_node, current_node) * self.text_graph[in_node]["score"]
			fraction = numerator / denominator
			score = score + damping * fraction
		self.text_graph[current_node]["score"] = score
		score_diff = abs(score - old_score)
		return score_diff

	def run_text_rank(self, largest_update=1, damping=0.85, ):
		"""runs the text rank algorithm, updating the score at each node of the graph
		until convergence is achieved to an acceptable tolerance level."""
		while largest_update > 0.001:
		    update_diffs = []
		    for node in list(self.text_graph.keys()):
		        update_diff = self.update_score(damping, node)
		        update_diffs.append(update_diff)
		    largest_update = max(update_diffs)