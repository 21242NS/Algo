def blacklist(grid: list[int], n: int) -> set[int]:
    i, j = n // 9, n % 9


    row = set(grid[9*i + k] for k in range(9))


    col = set(grid[9*k + j] for k in range(9))

    bi, bj = 3*(i // 3), 3*(j // 3)
    block = set(grid[9*(bi + x) + (bj + y)] for x in range(3) for y in range(3))

    return row | col | block  | {0}   
def solve(grid: list[int]):
   
    try:
        n = grid.index(0)
    except ValueError:
        return grid


    forbidden = blacklist(grid, n)
    for i in range(1, 10):
        if i not in forbidden:
            grid[n] = i
            res = solve(grid)
            if res is not None:
                return res   
            grid[n] = 0

    return None 
def print_sudoku(grid: list[int]):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)

        row = ""
        for j in range(9):
            if j % 3 == 0 and j != 0:
                row += "| "
            row += str(grid[9*i + j]) + " "
        print(row)
print_sudoku(solve(81*[0]))