import argparse
import time
import os
import matplotlib.pyplot as plt
import random

def solve_sudoku(grid, explain=False, hint=None):
    """
    Solve Sudoku problem using backtracking.
    :param grid: a list of m x m, representing the Sudoku puzzle, where 0 indicates an empty cell.
    :param explain: whether to show each step of the solving process. Default is False.
    :param hint: int, the number of cells to be filled in the solution. Default is None.
    :return: the solved puzzle if there exists a solution; otherwise, return None. Also return explanations if explain is True.
    """
    n = len(grid)
    m = int(n ** 0.5)  # determine the size of each sub-grid
    explanations = []

    def find_empty():
        """
        Find the position of the first empty cell in the Sudoku puzzle.
        :return: the position (row, col) of the empty cell if found; otherwise, return None.
        """
        for row in range(n):
            for col in range(n):
                if grid[row][col] == 0:
                    return row, col
        return None

    def is_valid(num, row, col):
        """
        Check whether it is valid to place num in the (row, col) cell of the Sudoku puzzle.
        :param num: the number to be placed.
        :param row: the row number of the cell.
        :param col: the column number of the cell.
        :return: True if it is valid to place num in the cell; otherwise, return False.
        """
        # check row and column
        for i in range(n):
            if grid[row][i] == num or grid[i][col] == num:
                return False
        # check sub-grid
        box_row = (row // m) * m
        box_col = (col // m) * m
        for i in range(m):
            for j in range(m):
                if grid[box_row + i][box_col + j] == num:
                    return False
        return True

    def solve(steps=0):
        """
        Solve the Sudoku puzzle using backtracking.
        :param steps: the number of steps taken in the solving process.
        :return: True if a solution is found; otherwise, return False.
        """
        if hint is not None and steps >= hint:
            return True
        pos = find_empty()
        if not pos:
            return True
        row, col = pos
        for num in range(1, n + 1):
            if is_valid(num, row, col):
                grid[row][col] = num
                if explain:
                    explanation = f"Place {num} at ({row}, {col});"
                    explanations.append(explanation)
                if solve(steps + 1):
                    return True
                grid[row][col] = 0
        return False

    if solve():
        if explain:
            return grid, explanations
        else:
            return grid, None
    else:
        if explain:
            return None, explanations
        else:
            return None, None

def print_grid(grid):
    for row in grid:
        print(row)

def read_grid_from_file(filename):
    grid = []
    with open(filename, 'r') as f:
        for line in f:
            row = [int(cell) for cell in line.strip().split()]
            grid.append(row)
    return grid

def write_solution_to_file(filename, solution, explanations=None):
    with open(filename, 'w') as f:
        if solution:
            for row in solution:
                f.write(' '.join(str(cell) for cell in row))
                f.write(os.linesep)
            if explanations:
                f.write(os.linesep)
                f.write("Explanations:")
                f.write(os.linesep)
                for explanation in explanations:
                    f.write(explanation)
                    f.write(os.linesep)
        else:
            f.write("No solution found.")

def generate_sudoku_puzzles(grid_sizes, difficulties):
    puzzles = []
    for grid_size in grid_sizes:
        for difficulty in difficulties:
            m, n = grid_size
            grid = [[0 for _ in range(n * m)] for _ in range(n * m)]
            puzzle, _ = solve_sudoku(grid)
            num_filled_cells = sum([1 for row in puzzle for cell in row if cell != 0])

            for _ in range(min(difficulty, num_filled_cells)):
                while True:
                    row = random.randint(0, n * m - 1)
                    col = random.randint(0, n * m - 1)
                    if puzzle[row][col] != 0:
                        puzzle[row][col] = 0
                        break
            puzzles.append(puzzle)
    return puzzles

def measure_solver_performance(sudoku_puzzles):
    time_data = []
    for puzzle in sudoku_puzzles:
        grid_size = len(puzzle)
        difficulty = sum(row.count(0) for row in puzzle)
        start_time = time.time()
        solve_sudoku(puzzle)
        end_time = time.time()
        time_taken = end_time - start_time
        time_data.append((grid_size, difficulty, time_taken))
    return time_data

def profile_sudoku_solver():
    # Define grid sizes and difficulties
    grid_sizes = [(2, 2), (3, 2), (3, 3)]
    difficulties = [10, 20, 30]  # Number of unfilled locations
    sudoku_puzzles = generate_sudoku_puzzles(grid_sizes, difficulties)
    time_data = measure_solver_performance(sudoku_puzzles)
    return time_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve Sudoku")
    parser.add_argument("--explain", action="store_true", help="Show each step of the solving process")
    parser.add_argument("--file", nargs=2, metavar=("INPUT", "OUTPUT"), help="Reads a grid from a file and saves the solution to another file")
    parser.add_argument("--hint", type=int, help="Return a grid with N values filled in")
    parser.add_argument("--profile", action="store_true", help="Measure the performance of the solver(s)")
    args = parser.parse_args()    

        # Implement --file flag
    if args.file:
        input_file, output_file = args.file
        grid = read_grid_from_file(input_file)
        solution = solve_sudoku(grid, explain=args.explain, hint=args.hint)
        write_solution_to_file(output_file, solution, args.explain)
    else:
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

    # Implement --hint flag
    if args.hint is not None:
        solution = solve_sudoku(grid, explain=args.explain, hint=args.hint)
        if solution:
            print_grid(solution)
        else:
            print("No solution found.")

    # Implement --profile flag
    elif args.profile:
        print(profile_sudoku_solver())

    # Default behavior
    else:
        solution = solve_sudoku(grid, explain=args.explain)
        if solution:
            print_grid(solution)
        else:
            print("No solution found.")

    solution = solve_sudoku(grid, explain=args.explain)