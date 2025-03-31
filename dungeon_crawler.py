from tabulate import tabulate
import random
import time
import os

# fun idea: roll some dice for player movement, attack, etc. and force them to choose
class Dungeon:
    def __init__(self):
        self.board_size = 5
        self.exit_pos = [self.board_size - 1, self.board_size - 1]
        occupied_spaces = [[0, 0], self.exit_pos]
        
        # wall generation
        self.walls = []
        wall_origins = [[random.randint(1, self.board_size - 2), random.randint(1, self.board_size - 2)] for _ in range(self.board_size // 2)]
        for origin in wall_origins:
            directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
            extra_walls = random.sample(directions, random.randint(1, 2)) # extra_walls is hardcoded for size 5
            for extra in extra_walls:
                new_wall = [row + col for row, col in zip(origin, extra)]
                self.walls.append(new_wall)
                occupied_spaces.append(new_wall)
        for wall in wall_origins:
            self.walls.append(wall)
            occupied_spaces.append(wall)
            
        # prevent the exit or player from being replaced by a wall
        for i in range(len(self.walls) - 1):
            if self.walls[i] == [0, 0] or self.walls[i] == [self.board_size - 1, self.board_size - 1]:
                self.walls.pop(i)
                
        # complete random wall generation
        #self.walls = [[random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)] for _ in range(((self.board_size ** 2) * 2) // 5)]
        #for i in range(len(self.walls) - 1):
        #    if self.walls[i] == [0, 0] or self.walls[i] == [self.board_size - 1, self.board_size - 1]:
        #        self.walls.pop(i)
        
        self.treasures = []
        num_treasures = 0
        while True:
            row = random.randint(0, self.board_size - 1)
            col = random.randint(0, self.board_size - 1)
            
            if [row, col] in occupied_spaces:
                continue
            
            self.treasures.append([row, col])
            occupied_spaces.append([row, col])
            num_treasures += 1
            
            if num_treasures == 2: # currently hard coded for size 5
                break
            
        print(occupied_spaces)
        print(self.walls)
        print(self.treasures)
        
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
        for treasure in self.treasures:
            board[treasure[0]][treasure[1]] = "T"
        
        print(f"Score: {player.score}")
        print(tabulate(board, tablefmt="grid"))
        
    def check_treasure(self, player):
        p_row, p_col = player.row, player.col
        for i in range(len(self.treasures)):
            if [p_row, p_col] == self.treasures[i]:
                player.score += 1
                self.treasures.pop(i)
         
class Player:
    def __init__(self):
        self.row = 0
        self.col = 0
        self.score = 0
        
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
                
        if direction.startswith("w") and self.row > 0 and wall_north == False:
            self.row -= 1
        elif direction.startswith("s") and self.row < game.board_size - 1 and wall_south == False:
            self.row += 1
        elif direction.startswith("a") and self.col > 0 and wall_west == False:
            self.col -= 1
        elif direction.startswith("d") and self.col < game.board_size - 1 and wall_east == False:
            self.col += 1
        
def main():
    game = Dungeon()
    player = Player()
    
    while True:
        game.print_board(player)
        move = input("wasd: ").lower()
        player.move(move, game)
        
        game.check_treasure(player)
        if game.check_win(player):
            game.print_board(player)
            break
        
        #os.system("cls")

if __name__ == "__main__":
    main()