import readchar
from items import Sword, Rifle, Armor, Boots

class Player:
    def __init__(self):
        self.row = 0
        self.col = 0
        self.score = 1
        self.inventory = []
        self.health = 2
        self.monsters_killed = 0
        
    def move(self, direction, game):
        wall_north = False
        wall_east = False
        wall_south = False
        wall_west = False
        
        for wall in game.walls:
            if self.row == wall[1] and self.col == wall[0] - 1:
                wall_east = True
            if self.row == wall[1] and self.col == wall[0] + 1:
                wall_west = True
            if self.row == wall[1] - 1 and self.col == wall[0]:
                wall_south = True
            if self.row == wall[1] + 1 and self.col == wall[0]:
                wall_north = True
        
        if direction.startswith("w") and self.row > 0 and wall_north == False:
            self.row -= 1
        elif direction.startswith("s") and self.row < game.board_columns - 1 and wall_south == False:
            self.row += 1
        elif direction.startswith("a") and self.col > 0 and wall_west == False:
            self.col -= 1
        elif direction.startswith("d") and self.col < game.board_rows - 1 and wall_east == False:
            self.col += 1
            
    def add_to_inventory(self, item):
        if len(self.inventory) < 2:
            self.inventory.append(item)
            print(f"You got [{item.name}]! Description: {item.description}")
        else:
            print(f"You found [{item.name}]! Description: {item.description}")
            print("Inventory full! Choose an item to drop: ")
            try:
                while True:
                    print(f"(1) for {self.inventory[0]}, (2) for {self.inventory[1]}, (3) for {item} ")
                    choice = readchar.readkey()
                    if choice == "1":
                        self.inventory.pop(0)
                        self.inventory.append(item)
                        break
                    elif choice == "2":
                        self.inventory.pop(1)
                        self.inventory.append(item)
                        break
                    elif choice == "3":
                        break
                    else:
                        print("Please choose an item to discard.")
                        continue
            except ValueError:
                print("Please choose an item to discard.")
                
    def check_armor(self):
        if self.inventory:
            for i in range(len(self.inventory)):
                if isinstance(self.inventory[i], Armor):
                    return i
        return -1
                
    def check_boots(self):
        if self.inventory:
            for item in self.inventory:
                if isinstance(item, Boots):
                    return True
        return False
    
    def use_item(self, item, board, player):
        if isinstance(item, Sword):
            print("(W) (A) (S) (D) direction to slash: ", end="")
            item.slash(board, player)
        elif isinstance(item, Rifle):
            print("(W) (A) (S) (D) direction to shoot: ", end="")
            item.shoot(board, player)
            
    # backdoor for debugging - get to later floors
    def backdoor(self, board):
        self.row = board.board_rows - 1
        self.col = board.board_columns - 1

class Monster:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    # monster movement is accidentally switched row, col --> col, row
    def move(self, player, board):
        p_row, p_col = player.row, player.col

        monster_col, monster_row = self.row, self.col
        
        wall_north = False
        wall_east = False
        wall_south = False
        wall_west = False
        
        for wall in board.walls:
            if monster_row == wall[1] and monster_col == wall[0] - 1:
                wall_east = True
            if monster_row == wall[1] and monster_col == wall[0] + 1:
                wall_west = True
            if monster_row == wall[1] - 1 and monster_col == wall[0]:
                wall_south = True
            if monster_row == wall[1] + 1 and monster_col == wall[0]:
                wall_north = True
        
        # x and y distances from player
        # try to minimize the larger one if a wall isn't in the way
        # otherwise minize the other one if a wall isnt in the way
        # otherwise dont move
        
        row_distance = monster_row - p_row # + means monster is below player
        col_distance = monster_col - p_col # + means monster is right of player
        if abs(row_distance) >= abs(col_distance):
            if monster_row > p_row and wall_north == False and [self.row - 1, self.col] not in board.monsters:
                self.col -= 1
            elif monster_row < p_row and wall_south == False and [self.row + 1, self.col] not in board.monsters:
                self.col += 1
            elif col_distance > 0 and wall_west == False and [self.row, self.col - 1] not in board.monsters:
                self.row -= 1
            elif col_distance < 0 and wall_east == False and [self.row, self.col + 1] not in board.monsters:
                self.row += 1
        elif abs(row_distance) < abs(col_distance):
            if monster_col > p_col and wall_west == False and [self.row, self.col - 1] not in board.monsters:
                self.row -= 1
            elif monster_col < p_col and wall_east == False and [self.row, self.col + 1] not in board.monsters:
                self.row += 1
            elif row_distance > 0 and wall_north == False and [self.row - 1, self.col] not in board.monsters:
                self.col -= 1
            elif row_distance < 0 and wall_south == False and [self.row + 1, self.col] not in board.monsters:
                self.col += 1