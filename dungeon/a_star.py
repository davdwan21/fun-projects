import heapq

# to be honest this algorithm is pretty bs. it literally just tries to go
# straight to the goal and if it doesnt work it just backtracks and tries again lol

class Cell:
    def __init__(self):
        self.row = 0
        self.col = 0
        self.f = float("inf")
        self.g = float("inf")
        self.h = 0 # integer because of manhattan distance

def is_valid(row, col, ROWS, COLS):
    return (row >= 0) and (row < ROWS) and (col >= 0) and (col < COLS)

def not_a_wall(grid, row, col):
    return grid[row][col] != "#"

def at_end(row, col, end):
    return (row == end[0]) and (col == end[1])
        
def calculate_h(row, col, end):
    return (abs(row - end[0]) + abs(col - end[1]))

def a_star_search(grid, start, end):
    """
    initialize lists for all cells and visited cells (empty at first)
    initialize starting cell
    initialize open list as a heapqueue and push starting cell into it
    
    search loop
        take node with smallest f value
        for each direction (up down left right)
            check if the new node is: exists (in the list), not a wall (unblocked), not already visited
            if the new node is the destination terminate return true
            else:
                calculate fgh values for the new node
                if the new node is not visited or the new f value is smaller
                    add the node to the open queue
                    
    if the end is never found, return false
    """
    closed_list = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]
    cells = [[Cell() for _ in range(len(grid[0]))] for _ in range(len(grid))]
    
    row = start[0]
    col = start[1]
    cells[row][col].f = 0
    cells[row][col].g = 0
    cells[row][col].h = 0
    cells[row][col].row = row
    cells[row][col].col = col
    
    open_list = []
    heapq.heapify(open_list)
    heapq.heappush(open_list, (0.0, row, col))
    
    while len(open_list) > 0:
        current_cell = heapq.heappop(open_list)
        
        row = current_cell[1]
        col = current_cell[2]
        closed_list[row][col] = True
        
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        for dir in directions:
            new_row = row + dir[0]
            new_col = col + dir[1]
            
            if is_valid(new_row, new_col, len(grid), len(grid[0])) and not_a_wall(grid, new_row, new_col) and not closed_list[new_row][new_col]:
                if at_end(new_row, new_col, end):
                    return True
                else:
                    new_g = cells[row][col].g + 1.0
                    new_h = calculate_h(new_row, new_col, end)
                    new_f = new_g + new_h
                    
                    if cells[new_row][new_col].f == float("inf") or cells[new_row][new_col].f > new_f:
                        heapq.heappush(open_list, (new_f, new_row, new_col))
                        
                        cells[new_row][new_col].f = new_f
                        cells[new_row][new_col].g = new_g
                        cells[new_row][new_col].h = new_h
                        cells[new_row][new_col].row = row
                        cells[new_row][new_col].col = col
    return False
    
def main():
    """
    grid
    start
    end
    
    run algorithm
    
    return
    """
    # grid for testing
    grid = [["-", "-", "#"],
            ["#", "-", "-"],
            ["-", "#", "-"]]
    start = [0, 0]
    end = [len(grid) - 1, len(grid[0]) - 1]
    
    path_found = a_star_search(grid, start, end)
    
    print(path_found)
    
if __name__ == "__main__":
    main()