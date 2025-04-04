from tabulate import tabulate
import random
import time
import os

# current ideas:
# see how many levels you can get through (each level is a dungeon)
# various items, you can only hold 2 at once though
# actives
# sword: kill a monster if you are on an adjacent square
# gun: kill a monster if you have x y LOS, only has 6 bullets though
# passives
# boots: move twice every turn
# armor: increases health by 1 (originally 2, now 3)

class Dungeon:
    def __init__(self):
        self.board_size = 7
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
        
        # treasure generation
        self.treasures = []
        num_treasures = 0
        while num_treasures < 3: # hard coded, adjust later
            row = random.randint(0, self.board_size - 1)
            col = random.randint(0, self.board_size - 1)
            
            if [row, col] in occupied_spaces:
                continue
            
            item_type = random.randint(1, 4)
            self.treasures.append([row, col, item_type])
            occupied_spaces.append([row, col])
            num_treasures += 1
            
        # monster generation
        self.monsters = []
        num_monsters = 0
        while num_monsters < 3: # hard coded, adjust later
            row = random.randint(0, self.board_size - 1)
            col = random.randint(0, self.board_size - 1)
            
            if [row, col] in occupied_spaces:
                continue
            
            self.monsters.append([row, col])
            occupied_spaces.append([row, col])
            num_monsters += 1
        
        print(occupied_spaces)
        print(self.walls)
        print(self.treasures)
        print(self.monsters)
        
    def check_win(self, player):
        if [player.row, player.col] == self.exit_pos:
            print("you win!")
            return True
        return False
        
    def print_board(self, player, turn):
        p_row, p_col = player.row, player.col
        board = [[" - " for _ in range(self.board_size)] for _ in range(self.board_size)]
        board[p_row][p_col] = "P"
        board[self.exit_pos[0]][self.exit_pos[1]] = "E"
        for wall in self.walls:
            board[wall[0]][wall[1]] = "#"
        for treasure in self.treasures:
            board[treasure[0]][treasure[1]] = "T"
        for monster in self.monsters:
            board[monster[0]][monster[1]] = "M"
        
        print(f"Score: {player.score} | Turn: {turn}")
        print(tabulate(board, tablefmt="grid"))
        
    def check_treasure(self, player):
        p_row, p_col = player.row, player.col
        for i in range(len(self.treasures)):
            if [p_row, p_col] == self.treasures[i][0:2]:
                if self.treasures[2] == 1:
                    item = Sword("Sword", "Kill monster on adjacent tile")
                elif self.treasures[2] == 2:
                    item = Revolver("Revolver", "Shoot a monster, 6 bullets")
                elif self.treasures[2] == 3:
                    item = Boots("Boots", "Move twice per turn")
                else:
                    item = Armor("Armor", "One extra health per level")
                
                player.add_to_inventory(item)
                print(f"You got [{item.name}]! Description: {item.description}")
                self.treasures.pop(i)
                break
         
class Player:
    def __init__(self):
        self.row = 0
        self.col = 0
        self.score = 0
        self.inventory = []
        self.health = 2
        
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
            
    def add_to_inventory(self, item):
        if len(self.inventory) < 2:
            self.inventory.append(item)
            
    def view_inventory(self):
        if self.inventory:
            print(tabulate(self.inventory, tablefmt="grid"))
        else:
            print("Inventory empty.")
        
class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def __str__(self):
        return f"{self.name} + {self.description}"

class Sword(Item):
    pass

class Revolver(Item):
    pass

class Boots(Item):
    pass

class Armor(Item):
    pass

class Monster:
    pass

def main():
    game = Dungeon()
    player = Player()
    turn = 1
    
    while True: # each iteration should be a "turn"
        game.print_board(player, turn)
        # debug printing
        for item in player.inventory:
            print(str(item))
            
        try:
            while True:
                move = input("(W) (A) (S) (D) to move or (I) for inventory: ").lower()
                if move == "i":
                    player.view_inventory()
                elif move == "w" or move == "a" or move == "s" or move == "d":
                    player.move(move, game)
                    break
                else:
                    print("Please input a proper move.")
                    continue
        except ValueError:
            print("Please play a move.")
        
        game.check_treasure(player)
        if game.check_win(player):
            game.print_board(player)
            break
        
        turn += 1
        #os.system("cls")

if __name__ == "__main__":
    main()