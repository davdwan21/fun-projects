import random
from tabulate import tabulate
from colorama import Fore
from entities import Monster
from items import Sword, Rifle, Armor, Boots
from a_star import a_star_search

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
        chosen_treasures = random.sample(treasure_choices, 3)
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
        for i in range(len(self.monsters) - 1, -1, -1):
            if self.monsters[i].col == p_row and self.monsters[i].row == p_col:
                armor_slot = player.check_armor()
                if armor_slot >= 0:
                    player.inventory.pop(armor_slot)
                    self.monsters.pop(i)
                    damage_blocked = True
                    continue

                player.health -= 1
                self.monsters.pop(i)

        return damage_blocked
    
def possible_board(board):
    board_vis = [["-" for _ in range(board.board_rows)] for _ in range(board.board_columns)]
    
    for wall in board.walls:
        board_vis[wall[1]][wall[0]] = "#" # apparently walls are also switched row, col --> col, row

    return a_star_search(board_vis, [0, 0], board.exit_pos)