import readchar
from tabulate import tabulate
import os
from items import Sword, Rifle

class Game:
    def action_instructions(self, player):
        print("(W) (A) (S) (D) to move", end="")
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