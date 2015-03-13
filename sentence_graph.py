from graph import Graph

class SentenceGraph(Graph):
    """SentenceGraph extends the Graph baseclass to handle the 
    construction of a graph based on sentences."""

    def __init__(self, sentences, get_similarity):
        """Constructs a graph using the sentences as nodes and get_similarity 
        to define weighted edges between each node."""
        self.word_graph = {}
        for node in sentences:
            other_nodes = [other_node for other_node in sentences if other_node != node]
            for other_node in other_nodes:
                similarity = get_similarity(node, other_node)
                if similarity > 0:
                    try:
                        self.word_graph[node]['edges'][other_node] = similarity
                    except KeyError:
                        self.word_graph[node] = {'score': 1, 'edges': {other_node: similarity} }