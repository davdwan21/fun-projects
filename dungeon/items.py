import readchar

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