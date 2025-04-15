from tabulate import tabulate
import random
import time
import os

# choose to either move or active item on a turn
# sword: 
class Game:
    def player_action(self, player, board):
        print("(W) (A) (S) (D) to move", end="")
        if player.inventory:
            for i in range(len(player.inventory)):
                if isinstance(player.inventory[i], Sword) or isinstance(player.inventory[i], Revolver):
                    print(f" | ({i + 1}) for {player.inventory[i].name}", end="")
        print(": ", end="")

        try:
            while True:
                move = input().lower()
                if move == "w" or move == "a" or move == "s" or move == "d":
                    player.move(move, board)
                    break
                elif move == "1" or move == "2":
                    pass
                    break
                else:
                    print("Please input a proper move.")
                    continue
        except ValueError:
            print("Please play a move.")

class Dungeon:
    def __init__(self):
        self.board_rows = random.randint(6, 8)
        self.board_columns = random.randint(5, 7)
        self.exit_pos = [self.board_rows - 1, self.board_columns - 1]
        occupied_spaces = [[0, 0], self.exit_pos]
        
        # wall generation
        self.walls = []
        wall_origins = [[random.randint(1, self.board_rows - 2), random.randint(1, self.board_columns - 2)] for _ in range(int((self.board_rows * self.board_columns) ** 0.33))]
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
            if self.walls[i] == [0, 0] or self.walls[i] == [self.board_rows - 1, self.board_columns - 1]:
                self.walls.pop(i)
                
        # complete random wall generation
        #self.walls = [[random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)] for _ in range(((self.board_size ** 2) * 2) // 5)]
        #for i in range(len(self.walls) - 1):
        #    if self.walls[i] == [0, 0] or self.walls[i] == [self.board_size - 1, self.board_size - 1]:
        #        self.walls.pop(i)
        
        # treasure generation
        self.treasures = []
        treasure_choices = [1, 2, 3, 4]
        chosen_treasures = random.sample(treasure_choices, 3) # hard coded
        for treasure_type in chosen_treasures:
            while True:
                row = random.randint(0, self.board_rows - 1)
                col = random.randint(0, self.board_columns - 1)
            
                if [row, col] in occupied_spaces:
                    continue
                else:
                    break
            
            item_type = treasure_type
            self.treasures.append([row, col, item_type])
            occupied_spaces.append([row, col])
            
        # monster generation
        self.monsters = []
        num_monsters = 0
        while num_monsters < 3: # hard coded, adjust later
            row = random.randint(0, self.board_rows - 1)
            col = random.randint(0, self.board_columns - 1)
            
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
        if [player.col, player.row] == self.exit_pos:
            print("You win!")
            return True
        return False
        
    def print_board(self, player, turn):
        p_row, p_col = player.row, player.col
        board = [[" - " for _ in range(self.board_rows)] for _ in range(self.board_columns)]
        board[p_row][p_col] = "P"
        board[self.exit_pos[1]][self.exit_pos[0]] = "E"
        for wall in self.walls:
            board[wall[1]][wall[0]] = "#"
        for treasure in self.treasures:
            board[treasure[1]][treasure[0]] = "T"
        for monster in self.monsters:
            board[monster[1]][monster[0]] = "M"
        
        print(f" Turn: {turn} | Floor: {player.score} | Health: {player.health}")
        if player.inventory:
            print("---Inventory---")
            print(tabulate([[item.name for item in player.inventory]]))
        print(tabulate(board, tablefmt="grid"))
        
    def check_and_get_treasure(self, player):
        p_row, p_col = player.row, player.col
        for i in range(len(self.treasures)):
            if [p_col, p_row] == self.treasures[i][0:2]:
                if self.treasures[i][2] == 1:
                    item = Sword("Sword", "Kill monster on adjacent tile, ")
                elif self.treasures[i][2] == 2:
                    item = Revolver("Revolver", "Shoot a monster, 6 bullets")
                elif self.treasures[i][2] == 3:
                    item = Boots("Boots", "Move twice every third turn")
                else:
                    item = Armor("Armor", "Blocks one monster attack")
                
                player.add_to_inventory(item)
                self.treasures.pop(i)
                break
    
    def monster_move(self, player):
        p_row, p_col = player.row, player.col

        for monster in self.monsters:
            monster_col, monster_row = monster[0], monster[1]
            
            wall_north = False
            wall_east = False
            wall_south = False
            wall_west = False
            
            for wall in self.walls:
                if monster_row == wall[1] and monster_col == wall[0] - 1:
                    wall_east = True
                if monster_row == wall[1] and monster_col == wall[0] + 1:
                    wall_west = True
                if monster_row == wall[1] - 1 and monster_col == wall[0]:
                    wall_south = True
                if monster_row == wall[1] + 1 and monster_col == wall[0]:
                    wall_north = True
            
            print("###", wall_north, wall_east, wall_south, wall_west)
            # x and y distances from player
            # try to minimize the larger one if a wall isn't in the way
            # otherwise minize the other one if a wall isnt in the way
            # otherwise dont move
            
            row_distance = monster_row - p_row # + means monster is below player
            col_distance = monster_col - p_col # + means monster is right of player
            print("###", row_distance, col_distance, monster_row, monster_col, p_row, p_col)
            if abs(row_distance) >= abs(col_distance):
                print("###", "moving closer on row")
                if monster_row > p_row and wall_north == False and [monster[0] - 1, monster[1]] not in self.monsters:
                    monster[1] -= 1
                    print("this is running")
                elif monster_row < p_row and wall_south == False and [monster[0] + 1, monster[1]] not in self.monsters:
                    monster[1] += 1
                elif col_distance > 0 and wall_west == False and [monster[0], monster[1] - 1] not in self.monsters:
                    monster[0] -= 1
                elif col_distance < 0 and wall_east == False and [monster[0], monster[1] + 1] not in self.monsters:
                    monster[0] += 1
            elif abs(row_distance) < abs(col_distance):
                print("###", "moving closer on col")
                if monster_col > p_col and wall_west == False and [monster[0], monster[1] - 1] not in self.monsters:
                    monster[0] -= 1
                elif monster_col < p_col and wall_east == False and [monster[0], monster[1] + 1] not in self.monsters:
                    monster[0] += 1
                elif row_distance > 0 and wall_north == False and [monster[0] - 1, monster[1]] not in self.monsters:
                    monster[1] -= 1
                elif row_distance < 0 and wall_south == False and [monster[0] + 1, monster[1]] not in self.monsters:
                    monster[1] += 1
                    
        print("#", p_row, p_col, self.monsters)
    
    def check_monster_attack(self, player):
        p_row, p_col = player.row, player.col
        print("##", self.monsters, p_row, p_col)
        for i in range(len(self.monsters)):
            print(self.monsters[i][1], self.monsters[i][0])
            if self.monsters[i][1] == p_row and self.monsters[i][0] == p_col:
                print("&", "is this running?")
                player.health -= 1
                self.monsters.pop(i)
                break
                
                
class Player:
    def __init__(self):
        self.row = 0
        self.col = 0
        self.score = 1
        self.inventory = []
        self.health = 2
        
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
                    choice = int(input(f"(1) for {self.inventory[0]}, (2) for {self.inventory[1]}, (3) for {item} "))
                    if choice == 1:
                        self.inventory.pop(0)
                        self.inventory.append(item)
                        break
                    elif choice == 2:
                        self.inventory.pop(1)
                        self.inventory.append(item)
                        break
                    elif choice == 3:
                        break
                    else:
                        print("Please choose an item to discard.")
                        continue
            except ValueError:
                print("Please choose an item to discard.")
                
    def check_armor(self):
        if self.inventory:
            for item in self.inventory:
                if isinstance(item, Armor):
                    return True
        return False
                
    def check_boots(self):
        if self.inventory:
            for item in self.inventory:
                if isinstance(item, Boots):
                    return True
        return False
            
    # def view_inventory(self):
    #    if self.inventory:
    #        print(tabulate(self.inventory, tablefmt="grid"))
    #    else:
    #        print("Inventory empty.")
        
class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def __str__(self):
        return f"{self.name}: {self.description}"

class Sword(Item):
    pass

class Revolver(Item):
    pass

class Boots(Item):
    def __init__(self, name, description):
        super().__init__(name, description)
        self.active = True

    def activate_boots(player_turn, player):
        if player_turn % 3 == 1 and player.check_boots():
            for item in player.inventory:
                if isinstance(item, Boots):
                    item.active = True

    def use_boots(player_turn, player):
        if player_turn % 3 == 0 and player.check_boots():
            print("[Boots] passive: move again.")
            for item in player.inventory:
                if isinstance(item, Boots):
                    item.active = False
                    return True
        
        return False

class Armor(Item):
    pass

class Monster:
    pass

def main():
    level = 1
    player = Player()
    game = Game()
    
    while True: # while loop for game
        board = Dungeon()
        player_turn = 1 # accounts for boots passive
        game_turn = 1
        player_dead = False
        
        print(f"Entering floor {level}")
        player.row, player.col = 0, 0
        
        while True: # while loop for levels
            board.print_board(player, game_turn)
            # debug printing
            for item in player.inventory:
                print(str(item))
            print(player_turn, game_turn)
                
            # activate boots if the player turn is the next player turn)
            Boots.activate_boots(player_turn, player)

            game.player_action(player, board)
            
            board.check_and_get_treasure(player)
            
            if board.check_win(player):
                board.print_board(player, game_turn)
                break
            board

            # use boots if player turn is mult of 3 (player turn to be played on)
            if Boots.use_boots(player_turn, player):
                player_turn += 1
                continue
            
            if game_turn % 2 == 0:
                board.monster_move(player)
            
            board.check_monster_attack(player)
            if player.health == 0:
                player_dead = True
                break
            
            player_turn += 1
            game_turn += 1
            #os.system("cls")
            
        if player_dead:
            board.print_board(player, game_turn)
            print(f"You died on floor {level}...")
            break
        
        print(f"Floor {level} passed in {game_turn} moves!")
        player.score += 1
        level += 1

if __name__ == "__main__":
    main()