# -*- coding: utf-8 -*-
"""
Created on Tue May  2 18:55:25 2023

@author: MSI
"""

from random import choice

def wavefront_propagation(grid):
    size = len(grid)
    # Initialize list of possible values for each cell
    possible_values = [[list(range(1, size+1)) for j in range(size)] for i in range(size)]
    for i in range(size):
        for j in range(size):
            if grid[i][j] != 0:
                possible_values[i][j] = []

    # Define function to update the list of possible values
    def update_possible_values():
        for i in range(size):
            for j in range(size):
                if grid[i][j] == 0:
                    # Check row
                    for val in grid[i]:
                        if val in possible_values[i][j]:
                            possible_values[i][j].remove(val)
                    # Check column
                    for row in grid:
                        if row[j] in possible_values[i][j]:
                            possible_values[i][j].remove(row[j])
                    # Check square
                    row_start = (i // int(size**0.5)) * int(size**0.5)
                    col_start = (j // int(size**0.5)) * int(size**0.5)
                    for row in range(row_start, row_start + int(size**0.5)):
                        for col in range(col_start, col_start + int(size**0.5)):
                            if grid[row][col] in possible_values[i][j]:
                                possible_values[i][j].remove(grid[row][col])

    # Define function to check if Sudoku is solved
    def is_solved():
        for row in grid:
            if 0 in row:
                return False
        return True

    # Solve Sudoku
    while not is_solved():
        update_possible_values()
        made_progress = False
        # Fill in cells with only one possible value
        for i in range(size):
            for j in range(size):
                if len(possible_values[i][j]) == 1:
                    grid[i][j] = possible_values[i][j][0]
                    possible_values[i][j] = []
                    made_progress = True
        if not made_progress:
            # If no progress is made, choose cell with minimum possible values and randomly select one
            min_len = size+1
            min_pos = None
            for i in range(size):
                for j in range(size):
                    if 1 < len(possible_values[i][j]) < min_len:
                        min_len = len(possible_values[i][j])
                        min_pos = (i, j)
            if min_pos is not None:
                i, j = min_pos
                grid[i][j] = choice(possible_values[i][j])
                possible_values[i][j] = []

    return grid

# Solve Sudoku
grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

solution = wavefront_propagation(grid)
if solution:
    for row in solution:
        print(row)
else:
    print("No solution")