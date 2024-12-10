"""
This file implements a Sudoku solving algorithm based upon the Greedy
graph coloring algorithm. In this scenario, Sudoku puzzles are represented as
graphs, where each square in the 9x9 grid is represented by a vertex and each
relationship (within a column, row, and subgrid) is represented by a 
connection.

The Greedy algorithm is one of the simplest graph coloring algorithms. It works
by progressing iteratively through every vertex in the graph in order. At each
vertex, it attempts to color the vertex with the lowest-possible number color
(where each new color is assigned an incrementing numerical identifier). If
it isn't possible to color the algorithm with the current number of colors,
a new color is added, and the process continues for the repeating vertices.

Given that new colors are assigned as needed, the Greedy algorithm doesn't
guarantee that the graph is colored with the minimum number of colors. This
problem is much more complex (NP-complete), and rather, the Greedy algorithm
simply guarantees that a graph can be colored in no more than d+1 colors, where
d is the maximum degree of a vertex (20 in the case of a sudoku graph). 21 is
obviously many more colors than allowed on a Sudoku graph. Instead, the
ordering of the vertices can be randomized to, in a way, "brute force" the
Greedy algorithm into continuing to create new graph colors until one is
created with only 9 colors. 
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import time
import random
import copy

# Import test puzzles
import sudoku_puzzles


def greedy(graph, vertex_mapping):
    """
    Implement the Greedy coloring algorithm for a Sudoku graph.

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
    # This function will continue to run as many times as needed to brute force
    # a solution the works. As such, create variables and a timer to track how
    # long the entire process takes.
    attempts = 0
    start_time = time.time()
    original_vertex_mapping = copy.deepcopy(vertex_mapping)

    while True:
        # Track if the loop should break. Assume yes, until an invalid case is
        # found
        solved = True
        # Track the number of iterations within a given attempt. This counting
        # is nessesary since the order of vertices may be randomized.
        current_attempts = 0

        # Iterate through every vertex in the graph.
        for vertex, color in vertex_mapping.items():
            # Increase number of current attempts.
            current_attempts = current_attempts + 1

            # If this vertex is already colored, continue to the next vertex.
            if color != 0:
                continue

            # Get the neighbors (connected vertices) of the current vertex
            neighbors = list(graph.neighbors(vertex))

            # Make a list of all colors of colored neighbors of the current
            # vertex
            connected_colors = []
            # Iterate through all neighbors to get connected colors
            for neighbor in neighbors:
                color = vertex_mapping[neighbor]
                # If the vertex is colored and is unique, add it to the list of
                # connected colors to track all utilized colors
                if color != 0 and color not in connected_colors:
                    connected_colors.append(color)

            # Calculate the lowest unused color - see if there are any colors
            # <= 8 (since this is zero-based indexing) that are currently
            # unused.
            unused_colors = list(set(range(1, 10)) - set(connected_colors))
            # If this list is empty, all colors have been used and a new
            # one is needed. As such, the Sudoku puzzle won't actually be
            # solved. Break this iteration and start a new one.
            #
            # Note: implicit boolean-ness means that an empty list evaluates to
            # false in Python
            if not unused_colors:
                attempts = attempts + 1
                # Start a new iteration by randomizing the order the vertices will
                # be colored in (randomize vertex_mapping)
                vertex_mapping = original_vertex_mapping
                vertex_mapping = shuffle_dict(vertex_mapping)
                # break from the current for loop and run again
                solved = False
                print(f"Attempt: {attempts} | Failed at vertex {current_attempts}")
                break

            # If this list is not empty, color with the minimum color
            vertex_mapping[vertex] = min(unused_colors)

        # If the inner loop is broken, break the outer loop.
        if not solved:
            continue

        # If this point is reached, assume the solution is valid. Return
        # the valid set of colorings and print clock.
        elapsed_time = time.time() - start_time
        print(f"Completed on attempt {attempts}. Time taken: {elapsed_time:.2f}")
        return vertex_mapping, elapsed_time, attempts


def shuffle_dict(dictionary):
    """
    Shuffle the order of items in a dictionary.

    Args:
        dictionary: dict to the shuffled

    Returns: a shuffled version of the original dictionary
    """
    dict_tuple = list(dictionary.items())
    # ensure the dictionary is actually shuffled
    while dict_tuple == list(dictionary.items()):
        random.shuffle(dict_tuple)
    return dict(dict_tuple)


def graph_sudoku(graph, vertex_mapping, fig_size: int = 9, size: int = 3):
    """
    Visualize the Sudoku game as a graph using Networkx and Matplotlib.
    Each cell in the game is represented by a vertex, and the colors of
    the vertices correspond to the values in `vertex_mapping`. The
    edges represent the adjancency (and therefore the relationships and
    constraints) between the cells (the vertices). Each unique value in
    Sudoku is represented by a different color.

    Inputs:
        vertex_mapping: A dictionary mapping each vertex to its color
        value (or in this case, the numerical value). The keys are
        integers that represent the index of the vertex, and the values
        are the value of the vertex at that index. Each vertex value
        corresponds to a different color. A value of 0 indicates that
        the vertex is "uncolored" (as in, it has no value assigned to
        it yet) while any other value indicates that it is colored.
        fig_size: An integer representing the figure size of the
        visual. By default, it is set to 9. The visual is a square.
        size: An integer representing the size of the Sudoku graph,
        where the dimension is size**2 by size**2. By default, the
        size is 3.

    Returns:
        Nothing, but it does make the graph show up.
    """

    # Create positions for the nodes in a grid layout
    pos = dict(
        zip(list(graph.nodes()), nx.grid_2d_graph(size * size, size * size).nodes())
    )

    # Determine the minimum and maximum values in the vertex mappin
    low, *_, high = sorted(vertex_mapping.values())
    # Normalize the values for color mapping
    norm = mpl.colors.Normalize(vmin=low, vmax=high, clip=True)
    # Use Set3 because it features 12 colors
    mapper = mpl.cm.ScalarMappable(
        norm=norm, cmap=mpl.cm.Set3  # pylint: disable=no-member
    )
    # Create the graph
    plt.figure(figsize=(fig_size, fig_size))
    nx.draw(
        graph,
        labels=vertex_mapping,  # Use vertex_mapping for labeling nodes
        pos=pos,  # Positions of the nodes
        with_labels=True,  # Display labels on the nodes
        node_color=[
            mapper.to_rgba(i) for i in vertex_mapping.values()
        ],  # Color nodes based on their values
        width=1,  # Width of the edges
        node_size=1000,  # Size of the vertices
    )
    plt.show()  # Show the graph


def main():
    """
    Runs the Greedy coloring algorithm for an example puzzle.
    """

    N = 3  # Make the sudoku grid 3x3 (standard 9x9)
    G = nx.sudoku_graph(N)  # Creates a graph representation of Sudoku

    mapping = dict(zip(G.nodes(), sudoku_puzzles.puzzle_hard_1.flatten()))

    test_mapping, _, _ = greedy(G, mapping)
    graph_sudoku(G, test_mapping)


# Run the main function.
if __name__ == "__main__":
    main()
