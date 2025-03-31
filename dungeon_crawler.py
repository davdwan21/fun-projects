from tabulate import tabulate
import random
import time

# fun idea: roll some dice for player movement, attack, etc. and force them to choose
class Dungeon:
    def __init__(self):
        self.board_size = 5
        self.exit_pos = [self.board_size - 1, self.board_size - 1]
        self.walls = []
        wall_origins = [[random.randint(1, self.board_size - 2), random.randint(1, self.board_size - 2)] for _ in range(self.board_size // 2)] # range is hardcoded, adjust for scalability
        for origin in wall_origins:
            directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
            extra_walls = random.sample(directions, random.randint(1, 2)) # extra_walls are hardcoded
            for extra in extra_walls:
                result = [row + col for row, col in zip(origin, extra)]
                self.walls.append(result)
        for wall in wall_origins:
            self.walls.append(wall)
            
        # prevent the exit or player from being replaced by a wall
        for i in range(len(self.walls) - 1):
            if self.walls[i] == [0, 0] or self.walls[i] == [self.board_size - 1, self.board_size - 1]:
                self.walls.pop(i)
                
        # complete random wall generation
        #self.walls = [[random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)] for _ in range(((self.board_size ** 2) * 2) // 5)]
        #for i in range(len(self.walls) - 1):
        #    if self.walls[i] == [0, 0] or self.walls[i] == [self.board_size - 1, self.board_size - 1]:
        #        self.walls.pop(i)
        
    def check_win(self, player):
        if [player.row, player.col] == self.exit_pos:
            print("you win!")
            return True
        return False
        
    def print_board(self, player):
        p_row, p_col = player.row, player.col
        board = [[" - " for _ in range(self.board_size)] for _ in range(self.board_size)]
        board[p_row][p_col] = "P"
        board[self.exit_pos[0]][self.exit_pos[1]] = "E"
        for wall in self.walls:
            board[wall[0]][wall[1]] = "#"
        
        print(tabulate(board, tablefmt="grid"))
         
class Player:
    def __init__(self):
        self.row = 0
        self.col = 0
        
    def move(self, direction, game):
        wall_north = False
        wall_east = False
        wall_south = False
        wall_west = False
        
        for wall in game.walls:
            if self.row == wall[0] and self.col == wall[1] - 1:
                wall_east = True
            if self.row == wall[0] and self.col == wall[1] + 1:
                wall_west = True
            if self.row == wall[0] - 1 and self.col == wall[1]:
                wall_south = True
            if self.row == wall[0] + 1 and self.col == wall[1]:
                wall_north = True
                
        if direction.startswith("u") and self.row > 0 and wall_north == False:
            self.row -= 1
        elif direction.startswith("d") and self.row < game.board_size - 1 and wall_south == False:
            self.row += 1
        elif direction.startswith("l") and self.col > 0 and wall_west == False:
            self.col -= 1
        elif direction.startswith("r") and self.col < game.board_size - 1 and wall_east == False:
            self.col += 1
        
def main():
    game = Dungeon()
    player = Player()
    game.print_board(player)
    
    while True:
        move = input("u d l r: ").lower()
        player.move(move, game)
        game.print_board(player)
        game.check_win(player)

if __name__ == "__main__":
    main()