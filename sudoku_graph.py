"""
This module creates a class `SudokuGraph`, which uses a graph coloring
approach to solve Sudoku puzzles. The class uses the NetworkX library 
to represent Sudoku as a graph, where vertices represent the cells and
edges represent the constraints for each cell. Each unique value in the
cells correspond to a different color.

So far, this class has the ability to solve Sudoku using the DSatur
algorithm, which colors vertices based on their degrees of saturation.
"""

import random
import time
import copy
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


class SudokuGraph:
    """
    A class to represent a Sudoku puzzle as a graph and solve it using
    graph coloring algorithms.

    Attributes:
        self.puzzle: A 2D Numpy array representing the unfinished
        Sudoku puzzle.
        self.size: An integer representing the size of Sudoku
        puzzle, where the amount of vertices = size ** 4.
        self.graph: A NetworkX graph object representing the Sudoku
        pizzle as a graph.
        self.mapping: A dictionary mapping each vertex to its color
        value (or in this case, the numerical value). The keys are
        integers that represent the index of the vertex, and the
        values are the value of the vertex at that index. Each
        vertex value corresponds to a different color. A value of 0
        indicates that the vertex is "uncolored" (as in, it has no
        value assigned to it yet) while any other value indicates
        that it is colored. When solving the Sudoku puzzle, this
        will be the attribute that is modified and updated with new
        number assignments.
            self.original_mapping: The original Sudoku puzzle
            without modifications (the blank, unsolved puzzle).
            self.solution: The solve Sudoku puzzle.

    Methods:
        check_size(): Validates that the Sudoku puzzle is a square
        grid.
        reset_puzzle(): Resets the puzzle to its original state.
        get_degrees_of_saturation(): Calculates the degree of
        saturation and unsaturation for uncolored vertices.
        select_max_degree_of_saturation(): Selects the vertex with the
        maximum degree of saturation.
        get_value_counts(): Counts occurrences of each value in the
        Sudoku puzzle.
        dsatur(): Solves the Sudoku puzzle using the DSatur
        algorithm.
        graph_sudoku(): Visualizes the Sudoku puzzle as a graph using
        Matplotlib.
    """

    def __init__(self, sudoku_puzzle):
        """
        Initialize the SudokuGraph class with a given puzzle.
        This will turn the Sudoku puzzle into a graph representation.

        Inputs:
            puzzle: A 2D Numpy array representing the unfinished Sudoku
            puzzle. It must be square and contain only integers.
        """
        self.puzzle = sudoku_puzzle
        self.size = self.check_size()
        self.graph = nx.sudoku_graph(self.size)
        # Maps each node in graph to its corresponding value
        self.mapping = dict(zip(self.graph.nodes(), self.puzzle.flatten()))
        self.original_mapping = copy.deepcopy(self.mapping)
        self.solution = None

    def check_size(self):
        """
        Ensures the the Sudoku puzzle is square.

        Returns:
            The size of the Sudoku puzzle, where the amount of vertices
            is size ** 4 (as defined by NetworkX).
        """
        size = len(self.puzzle)
        if (size**0.5).is_integer():
            return int(size**0.5)  # Convert to integer
        raise ValueError("Invalid size: The puzzle must be a square grid.")

    def reset_puzzle(self):
        """
        Resets the puzzle to its original state.

        Returns:
            self.mapping: A dictionary mapping each vertex to its color
            value (or in this case, the numerical value). The keys are
            integers that represent the index of the vertex, and the values
            are the value of the vertex at that index. Each vertex value
            corresponds to a different color. A value of 0 indicates that
            the vertex is "uncolored" (as in, it has no value assigned to
            it yet) while any other value indicates that it is colored.
        """
        self.mapping = copy.deepcopy(self.original_mapping)
        return self.mapping

    def get_degrees_of_saturation(self):
        """
        Calculate the degree of saturation and unsaturation for uncolored
        vertices in a graph.

        The degree of saturation for a vertex is defined as the number of
        colored neighbors it has, while the degree of unsaturation is
        defined as the number of uncolored neighbors.

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
            vertex for vertex in self.mapping if self.mapping[vertex] == 0
        ]
        # The amount of colored vertices in a vertex's neighborhood
        colored_vertices_degree_of_saturation = []
        # The amount of uncolored vertices in a vertex's neighborhood
        uncolored_vertices_degree_of_unsaturation = []

        # Iterate for each vertex that is uncolored
        for vertex in uncolored_vertices:
            # Get the neighbors of the vertex
            neighborhood_indices = sorted(self.graph.neighbors(vertex))
            # Get the values of each vertex in the neighborhood
            values_of_neighborhood = [self.mapping[key] for key in neighborhood_indices]
            # Get the amount of colored vertices in its neighborhood
            colored_neighbors = len(
                neighborhood_indices
            ) - values_of_neighborhood.count(0)
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

    def select_max_degree_of_saturation(self):
        """
        Select the vertex with the maximum degree of saturation from a
        graph. Specifically, it takes the uncolored vertices of the graph.
        In the case of a tie, one of the vertices is randomly chosen.

        Returns:
            chosen_vertex: An integer representing the index of the
            uncolored vertex with the maximum degree of saturation. If
            there are no uncolored vertices, it returns `None` instead.
            max_degree_of_saturation: An integer representing the value of
            the maximum degree of saturation. If there are no uncolored
            vertices, it returns `None` instead.
        """
        # Get the degrees of saturation of all of the uncolored vertices
        colored_dictionary, _ = self.get_degrees_of_saturation()

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

    def get_value_counts(self, lowest: int = 0, highest: int = 10):
        """
        Counts the occurences of each value in a Sudoku. This will count
        the amount of times each value (by default, it is 0-9, as a normal
        game of Sudoku has values 1-9, and 0 represents an unfilled square).

        Inputs:
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
        for _, value in self.mapping.items():
            if 0 <= value <= 9:
                value_counts[value] += 1

        # Return the dictionary
        return value_counts

    def dsatur(self, inf=False):
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
            inf: A boolean representing whether or not to infinitely run
            the loop until a solution is found. If it is set to `True`,
            the function will run until a solution is found. If it is set
            to `False`, it will attempt once and output that result, even
            if it is incorrect.

        Returns:
            self.mapping: A dictionary mapping each vertex to its color
            value (or in this case, the numerical value). The keys are
            integers that represent the index of the vertex, and the values
            are the value of the vertex at that index. Each vertex value
            corresponds to a different color. A value of 0 indicates that
            the vertex is "uncolored" (as in, it has no value assigned to
            it yet) while any other value indicates that it is colored.
        """
        # Set up starting variables
        attempts = 0  # Count the amount of attempts
        start_time = time.time()  # Start timing how long it takes

        # Run the loop until a valid configuration is found
        while True:

            # Get the uncolored vertices
            current_vertex, _ = self.select_max_degree_of_saturation()

            # If there are no uncolored vertices, that means the Sudoku
            # puzzle has been solved and the loop can be broken
            if current_vertex is None:
                break

            # Get all of the neighbors of the current vertex
            neighbors = self.graph.neighbors(current_vertex)

            # Get the colors/values of the neighbors
            neighbor_colors = {
                self.mapping[neighbor]
                for neighbor in neighbors
                if self.mapping[neighbor] != 0
            }

            # Take the amount of times each value occurs
            value_counts = self.get_value_counts()
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
                self.mapping[current_vertex] = color
            # If there are no available colors/values, then this
            # configuration is invalid. Reset the Sudoku graph to its
            # original state and add to the `attempts` counter.
            except (IndexError, ValueError):
                # Check if the infinite flag is set
                if inf:
                    self.reset_puzzle()
                    attempts += 1
                    print(f"Attempt: {attempts} | Failed at vertex: {current_vertex}")
                    continue
                if not inf:
                    print("Exiting...")
                    break

        # Calculate the amount of time the function ran for
        end_time = time.time()
        elapsed_time = end_time - start_time
        self.solution = self.mapping
        print(f"Total time taken: {elapsed_time:.2f} seconds")
        # Return the vertex mapping dictionary
        return self.solution, elapsed_time, attempts

    def graph_sudoku(self, show_solution: bool = True, fig_size: int = 9):
        """
        Visualize the Sudoku game as a graph using NetworkX and
        Matplotlib. Each cell in the game is represented by a vertex,
        and the colors of the vertices correspond to the values in
        `mapping`. The edges represent the adjancency (and therefore
        the relationships and constraints) between the cells (the
        vertices). Each unique value in Sudoku is represented by a
        different color.

        Inputs:
            fig_size: An integer representing the figure size of the
            visual. By default, it is set to 9. The visual is a square.

        Returns:
            Nothing, but it does make the graph show up.
        """

        if show_solution:
            mapping = self.solution
        else:
            mapping = self.original_mapping

        # Create positions for the nodes in a grid layout
        pos = dict(
            zip(
                list(self.graph.nodes()),
                nx.grid_2d_graph(self.size * self.size, self.size * self.size).nodes(),
            )
        )

        # Determine the minimum and maximum values in the vertex mappin
        low, *_, high = sorted(mapping.values())
        # Normalize the values for color mapping
        norm = mpl.colors.Normalize(vmin=low, vmax=high, clip=True)
        # Use Set3 because it features 12 colors
        mapper = mpl.cm.ScalarMappable(
            norm=norm, cmap=mpl.cm.Set3  # pylint: disable=no-member
        )
        # Create the graph
        plt.figure(figsize=(fig_size, fig_size))
        nx.draw(
            self.graph,
            labels=mapping,  # Use self.mapping for labeling nodes
            pos=pos,  # Positions of the nodes
            with_labels=True,  # Display labels on the nodes
            node_color=[
                mapper.to_rgba(i) for i in mapping.values()
            ],  # Color nodes based on their values
            width=1,  # Width of the edges
            node_size=1000,  # Size of the vertices
        )
        plt.show()  # Show the graph


puzzle = np.asarray(
    [
        [8, 0, 9, 3, 0, 5, 6, 0, 0],
        [2, 6, 5, 9, 0, 8, 4, 3, 7],
        [1, 0, 0, 0, 2, 0, 5, 8, 0],
        [6, 8, 2, 4, 0, 1, 0, 7, 3],
        [3, 9, 4, 7, 0, 0, 0, 1, 5],
        [7, 5, 1, 8, 9, 0, 0, 4, 0],
        [0, 1, 0, 2, 3, 4, 7, 0, 8],
        [0, 0, 0, 5, 0, 0, 1, 6, 0],
        [5, 2, 0, 1, 7, 0, 3, 9, 0],
    ]
)

sudoku = SudokuGraph(puzzle)
sudoku.dsatur(True)
sudoku.graph_sudoku(show_solution=True)
