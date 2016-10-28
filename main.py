
# ------------------------------------------
# Authors: Jesse Simpson and Micahel Thomas
# ------------------------------------------

# ------------------------------------------
# File: main.py
# ------------------------------------------

def p_board(board, n):
	s = "+-" * n + "+\n"
	for item in board:
		s += "|"
		for i in item:
			s += ''.join(i) + "|"
		s += "\n" + "+-" * n + "+\n"

	print s

def initialize_board(board, n):
	board[(n/2) - 1][(n/2)-1] = "B"
	board[(n/2)][(n/2)] = "B"
	board[(n/2) - 1][(n/2)] = "W"
	board[(n/2)][(n/2-1)] = "W"
	return board
	


def main():
	n = input()
	x = []
	for i in range(n):
		y = [' '] * n
		x.append(y)
	y = initialize_board(x, n)
	p_board(y, n)

if __name__ == "__main__":
    main()