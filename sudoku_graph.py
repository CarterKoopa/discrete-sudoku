"""
Sudoku graph class

# TODO: WORK IN PROGRESS - Audrey
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx


class SudokuGraph:
    """
    Creates a class for Suduko graph
    """

    def __init__(self, puzzle, size: int = 3):
        self.puzzle = puzzle
        self.graph = nx.sudoku_graph(size)
        # Maps each node in graph to its corresponding value
        self.mapping = dict(zip(self.graph.nodes(), self.puzzle.flatten()))
        self.pos = dict(
            zip(list(self.graph.nodes()), nx.grid_2d_graph(size * size, size * size))
        )
        self.low = min(self.mapping.values())
        self.high = max(self.mapping.values())
        self.norm = mpl.colors.Normalize(vmin=self.low, vmax=self.high, clip=True)
        self.mapper = mpl.cm.ScalarMappable(norm=self.norm, cmap=mpl.cm.Pastel1)

    def get_degrees_of_saturation(self):
        """
        Get the degrees of saturation
        """
        # Get all of the uncolored vertices
        uncolored_vertices = [
            vertex for vertex in self.mapping if self.mapping[vertex] == 0
        ]
        # The amount of uncolored vertices in a vertex's neighborhood
        uncolored_vertices_degree_of_saturation = []
        # The amount of colored vertices in a vertex's neighborhood

        # For each vertex that is uncolored
        for vertex in uncolored_vertices:
            # Get the neighbors of the vertex
            neighborhood_indices = sorted(self.graph.neighbors(vertex))
            # Get the values of each vertex in the neighborhood
            values_of_neighborhood = [self.mapping[key] for key in neighborhood_indices]
            # Get the amount of uncolored vertices in its neighborhood
            uncolored_neighbors = 20 - values_of_neighborhood.count(0)
            # Add that to a list
            uncolored_vertices_degree_of_saturation.append(uncolored_neighbors)
            # There are 20 neighbors per vertex

        dictionary = dict(
            zip(uncolored_vertices, uncolored_vertices_degree_of_saturation)
        )

        return dictionary
