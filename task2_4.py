import argparse
import numpy as np
import time
from tqdm import tqdm
from matplotlib import pyplot as plt

def solve_sudoku(grid, explain=False,hint_N=0):    
    """
    Solve Sudoku problem using backtracking.
    :param grid: a list of m x m, representing the Sudoku puzzle, where 0 indicates an empty cell.
    :param explain: whether to show each step of the solving process. Default is False.
    :return: the solved puzzle if there exists a solution; otherwise, return None.
    """
    n = len(grid)
    m = int(n ** 0.5)  # determine the size of each sub-grid
    hint_cnt=0
    
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
    
    def solve(hint_cnt):
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
                if explain and hint_cnt<hint_N:
                    print(f"Place {num} at ({row}, {col});")
                    hint_cnt+=1
                if not hint_cnt<hint_N:
                    return True
                if solve(hint_cnt):
                    return True
                grid[row][col] = 0
        return False

    if solve(hint_cnt):
        return grid
    else:
        return None

def print_grid(grid):
    """
    Print the current state of the Sudoku puzzle.
    """
    for row in grid:
        print(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve Sudoku")
    parser.add_argument("--explain", action="store_true", help="Show each step of the solving process")
    parser.add_argument('--hint', type=int, default=3, help='Returns a grid with N values filled in')
    parser.add_argument("--profile", action="store_true", help="Measures the performance and plot analysis")
    args = parser.parse_args()

    # solve Sudoku
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
    # print(args.explain,args.hint,args.profile)
    zero_cnt=np.array(grid).size-np.count_nonzero(grid)
    # print(zero_cnt)

    args.profile=True
    st=time.time()
    if args.profile:
        end_list=[]
        for N in tqdm(range(zero_cnt)):
            for _ in range(10000):
                solution = solve_sudoku(grid, explain=args.explain,hint_N=N)
            end=time.time()
            end_list.append((end-st)/10)
        
        plt.scatter([i for i in range(len(end_list))],end_list,s=0.5,label='run time')
        plt.xlabel('Non-zero elements need to be fiiled',fontdict={'weight': 'normal', 'size': 13})
        plt.ylabel('run time',fontdict={'weight':'normal', 'size': 13})
        plt.legend()
        plt.show()
    else:
        solution = solve_sudoku(grid, explain=args.explain,hint_N=args.hint)

        if solution:
            print_grid(solution)
        else:
            print("No solution found.")

# example: python part2.4.py --explain --profile

