def solve_sudoku(grid):
    """
    Solve Sudoku problem using backtracking.
    :param grid: a list of m x m, representing the Sudoku puzzle, where 0 indicates an empty cell.
    :return: the solved puzzle if there exists a solution; otherwise, return None.
    """
    n = len(grid)
    m = int(n ** 0.5)  # determine the size of each sub-grid

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

    def solve():
        """
        Solve the Sudoku puzzle using backtracking.
        :return: True if a solution is found; otherwise, return False.
        """
        pos = find_empty()
        if not pos:
            return True
        row, col = pos
        for num in range(1, n + 1):
            if is_valid(num, row, col):
                grid[row][col] = num
                if solve():
                    return True
                grid[row][col] = 0
        return False

    if solve():
        return grid
    else:
        return None


# Test
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

solution = solve_sudoku(grid)
if solution:
    for row in solution:
        print(row)
else:
        print("No solution")

