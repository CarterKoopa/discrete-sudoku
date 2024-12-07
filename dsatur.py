"""
This module implements the DSatur graph coloring algoritm to solve
Sudoku puzzles. In this, the Sudoku puzzles are represented as graphs,
where vertices (AKA nodes) represent the cells while the edges
represent the adjancency (and therefore the relationships and 
constraints) between the cells (which are the vertices). Each unique
value in the cells are assigned a different colors. Cells with the same
value are labeled with the same color.

The way DSatur works is that it finds the uncolored vertex with the
highest number of colors in its neighborhood (AKA the degree of 
saturation). If these is a tie, then usually the vertex with the
highest degree in the subgraph composed of the uncolored vertices is
chosen. That vertex is then colored using a color label not being
used by any of its neighbors. These steps are repeated until all of the
vertices have been colored.

In the case of Sudoku, the DSatur algorithm has been slightly modified.
If an uncolored vertex is selected but its neighbors already use up 9 
other colors (not including the color assigned to 0, which indicates an
uncolored cell/vertex), then that configuration is scapped and a new
one is started from scratch. Additionally, because all of the vertices
in a Sudoku graph have the same degree, if there is a tie for the 
degree of saturation, a vertex from the tied vertices is randomly
selected.

The functions included are:
    get_degrees_of_saturation: Gets the degree of saturation and 
    unsaturation for the uncolored vertices in a graph.
    get_max_degree_of_saturation: Selects the uncolored vertex with 
    the highest degree in a graph.
    get_value_counts: Counts the amount of time each value appears in
    the Sudoku graph.
    dsatur: Uses the Dsatur algorithm to solve a Sudoku puzzle.
    graph_sudoku: Visualizes the Sudoku puzzle.
"""

# Import libraries
import random
import copy
import time
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx


def get_degrees_of_saturation(graph, vertex_mapping):
    """
    Calculate the degree of saturation and unsaturation for uncolored
    vertices in a graph.

    The degree of saturation for a vertex is defined as the number of
    colored neighbors it has, while the degree of unsaturation is
    defined as the number of uncolored neighbors.

    Inputs:
        graph: A Networkx graph object representing the graph in which
        the vertices are located.
        vertex_mapping:  A dictionary mapping each vertex to its color
        value (or in this case, the numerical value). The keys are
        integers that represent the index of the vertex, and the values
        are the value of the vertex at that index. Each vertex value
        corresponds to a different color. A value of 0 indicates that
        the vertex is "uncolored" (as in, it has no value assigned to
        it yet) while any other value indicates that it is colored.

    Returns:
        colored_dictionary: A dictionary mapping each uncolored vertex
        to its degree of saturation (number of colored neighbors). The
        keys and values are both integers.
        uncolored_dictionary: A dictionary mapping each uncolored
        vertex to its degree of unsaturation (number of uncolored
        neighbors). The keys and values are both integers.
    """
    # Get all of the uncolored vertices
    uncolored_vertices = [
        vertex for vertex in vertex_mapping if vertex_mapping[vertex] == 0
    ]
    # The amount of colored vertices in a vertex's neighborhood
    colored_vertices_degree_of_saturation = []
    # The amount of uncolored vertices in a vertex's neighborhood
    uncolored_vertices_degree_of_unsaturation = []

    # Iterate for each vertex that is uncolored
    for vertex in uncolored_vertices:
        # Get the neighbors of the vertex
        neighborhood_indices = sorted(graph.neighbors(vertex))
        # Get the values of each vertex in the neighborhood
        values_of_neighborhood = [vertex_mapping[key] for key in neighborhood_indices]
        # Get the amount of colored vertices in its neighborhood
        colored_neighbors = len(neighborhood_indices) - values_of_neighborhood.count(0)
        # Get the amount of uncolored vertices in its neighborhood
        uncolored_neighbors = values_of_neighborhood.count(0)
        # Add each to a list
        colored_vertices_degree_of_saturation.append(colored_neighbors)
        uncolored_vertices_degree_of_unsaturation.append(uncolored_neighbors)

    # Create a dictionary containing the indices of the uncolored
    # vertices and their corresponding degree of saturation or unsaturation
    colored_dictionary = dict(
        zip(uncolored_vertices, colored_vertices_degree_of_saturation)
    )
    uncolored_dictionary = dict(
        zip(uncolored_vertices, uncolored_vertices_degree_of_unsaturation)
    )
    # Return the dictionaries
    return colored_dictionary, uncolored_dictionary


def select_max_degree_of_saturation(graph, vertex_mapping):
    """
    Select the vertex with the maximum degree of saturation from a
    graph. Specifically, it takes the uncolored vertices of the graph.
    In the case of a tie, one of the vertices is randomly chosen.

    Inputs:
        graph: A Networkx graph object representing the graph in which
        the vertices are located.
        vertex_mapping: A dictionary mapping each vertex to its color
        value (or in this case, the numerical value). The keys are
        integers that represent the index of the vertex, and the values
        are the value of the vertex at that index. Each vertex value
        corresponds to a different color. A value of 0 indicates that
        the vertex is "uncolored" (as in, it has no value assigned to
        it yet) while any other value indicates that it is colored.

    Returns:
        chosen_vertex: An integer representing the index of the
        uncolored vertex with the maximum degree of saturation. If
        there are no uncolored vertices, it returns `None` instead.
        max_degree_of_saturation: An integer representing the value of
        the maximum degree of saturation. If there are no uncolored
        vertices, it returns `None` instead.
    """
    # Get the degrees of saturation of all of the uncolored vertices
    colored_dictionary, _ = get_degrees_of_saturation(graph, vertex_mapping)

    # If there are uncolored vertices, get the maximum degree of
    # saturation. Otherwise, return `None`
    try:
        max_degree_of_saturation = max(colored_dictionary.values())
    except ValueError:
        return None, None

    # Check if there are multiple with the highest degree of saturation
    if list(colored_dictionary.values()).count(max_degree_of_saturation) > 1:

        # Look for all of the vertices with the highest degree found
        contenders = [
            vertex
            for vertex, degree_of_saturation in colored_dictionary.items()
            if degree_of_saturation == max_degree_of_saturation
        ]

        # Because all of them have the same amount of edges (due to
        # the nature of Sudoku), randomly choose one
        chosen_vertex = random.choice(contenders)
        # Return the chosen vertex and its degree of saturation
        return chosen_vertex, max_degree_of_saturation

    # If there is only one, simply return the vertex and its degree of saturation
    chosen_vertex = max(colored_dictionary, key=colored_dictionary.get)
    return chosen_vertex, max_degree_of_saturation


def get_value_counts(vertex_mapping, lowest: int = 0, highest: int = 10):
    """
    Counts the occurences of each value in a Sudoku. This will count
    the amount of times each value (by default, it is 0-9, as a normal
    game of Sudoku has values 1-9, and 0 represents an unfilled square).

    Inputs:
        vertex_mapping: A dictionary mapping each vertex to its color
        value (or in this case, the numerical value). The keys are
        integers that represent the index of the vertex, and the values
        are the value of the vertex at that index. Each vertex value
        corresponds to a different color. A value of 0 indicates that
        the vertex is "uncolored" (as in, it has no value assigned to
        it yet) while any other value indicates that it is colored.
        lowest: An integer representing the lowest value appearing in
        the Sudoku game.
        highest: An integer representing the highest value appearing in
        a Sudoku game.

    Returns:
        value_counts: A dictionary representing the amount of times
        each value occurs in a Sudoku game. The keys are integers that
        represent all the possible values in the Sudoku game, and the
        values are integers that represent how often they occur.
    """
    # Create a dictionary to count the amount of times each value appears
    value_counts = {key: 0 for key in range(lowest, highest)}
    # Loop through every vertex and count the occurence of each value
    for _, value in vertex_mapping.items():
        if 0 <= value <= 9:
            value_counts[value] += 1

    # Return the dictionary
    return value_counts


def dsatur(graph, vertex_mapping, inf=False):
    """
    Use the DSatur (Degree of Saturation) algorithm for graph coloring
    to solve a Sudoku puzzle.

    DSatur works by selecting the vertex with the lowest degree of
    saturation, which is the number of different colors in its
    neighborhood. If there is a tie for highest degree of saturation,
    a random vertex is selected from the tied vertices.

    Once a vertex is selected, the vertex is colored so that it does
    not conflict with any of its neighbors. In the context of Sudoku,
    that means it cannot take on a value that one of its neighbors has.
    If there is no color that the randomly selected vertex can take on,
    the vertex mapping is reset to the original and the process begins
    again.

    Please note that this may take a while to run

    Inputs:
        graph: A Networkx graph object representing the graph in which
        the vertices are located.
        vertex_mapping: A dictionary mapping each vertex to its color
        value (or in this case, the numerical value). The keys are
        integers that represent the index of the vertex, and the values
        are the value of the vertex at that index. Each vertex value
        corresponds to a different color. A value of 0 indicates that
        the vertex is "uncolored" (as in, it has no value assigned to
        it yet) while any other value indicates that it is colored.
        inf: A boolean representing whether or not to infinitely run
        the loop until a solution is found. If it is set to `True`,
        the function will run until a solution is found. If it is set
        to `False`, it will attempt once and output that result, even
        if it is incorrect.

    Returns:
        vertex_mapping: A dictionary mapping each vertex to its color
        value (or in this case, the numerical value). The keys are
        integers that represent the index of the vertex, and the values
        are the value of the vertex at that index. Each vertex value
        corresponds to a different color. A value of 0 indicates that
        the vertex is "uncolored" (as in, it has no value assigned to
        it yet) while any other value indicates that it is colored.
    """
    # Create a deep copy of the original vertex mapping so it can be reset
    original_vertex_mapping = copy.deepcopy(vertex_mapping)
    # Set up other variables
    attempts = 0  # Count the amount of attempts
    start_time = time.time()  # Start timing how long it takes

    # Run the loop until a valid configuration is found
    while True:

        # Get the uncolored vertices
        current_vertex, _ = select_max_degree_of_saturation(graph, vertex_mapping)

        # If there are no uncolored vertices, that means the Sudoku
        # puzzle has been solved and the loop can be broken
        if current_vertex is None:
            break

        # Get all of the neighbors of the current vertex
        neighbors = graph.neighbors(current_vertex)

        # Get the colors/values of the neighbors
        neighbor_colors = {
            vertex_mapping[neighbor]
            for neighbor in neighbors
            if vertex_mapping[neighbor] != 0
        }

        # Take the amount of times each value occurs
        value_counts = get_value_counts(vertex_mapping)
        # Filter out the amount of times each value occurs if it is NOT
        # in the current vertex's neighborhood. Also exclude 0s because
        # those are uncolored vertices.
        filtered_value_counts = {
            key: value
            for key, value in value_counts.items()
            if key not in neighbor_colors and key != 0
        }

        # Randomly select a color from the filtered value counts to
        # assign the currently selected vertex a color/value.
        try:
            color = random.choice(list(filtered_value_counts.keys()))
            vertex_mapping[current_vertex] = color
        # If there are no available colors/values, then this
        # configuration is invalid. Reset the Sudoku graph to its
        # original state and add to the `attempts` counter.
        except (IndexError, ValueError):
            # Check if the infinite flag is set
            if inf:
                vertex_mapping = copy.deepcopy(original_vertex_mapping)
                attempts += 1
                print(f"Attempt: {attempts} | Failed at: {current_vertex}")
                continue
            if not inf:
                print("Exiting...")
                break

    # Calculate the amount of time the function ran for
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total time taken: {elapsed_time:.2f} seconds")
    # Return the vertex mapping dictionary
    return vertex_mapping, elapsed_time, attempts


def graph_sudoku(vertex_mapping, fig_size: int = 9, size: int = 3):
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
    pos = dict(zip(list(G.nodes()), nx.grid_2d_graph(size * size, size * size).nodes()))

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
        G,
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


# Test the functions in an example Sudoku puzzle

# Create Sudoku puzzle
# --- The row corresponds to the first column of the sudoku puzzle
# --- The numbers indicate the values in the Sudoku puzzle from bottom up
# --- 0s mean that the cell is not filled in

# Here is a sample puzzle
puzzle = np.asarray(
    [
        [0, 4, 3, 0, 8, 0, 2, 5, 0],
        [6, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 9, 4],
        [9, 0, 0, 0, 0, 4, 0, 7, 0],
        [0, 0, 0, 6, 0, 8, 0, 0, 0],
        [0, 1, 0, 2, 0, 0, 0, 0, 3],
        [8, 2, 0, 5, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 5],
        [0, 3, 4, 0, 9, 0, 7, 1, 0],
    ]
)

N = 3  # Make the sudoku grid 3x3 (standard 9x9)
G = nx.sudoku_graph(N)  # Creates a graph representation of Sudoku
mapping = dict(
    zip(G.nodes(), puzzle.flatten())
)  # Maps each vertex in graph to its corresponding value

# Call the functions :)
# This make take a while to run
test_mapping, _, _ = dsatur(G, mapping, inf=True)
graph_sudoku(test_mapping)
