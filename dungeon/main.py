from game import Game
from entities import Player
from dungeon_logic import Dungeon, possible_board
from items import Boots, Sword, Rifle
import os

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
                    
                # activate boots if the player turn is the next player turn)
                Boots.activate_boots(player_turn, player)

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
                
                # check if items are out of out of use
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