"""
Some sample sudoku problems to test solving algorithms.
"""

import numpy as np

# Small
puzzle_small = np.array([[2, 0, 0, 0], [3, 0, 0, 4], [0, 2, 0, 0], [0, 3, 4, 0]])

# HARD
puzzle_hard_1 = np.asarray(
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

# HARD
puzzle_hard_2 = np.asarray(
    [
        [0, 0, 4, 0, 0, 3, 5, 6, 8],
        [5, 0, 0, 8, 0, 7, 0, 4, 2],
        [0, 0, 0, 0, 0, 4, 0, 0, 0],
        [8, 0, 5, 0, 1, 2, 0, 0, 0],
        [0, 0, 0, 0, 5, 0, 2, 0, 9],
        [0, 0, 0, 0, 0, 0, 6, 0, 0],
        [0, 7, 8, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 5, 0],
        [6, 0, 0, 9, 0, 0, 0, 7, 0],
    ]
)

# HARD
puzzle_hard_3 = np.asarray(
    [
        [0, 0, 3, 0, 0, 0, 0, 0, 9],
        [0, 2, 0, 0, 9, 4, 8, 0, 0],
        [0, 9, 4, 0, 0, 0, 0, 7, 2],
        [7, 3, 0, 0, 0, 0, 0, 0, 5],
        [0, 0, 9, 1, 0, 0, 0, 0, 3],
        [6, 0, 1, 3, 4, 0, 0, 2, 0],
        [0, 0, 0, 7, 0, 0, 2, 0, 4],
        [0, 0, 0, 2, 8, 1, 0, 0, 0],
        [0, 0, 0, 0, 6, 9, 0, 5, 0],
    ]
)

# Easy
puzzle_easy = np.asarray(
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
puzzle_super_easy = np.asarray(
    [
        [5, 3, 2, 9, 6, 4, 1, 8, 7],
        [6, 8, 9, 7, 5, 1, 4, 2, 3],
        [4, 7, 1, 0, 3, 0, 5, 9, 6],
        [7, 6, 4, 5, 0, 9, 3, 0, 2],
        [8, 1, 0, 6, 0, 0, 0, 4, 0],
        [0, 2, 3, 0, 1, 7, 0, 0, 0],
        [1, 0, 7, 0, 9, 0, 8, 3, 5],
        [2, 5, 6, 0, 0, 8, 9, 0, 1],
        [3, 9, 8, 1, 7, 0, 0, 0, 0],
    ]
)

all_puzzles = [puzzle_easy, puzzle_hard_1, puzzle_hard_2, puzzle_hard_3]
