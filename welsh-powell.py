"""
This file implements a Sudoku solving algorithm based upon the Welsh-Powell
algorithm. In this scenario, Sudoku puzzles are represented as
graphs, where each square in the 9x9 grid is represented by a vertex and each
relationship (within a column, row, and subgrid) is represented by a 
connection.

The Welsh-Powell algorithm is a Greedy-like graph coloring algorithm. Where it
differs is that instead of iterating by vertex, this algorithm iterates by
color. Starting with the vertex of the highest degree (another major difference
compared to the Greedy algorithm, which just uses the first vertex), the first
vertex is colored with the first color, and all remaining vertices that can be
colored with that color are. This cycle continues with as many colors as needed
to color the graph.

In this situation, the number of colors will be limited to nine, as in a real
Sudoku puzzle. Further, in a Sudoku puzzle, all vertices have the same degree.
As such, logic to pick the vertex with the highest degree is not included or
necessary.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import time
import random

# Import test puzzles
import sudoku_puzzles

# Import graphing function
from greedy import graph_sudoku


def welsh_powell(graph, vertex_mapping):
    """
    Implement the Welsh-Powell coloring algorithm for a Sudoku graph.

    The two inputs of this function represent a generic Sudoku graph (the
    networkx object), and a mapping of the numbers (or rather, colors) in
    each spot on a specific Sudoku graph (ie, the dictionary)

    Args:
        graph: A networkx graph object which represented a Sudoku
        graph (ie, the connectivity)
        vertex_mapping: a dictionary where the keys represent a specific
        box/vertex in the Sudoku graph (0-80) and the value represents the
        number/color at that location.
    """

    # Iterate through each of the 9 available colors.
    #
    # Note: use 1-based indexing, as the zero index is used to represent an
    # uncolored vertex.
    for color in range(1, 10):
        # Begin iterating through all vertices
        for vertex, current_color in vertex_mapping.items():
            # If the vertex is already colored, continue
            if current_color != 0:
                continue

            # Get all neighbors to the current vertex
            neighbors = list(graph.neighbors(vertex))

            # Make a list of all connected colors
            connected_colors = []
            for neighbor in neighbors:
                neighbor_color = vertex_mapping[neighbor]
                # If the vertex is colored and is unique, add it to the list of
                # connected colors to track all utilized colors
                if neighbor_color != 0 and neighbor_color not in connected_colors:
                    connected_colors.append(neighbor_color)

            # Color all vertices that can be colored with the current color
            if color not in connected_colors:
                vertex_mapping[vertex] = color

    return vertex_mapping


def main():
    """
    Runs the Welsh-Powell coloring algorithm for an example puzzle.
    """
    N = 3  # Make the sudoku grid 3x3 (standard 9x9)
    G = nx.sudoku_graph(N)  # Creates a graph representation of Sudoku

    mapping = dict(zip(G.nodes(), sudoku_puzzles.puzzle_easy.flatten()))

    test_mapping = welsh_powell(G, mapping)
    graph_sudoku(G, test_mapping)


# Runs the main loop
if __name__ == "__main__":
    main()
