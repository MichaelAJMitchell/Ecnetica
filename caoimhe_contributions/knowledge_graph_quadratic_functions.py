#this is the quadratic functions knowledge graph in its clearest form, this isnt actualy a form thats used anywhere in my code
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass, field 
''' the nodes are a mix of claude and me. the edges and wieghts i determined mself. 
how i thought about determining the weights is based on how related the two topics are: 
if there is very little difference between them then the weight is high, if they are quite different 
(ie one is a lot more advanced than the other) then they would have a low weight. this would make sense for 
backpropagating mastery after a question- the more related they are the more studying one also counts as studying the other.   

the chapter part is obviously not very useful for such a small graph, but it is more a proxy for clustering the nodes into chapters, topics and nodes. 
''' 
nodes = {
    'solving linear equations': {
        'topic': 'solving linear equations',
        'chapter': 'algebra',
        'index': 0,
        'dependencies': [(6,0.5), (14,0.8), (15,0.6)] #(node it goes to, weight)
    },
    'linear equations in standard form': {
        'topic': 'linear equations in standard form',
        'chapter': 'algebra',
        'index': 1,
        'dependencies': [(0,0.3) ,(2,0.4)]
    },
    'form of quadratic equations': {
        'topic': 'form of quadratic equations',
        'chapter': 'algebra',
        'index': 2,
        'dependencies': [(5,0.9), (6,0.7) ,(9,0.6), (10,0.8), (12,0.6), (14,0.7), (15,0.8), (17,0.6)]
    },
    'expanding brackets': {
        'topic': 'expanding brackets',
        'chapter': 'algebra',
        'index': 3,
        'dependencies': [(0,0.7), (9,0.8), (14,0.2)]
    },
    'substitution': {
        'topic': 'substitution',
        'chapter': 'algebra',
        'index': 4,
        'dependencies':  [(5,0.9), (11,0.3), (12,0.3), (13,0.4), (15,0.9),(17,0.8)]
    },
    'using substitution to make equations in quadratic equations': {
        'topic': 'using substitution to make equations in quadratic equations',
        'chapter': 'algebra',
        'index': 5,
        'dependencies': []
    },
    'factorisation by inspection for a=1': {
        'topic': 'factorisation by inspection for a=1',
        'chapter': 'algebra',
        'index': 6,
        'dependencies':[(7,0.9), (9,0.6), (10,0.7), (12,0.7)]
    },
    'factorisation by inspection for a ≠ 1': {
        'topic': 'factorisation by inspection for a ≠ 1',
        'chapter': 'algebra',
        'index': 7,
        'dependencies':  [(9,0.8), (10,0.7), (12,0.7)]
    },
    'basic coordinate geometry': {
        'topic': 'basic coordinate geometry',
        'chapter': 'geometry',
        'index': 8,
        'dependencies': [(10,0.7), (11,0.6), (12,0.6), (13,0.6), (16,0.6)]
    },
    'writing quadratics in completed square form': {
        'topic': 'writing quadratics in completed square form',
        'chapter': 'algebra',
        'index': 9,
        'dependencies': [(13,0.8), (11,0.7),(14,0.7)]
    },
    'form of graph of quadratics': {
        'topic': 'graph of quadratics',
        'chapter': 'algebra',
        'index': 10,
        'dependencies': [(11,0.8), (13,0.8), (16,0.7)]
    },
    'vertex of parabola': {
        'topic': 'vertex of parabola',
        'chapter': 'algebra',
        'index': 11,
        'dependencies':  [(13,0.9)]
    },
    'x-intercept/roots of quadratic equations': {
        'topic': 'x-intercept/roots',
        'chapter': 'algebra',
        'index': 12,
        'dependencies':[(16,0.9), (15,0.6)]
    },
    'interpreting completed square form': {
        'topic': 'interpreting completed square form',
        'chapter': 'algebra',
        'index': 13,
        'dependencies': []
    },
    'quadratic formula derivation': {
        'topic': 'quadratic formula derivation',
        'chapter': 'algebra',
        'index': 14,
        'dependencies': [(15,0.3)]
    },
    'using quadratic formula': {
        'topic': 'using quadratic formula',
        'chapter': 'algebra',
        'index': 15,
        'dependencies':[(17,0.7), (12,0.8)]
    },
    'nature of roots': {
        'topic': 'nature of roots',
        'chapter': 'algebra',
        'index': 16,
        'dependencies': []
    },
    'discriminant': {
        'topic': 'discriminant',
        'chapter': 'algebra',
        'index': 17,
        'dependencies': [(16,0.7)]
    }
}

#============================================================================
#the knowledge graph as i actually use it 

@dataclass
class Node:
    """Knowledge graph node representing a topic/concept"""
    topic: str
    chapter: str
    dependencies: List[Tuple[int, float]]
    _in_degree: Optional[int] = field(default=None, init=False)
    _out_degree: Optional[int] = field(default=None, init=False)

class KnowledgeGraph:
    def __init__(self):
        self.nodes = {}  # {index: Node}
        self.topic_to_index = {}  # Maps topic names to indexes: {topic_name: index}
        self.mcqs = {}
        self.graph = nx.DiGraph()
        self._next_index = 0  # Auto-incrementing index counter
        self._adjacency_matrix = None  # Cache the matrix
        self._matrix_dirty = False     # Track if matrix needs recalculation

        # Initialize nodes with the original data
        self._initialize_nodes()

        # Create NetworkX graph
        self._build_graph()

    def _initialize_nodes(self):
        # nodes with (topic, chapter, dependencies[destination node, weight])
        node_data = [
            ('solving linear equations', 'algebra', [(6,0.5), (14,0.8), (15,0.6)]),
            ('linear equations in standard form', 'algebra', [(0,0.3), (2,0.4)]),
            ('form of quadratic equations', 'algebra', [(5,0.9), (6,0.7), (9,0.6), (10,0.8), (12,0.6), (14,0.7), (15,0.8), (17,0.6)]),
            ('expanding brackets', 'algebra', [(0,0.7), (9,0.8), (14,0.2)]),
            ('substitution', 'algebra', [(5,0.9), (11,0.3), (12,0.3), (13,0.4), (15,0.9), (17,0.8)]),
            ('using substitution to make equations in quadratic equations', 'algebra', [(9,0.5), (11,0.6), (12,0.7), (13,0.5)]),
            ('factorisation by inspection for a=1', 'algebra', [(7,0.8), (12,0.9)]),
            ('factorisation by inspection for a ne 1', 'algebra', [(12,0.9)]),
            ('basic coordinate geometry', 'geometry', [(10,0.8), (11,0.6), (13,0.7)]),
            ('writing quadratics in completed square form', 'algebra', [(11,0.9), (13,0.8)]),
            ('form of graph of quadratics', 'algebra', [(11,0.7), (12,0.5), (13,0.6)]),
            ('vertex of parabola', 'algebra', []),
            ('x-intercept/roots of quadratic equations', 'algebra', [(15,0.4), (16,0.6), (17,0.5)]),
            ('interpreting completed square form', 'algebra', []),
            ('quadratic formula derivation', 'algebra', [(15,0.9)]),
            ('using quadratic formula', 'algebra', [(16,0.8), (17,0.7)]),
            ('nature of roots', 'algebra', []),
            ('discriminant', 'algebra', [(16,0.7)])
        ]

        for topic, chapter, dependencies in node_data:
            self._add_node_internal(topic, chapter, dependencies)

    def _build_graph(self):
        # Add nodes with their attributes
        for index, node in self.nodes.items():
            self.graph.add_node(index,
                              topic=node.topic,
                              chapter=node.chapter)

        # Add weighted edges based on dependencies
        for index, node in self.nodes.items():
            for dest, weight in node.dependencies:
                self.graph.add_edge(index, dest, weight=weight)

    def _add_node_internal(self, topic: str, chapter: str, dependencies: List[Tuple[int, float]]):
        """Internal method to add a node with automatic index assignment"""
        index = self._next_index
        self._next_index += 1

        node = Node(topic, chapter, dependencies)
        self.nodes[index] = node
        self.topic_to_index[topic] = index
        self._matrix_dirty = True  # Invalidate cache
        return index
    
    def get_adjacency_matrix(self) -> np.ndarray:
        """Cache adjacency matrix until graph changes"""
        if self._adjacency_matrix is None or self._matrix_dirty:
            self._adjacency_matrix = self._calculate_adjacency_matrix()
            self._matrix_dirty = False
        return self._adjacency_matrix

    def _calculate_adjacency_matrix(self) -> np.ndarray:
        """Private method to actually calculate the matrix"""
        if not self.nodes:
            return np.array([])

        max_index = max(self.nodes.keys())
        n = max_index + 1
        matrix = np.zeros((n, n), dtype=float)

        for source_index, node in self.nodes.items():
            for dest_index, weight in node.dependencies:
                if dest_index < n:
                    matrix[source_index, dest_index] = weight
        return matrix


    def visualize_graph(self, figsize=(12, 8), node_size=1000, font_size=8):
        """Visualize the knowledge graph"""
        fig, ax = plt.subplots(figsize=figsize)

        # Use hierarchical layout
        pos = nx.spring_layout(self.graph, k=2, iterations=50)

        # Draw nodes
        nx.draw_networkx_nodes(self.graph, pos,
                              node_color='lightblue',
                              node_size=node_size,
                              ax=ax)

        # Draw edges with weights
        edges = self.graph.edges()
        weights = [self.graph[u][v]['weight'] for u, v in edges]

        nx.draw_networkx_edges(self.graph, pos,
                              edge_color='gray',
                              width=[w*3 for w in weights],
                              alpha=0.6,
                              arrows=True,
                              arrowsize=20,
                              ax=ax)

        # Draw labels
        labels = {node: f"{node}\n{self.graph.nodes[node]['topic'][:15]}..."
                 for node in self.graph.nodes()}
        nx.draw_networkx_labels(self.graph, pos, labels, font_size=font_size, ax=ax)

        plt.title("Knowledge Graph Visualization")
        plt.axis('off')
        plt.tight_layout()
        plt.show()
