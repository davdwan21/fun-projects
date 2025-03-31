# should i typecast move when i receive the input or when i use it
# should i look to write methods first or the raw code first?
# what are some things / tips i should look to do when first approaching a project with many steps

# todays tasks:
# - scalability - make the game applicable for any size board
# - handle input and edge cases
# - modularize - eliminate repetition with classes

divider = "---------"
game_size = 3 # functionally this works but it looks like dog water
tiles = game_size ** 2
game = [i + 1 for i in range(tiles)]
played_moves = set()
current_player = 0
win = -1

def print_board():
	for i in range(tiles):
		if (i % game_size != game_size - 1):
			print(f"{game[i]} | ", end="")
		else:
			print(f"{game[i]}", divider, sep="\n")

def check_win():
	win_condition = []

	# check horizontals
	for i in range(0, tiles, game_size):
		for j in range(i, i + game_size):
			win_condition.append(game[j])

		if len(set(win_condition)) == 1:
			return 0 if win_condition[0] == "X" else 1

		win_condition.clear()

	# check verticals
	for i in range(0, game_size):
		for j in range(i, tiles, game_size):
			win_condition.append(game[j])
		
		if len(set(win_condition)) == 1:
			return 0 if win_condition[0] == "X" else 1

		win_condition.clear()

	# diagonal 1
	for i in range(0, tiles, game_size + 1):
		win_condition.append(game[i])
	if len(set(win_condition)) == 1:
		return 0 if win_condition[0] == "X" else 1
	win_condition.clear()

	# diagonal 2
	for i in range(game_size - 1, tiles, game_size - 1):
		win_condition.append(game[i])
	if len(set(win_condition)) == 1:
		return 0 if win_condition[0] == "X" else 1
	win_condition.clear()

	# no winner
	return -1

def play_move(current_player):
	print(f"---PLAYER {current_player + 1}---")
	print_board()
	player_symbol = "X" if current_player == 0 else "O"

	while True:
		try:
			move = int(input("select a position to play in: "))
			if (move < 1) or (move > tiles) or (move in played_moves):
				print("please play a move within the board space that hasn't been played")
				continue
			break
		except ValueError:
			print("please enter a number for your move")
	
	game[move - 1] = player_symbol
	played_moves.add(move)

while True:
	play_move(current_player)
	win = check_win()

	if win != -1:
		break
	elif len(played_moves) == tiles:
		break

	current_player = 1 - current_player

if win == 0:
	print("player 1 wins!")
elif win == 1:
	print("player 2 wins!")
else:
	print("tie game")

print_board()