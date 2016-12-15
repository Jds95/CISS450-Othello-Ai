
# ------------------------------------------
# Authors: Jesse Simpson and Micahel Thomas
# ------------------------------------------

# ------------------------------------------
# File: main.py
# ------------------------------------------

import random

# 100 points for corner move, 2 points for side (20 for side if you have corner, 
# 1 point if no corner), 1 point per flip 

# Corner spots are [0, 0], [n-1, 0], [0, n-1], [n-1,n-1]
# Note: Dictionary Keys are in form of (x, y) not [x, y]
# Data associated with keys are list of [x,y] to flip if move is made



def out_of_range_check(x, y, n):
	# Check if x or y is less than 0 or greater than the board n
	if x < 0 or y < 0 or x >= n or y >= n:
		return True
	else:
		return False

def valid_move_check(board, piece, xs, ys, n):
	# Place piece to test
	board[xs][ys] = piece
	if piece == 'B':
		other_piece = 'W'
	else:
		other_piece = 'B'

	# List to hold pieces to flip
	flip = []
	# Loop to Check NSEW Diagonals
	for xdir, ydir in [[0,1], [1,1], [1,0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
		x, y = xs, ys
		x += xdir
		y += ydir
		# If [x][y] are out of scope, test next direciton
		if out_of_range_check(x, y, n):
			continue
		# Goes into while loop if piece besides it is opposite piece
		while board[x][y] == other_piece:
			x += xdir
			y += ydir
			# If it leaves scope, break
			if out_of_range_check(x, y, n):
				break

		if out_of_range_check(x, y, n):
			continue
		# This point we know we have valid move, back track pieces to swap
		if board[x][y] == piece:
			while True:
				x -= xdir
				y -= ydir
				if x == xs and y == ys:
					break
				# Add to list of pieces to be swapped
				flip.append([x,y])

	#Put Space back onto board for [x][y] we checked
	board[xs][ys] = ' '

	# If no pieces to flip, invalid move
	if len(flip) == 0:
		return (False, flip)

	# Return True, list of x, y coordinates to flip
	return (True, flip)


def get_move(board_size, board_state, turn, time_left, oppenent_time_left):
	moves = {}
	for i in range(board_size):
		for l in range(board_size):
			if board_state[i][l] != ' ':
				continue
			y = valid_move_check(board_state, turn, i, l, board_size)
			if y[0] == True:
				# Append to moves the [x,y] of move and y[1] which is list of all pieces to flip.
				moves[(i, l)] = y[1]
	m = None
	for key in moves.keys():
		if (key == (0, 0) or key == (0, board_size-1) or key == (board_size-1, board_size-1) or key == (board_size-1, 0)):
			return list(key)
		if len(moves[key]) > m:
			m = list(key)
	return m

# def p_board(board, n):
# 	s = "+-" * n + "+\n"
# 	for item in board:
# 		s += "|"
# 		for i in item:
# 			s += ''.join(i) + "|"
# 		s += "\n" + "+-" * n + "+\n"

# 	print s

# def initialize_board(board, n):
# 	board[(n/2) - 1][(n/2)-1] = "B"
# 	board[(n/2)][(n/2)] = "B"
# 	board[(n/2) - 1][(n/2)] = "W"
# 	board[(n/2)][(n/2-1)] = "W"
# 	return board

# def main():
# 	n = input()
# 	x = []
# 	for i in range(n):
# 		y = [' '] * n
# 		x.append(y)
# 	y = initialize_board(x, n)
# 	p_board(y, n)
# 	get_move(n, y, 'B', 10000, 10000)

# if __name__ == "__main__":
#     main()