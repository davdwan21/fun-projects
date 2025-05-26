from tabulate import tabulate
import random
import time
import os
from a_star import a_star_search
from colorama import Fore
import readchar

# choose to either move or active item on a turn
# sword: on turn, choose to use sword + slash in a certain direction.

# WHY THE FRICK ARE ENEMIES IMMUNE TO RIFLES RANDOMLY
class Game:
    def action_instructions(self, player):
        print("(W) (A) (S) (D) to move (what the frick)", end="")
        if player.inventory:
            for i in range(len(player.inventory)):
                if isinstance(player.inventory[i], Sword) or isinstance(player.inventory[i], Rifle):
                    print(f" | ({i + 1}) for {player.inventory[i].name}", end="")
        print(": ", end="")

    def player_action(self, player, board):
        try:
            while True:
                move = readchar.readkey()

                if move == "w" or move == "a" or move == "s" or move == "d":
                    player.move(move, board)
                    break
                elif move == "1" or move == "2":
                    if player.inventory:
                        item = player.inventory[int(move) - 1]
                        print("why isnt this running")
                        player.use_item(item, board, player)
                    else:
                        print("Please input a proper move.")
                    continue
                elif move == "/":
                    player.backdoor(board)
                    break
                else:
                    print("Please input a proper move.")
                    continue
        except ValueError:
            print("Please play a move.")

    def main_menu(self):
        while True:
            try:
                print("--basic dungeon crawler--")
                print(tabulate([["PLAY", "HOW TO PLAY", "EXIT"]]))
                
                user = input("Type to (P)lay, (H)ow to Play, or (E)xit.\n")
                print(user.lower()[0])
                if user.lower()[0] == "p":
                    break
                elif user.lower()[0] == "e":
                    exit()
                elif user.lower()[0] == "h":
                    os.system("clear")
                    print("---HOW TO PLAY---")
                    print(tabulate([["P", " The [P]layer: you move with (W) (A) (S) (D) and use items with (1) (2)"],
                                    ["E", " Get to the [E]xit for each floor"],
                                    ["#", " Walls block player and enemy movement"],
                                    ["-", " Empty Spaces"],
                                    ["M", " [M]onsters move towards the player and damage you on contact"],
                                    ["T", " [T]reasures contain useful items in your journey"]], tablefmt="grid"))
                    input("Press any button to continue.\n")
                else:
                    print("Please make a valid input")
            except Exception:
                print("Please make a valid input")
        os.system("clear")

class Dungeon:
    def __init__(self, level_num):
        self.level_num = level_num
        self.board_rows = random.randint(6, 8)
        self.board_columns = random.randint(5, 7)
        self.exit_pos = [self.board_rows - 1, self.board_columns - 1]
        occupied_spaces = [[0, 0], self.exit_pos]
        self.infested = False
        self.blood_moon = False

        # blood moon floor takes precedence
        if (self.level_num % 10 > 6) and (self.level_num % 10 < 10):
            if random.randint(1, 3) == 1:
                self.blood_moon = True
        # infested and blood moon cannot happen simultaneously
        elif (self.level_num % 10 > 2) and (self.level_num % 10 < 10):
            if random.randint(1, 4) == 1:
                self.infested = True
        
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
        # print(self.walls)
            
        # prevent the exit or player from being replaced by a wall
        for i in range(len(self.walls) - 1):
            if self.walls[i] == [0, 0] or self.walls[i] == [self.board_rows - 1, self.board_columns - 1]:
                self.walls.pop(i)
                
        # completely random wall generation
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
        max_monsters = 3 + (level_num // 5)
        if self.infested:
            max_monsters += 2
        
        while num_monsters < max_monsters:
            row = random.randint(0, self.board_rows - 1)
            col = random.randint(0, self.board_columns - 1)
            
            if [row, col] in occupied_spaces:
                continue
            
            monster = Monster(row, col)
            self.monsters.append(monster)
            occupied_spaces.append([row, col])
            num_monsters += 1
        
        # print(occupied_spaces)
        # print(self.walls)
        # print(self.treasures)
        # print(self.monsters)
        
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
            board[monster.col][monster.row] = "M"
        
        print(f" Turn: {turn} | Floor: {player.score} | Health: {player.health}")
        if player.inventory:
            print("---Inventory---")
            item_list = []
            for item in player.inventory:
                item_name = item.name
                if isinstance(item, Rifle):
                    item_name += f": {item.ammo} ||"
                elif isinstance(item, Sword):
                    item_name += f": {item.durability} //"
                item_list.append(item_name)
            print(tabulate([item_list]))
        
        if self.infested:
            print(Fore.GREEN + "This floor is infested... (Extra monsters)")
        elif self.blood_moon:
            print(Fore.RED + "The blood moon rises... (Monsters move faster)")

        print(tabulate(board, tablefmt="grid"))
        print(Fore.RESET)
        
    def check_and_get_treasure(self, player):
        p_row, p_col = player.row, player.col
        for i in range(len(self.treasures)):
            if [p_col, p_row] == self.treasures[i][0:2]:
                if self.treasures[i][2] == 1:
                    durability = random.randint(6, 8)
                    item = Sword("Sword", "Kill monsters on adjacent tiles", durability)
                elif self.treasures[i][2] == 2:
                    ammo = random.randint(2, 3)
                    item = Rifle("Rifle", f"Shoot monsters with {ammo} piercing bullets", ammo)
                elif self.treasures[i][2] == 3:
                    item = Boots("Boots", "Move twice every third turn")
                else:
                    item = Armor("Armor", "Blocks one monster attack")
                
                player.add_to_inventory(item)
                self.treasures.pop(i)
                break
    
    def check_monster_attack(self, player):
        damage_blocked = False

        p_row, p_col = player.row, player.col
        # print("##", self.monsters, p_row, p_col)
        for i in range(len(self.monsters) - 1, -1, -1):
            if self.monsters[i].col == p_row and self.monsters[i].row == p_col:
                # print("&", "is this running?")

                armor_slot = player.check_armor()
                if armor_slot >= 0:
                    player.inventory.pop(armor_slot)
                    self.monsters.pop(i)
                    damage_blocked = True
                    continue

                player.health -= 1
                self.monsters.pop(i)

        return damage_blocked
                     
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
    def __init__(self, name, description, durability):
        super().__init__(name, description)
        self.durability = durability

    def slash(self, board, player):
        self.durability -= 1
        p_row, p_col = player.row, player.col
        try:
            while True:
                direction = readchar.readkey()
                if direction == "w":
                    attacked_square = [p_row - 1, p_col]
                    break
                elif direction == "a":
                    attacked_square = [p_row, p_col - 1]
                    break
                elif direction == "s":
                    attacked_square = [p_row + 1, p_col]
                    break
                elif direction == "d":
                    attacked_square = [p_row, p_col + 1]
                    break
                else:
                    print("Improper direction.")
                    continue

            print(f"You slash in the direction: ({direction.upper()})")
            # attack phase
            i = len(board.monsters) - 1
            while i >= 0:
                if [board.monsters[i].col, board.monsters[i].row] == attacked_square:
                    print("Monster slashed!")
                    player.monsters_killed += 1
                    board.monsters.pop(i)
                i -= 1
        except ValueError:
            print("Please input a direction.")

class Rifle(Item):
    def __init__(self, name, description, ammo):
        super().__init__(name, description)
        self.ammo = ammo
        
    def shoot(self, board, player):
        self.ammo -= 1
        p_row, p_col = player.row, player.col
        try:
            while True:
                print("(W) (A) (S) (D) direction to fire: ", end="")
                direction = readchar.readkey()
                if direction == "w":
                    attack_squares = [[p_row - i, p_col] for i in range(1, p_row)]
                    break
                elif direction == "a":
                    attack_squares = [[p_row, p_col - i] for i in range(1, p_col)]
                    break
                elif direction == "s":
                    attack_squares = [[p_row + i, p_col] for i in range(1, board.board_rows - p_row)]
                    break
                elif direction == "d":
                    attack_squares = [[p_row, p_col + i] for i in range(1, board.board_columns - p_col)]
                    break
                else:
                    print("Improper direction.")
                    continue
                
            print(f"You shoot in the direction ({direction})")
            for square in attack_squares:
                i = len(board.monsters) - 1
                while i >= 0:
                    if [board.monsters[i].col, board.monsters[i].row] == square:
                        print("Monster shot!")
                        player.monsters_killed += 1
                        board.monsters.pop(i)
                    i -= 1
        except ValueError:
            print("Please input a direction.")

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
            for item in player.inventory:
                if isinstance(item, Boots):
                    item.active = False
                    return True
        
        return False

class Armor(Item):
    pass

class Monster:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    # monster movement is switched row, col --> col, row
    def move(self, player, board):
        p_row, p_col = player.row, player.col

        # why the frick?
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
        
        # print("###", wall_north, wall_east, wall_south, wall_west)
        # x and y distances from player
        # try to minimize the larger one if a wall isn't in the way
        # otherwise minize the other one if a wall isnt in the way
        # otherwise dont move
        
        row_distance = monster_row - p_row # + means monster is below player
        col_distance = monster_col - p_col # + means monster is right of player
        # print("###", row_distance, col_distance, monster_row, monster_col, p_row, p_col)
        if abs(row_distance) >= abs(col_distance):
            # print("###", "moving closer on row")
            if monster_row > p_row and wall_north == False and [self.row - 1, self.col] not in board.monsters:
                self.col -= 1
                # print("this is running")
            elif monster_row < p_row and wall_south == False and [self.row + 1, self.col] not in board.monsters:
                self.col += 1
            elif col_distance > 0 and wall_west == False and [self.row, self.col - 1] not in board.monsters:
                self.row -= 1
            elif col_distance < 0 and wall_east == False and [self.row, self.col + 1] not in board.monsters:
                self.row += 1
        elif abs(row_distance) < abs(col_distance):
            # print("###", "moving closer on col")
            if monster_col > p_col and wall_west == False and [self.row, self.col - 1] not in board.monsters:
                self.row -= 1
            elif monster_col < p_col and wall_east == False and [self.row, self.col + 1] not in board.monsters:
                self.row += 1
            elif row_distance > 0 and wall_north == False and [self.row - 1, self.col] not in board.monsters:
                self.col -= 1
            elif row_distance < 0 and wall_south == False and [self.row + 1, self.col] not in board.monsters:
                self.col += 1

# board is of type dungeon
def possible_board(board):
    board_vis = [["-" for _ in range(board.board_rows)] for _ in range(board.board_columns)]
    
    for wall in board.walls:
        board_vis[wall[1]][wall[0]] = "#" # WHY IS MY GAME COOKED
        
    # print(tabulate(board_vis, tablefmt="grid"))

    return a_star_search(board_vis, [0, 0], board.exit_pos)
    
def main():
    game = Game()
    
    while True: # while loop for the game itself
        game.main_menu()
        player = Player()
        level = 1

        while True: # while loop for gameplay
            while True:
                board = Dungeon(level)
                if possible_board(board):
                    # print("board is solvable")
                    break
                
            player_turn = 1 # accounts for boots passive
            game_turn = 1
            player_dead = False
            
            print(f"Entering floor {level}")
            player.row, player.col = 0, 0

            damage_blocked = False
            rifle_dropped = False
            sword_broke = False
            while True: # while loop for levels
                # print("#####")
                if damage_blocked:
                    print("[Armor] passive: damage blocked!")
                    damage_blocked = False
                if rifle_dropped:
                    print("[Rifle] out of bullets.")
                    rifle_dropped = False
                if sword_broke:
                    print("[Sword] broke.")
                    sword_broke = False

                board.print_board(player, game_turn)
                # debug printing
                # for item in player.inventory:
                #    print(str(item))
                # print(player_turn, game_turn)
                    
                # activate boots if the player turn is the next player turn)
                Boots.activate_boots(player_turn, player)

                # print("wrap")
                game.action_instructions(player)
                print()
                game.player_action(player, board)
                
                board.check_and_get_treasure(player)
                
                if board.check_win(player):
                    board.print_board(player, game_turn)
                    break
                board

                # use boots if player turn is mult of 3 (player turn to be played on)
                if Boots.use_boots(player_turn, player):
                    player_turn += 1
                    os.system("clear")
                    print("[Boots] passive: move again")
                    continue
                
                if (game_turn % 2 == 0) and (board.blood_moon == False):
                    for monster in board.monsters:
                        monster.move(player, board)
                elif board.blood_moon == True:
                    for monster in board.monsters:
                        monster.move(player, board)
                
                damage_blocked = board.check_monster_attack(player)
                
                if player.health <= 0:
                    player_dead = True
                    break
                
                # check if items are broken
                i = len(player.inventory) - 1
                while i >= 0:
                    if isinstance(player.inventory[i], Rifle):
                        if player.inventory[i].ammo <= 0:
                            player.inventory.pop(i)
                            rifle_dropped = True
                            break
                    if isinstance(player.inventory[i], Sword):
                        if player.inventory[i].durability <= 0:
                            player.inventory.pop(i)
                            sword_broke = True
                            break
                    i -= 1
                
                player_turn += 1
                game_turn += 1
                os.system("clear")
                # print("#")
                
            if player_dead:
                board.print_board(player, game_turn)
                print(f"You died on floor {level}...")
                print(f"Monsters slain: {player.monsters_killed}")
                input("Press [ENTER] to continue\n")
                os.system("clear")
                break
            
            print(f"Floor {level} passed in {game_turn} moves!")
            player.score += 1
            level += 1

            os.system("clear")

if __name__ == "__main__":
    main()