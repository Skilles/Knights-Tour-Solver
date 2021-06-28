# Supports up to 10 x 10 for now
import re

pos_list = []  # [x, y]
dimensions = ()  # (x, y)


class Pos:
    def __init__(self, x, y, possible_moves):
        self.x = x
        self.y = y
        self.possible_moves = possible_moves

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.possible_moves < other.possible_moves

    def __le__(self, other):
        return self.possible_moves <= other.possible_moves

    def __gt__(self, other):
        return self.possible_moves > other.possible_moves

    def __ge__(self, other):
        return self.possible_moves >= other.possible_moves

    def coordinates(self):
        return self.x, self.y


def do_error(type):
    if type == 1:
        print('Invalid dimensions!')
        set_dim()
    elif type == 0:
        print('Invalid position!')
        set_pos()
    else:
        print('Invalid move!')
        init()
        solve(False)
        # prompt_move()


def check_pos(list_):
    global main_board
    if len(list_) != 2:
        return False
    if list_[0] > dimensions[0] or list_[1] > dimensions[1] or list_[0] < 1 or list_[1] < 1:
        return False
    return True


def check_dimensions(list_):
    if len(list_) != 2:
        return False
    for pos in list_:
        if pos <= 0:
            return False
    return True


def set_dim():
    global dimensions
    print('Enter your board dimensions:')
    dim_input = input()
    try:
        dimensions = [int(char) for char in dim_input.split()]
        if not check_dimensions(dimensions):
            do_error(1)
    except ValueError:
        do_error(1)


def set_pos():
    global pos_list
    print("Enter the knight's starting position:")
    pos_input = input()
    try:
        pos_list = [int(char) for char in pos_input.split()]
        if not check_pos(pos_list):
            do_error(0)
    except ValueError:
        do_error(0)


def print_board(board):
    global x_space
    print(horizontal)
    output_str = ''
    for i in range(len(board), 0, -1):
        # print(count, '|', end='')
        indent = ''
        if double_space and len(str(i)) == 1:
            indent = ' '
        output_str += f'{indent}{i}| '
        for ccount, num in enumerate(board[i - 1]):
            # Checks if last cell
            if ccount == len(board[i - 1]) - 1:
                output_str += f'{num} |'
                # Checks if on the last row
                if i != 1:
                    output_str += '\n'
            else:
                output_str += f'{num} '
    print(output_str)
    print(horizontal)
    print(column_text)


def fill_board(board):
    board.clear()
    for i in range(0, dimensions[1]):
        board.append([])
    for i in range(0, dimensions[0]):
        for row in board:
            row.append(cell)


def format_board():
    global cell, space, column_text, x_space, horizontal, double_space
    # Indent if needed
    if double_space:
        horizontal += ' '
        column_text += ' '
    for i in range(0, len(str(dimensions[0] * dimensions[1]))):
        cell += '_'
        space += ' '
        if i != 0:
            x_space += ' '
    column_text += x_space
    for i in range(0, dimensions[0]):
        column_text += f'{i + 1}{space}'
    for i in range(0, dimensions[0] * (len(cell) + 1) + 3):
        horizontal += '-'


# pos = (x, y) with x being from 0 to dim - 1
def check_restraints(pos):
    pos = (pos[0] - 1, pos[1] - 1)
    if pos[1] >= dimensions[1] or pos[0] >= dimensions[0] or pos[0] < 0 or pos[1] < 0:
        return False
    else:
        return True


# Sets possible moves on the board
def set_possible_moves(pos, board):
    global possible_moves
    # (x, y) from 0, max_dim
    player_pos = (pos[0] - 1, pos[1] - 1)
    output = []
    # Sorts out bad moves
    can = 0
    for i in range(0, 8):
        pos = get_next_pos(i, player_pos)
        if is_valid_move((pos[0] + 1, pos[1] + 1)):
            can += 1
            av_moves = available_moves(pos)
            output.append(Pos(pos[0] + 1, pos[1] + 1, av_moves))
            board[pos[1]][pos[0]] = f'{x_space}{av_moves}'
            # possible_moves(pos, stage + 1)
    possible_moves = output
    if can == 0:
        if state != 'simulate':
            if state == 'solve':
                print_solution(board)
                exit()
            print_board(board)
            if visited == dimensions[0] * dimensions[1]:
                print('What a great tour! Congratulations!')
                exit()
            print('No more possible moves!')
            print(f'Your knight visited {visited} squares!')
            exit()


def available_moves(pos):
    player_pos = pos
    can = 0
    for i in range(0, 8):
        pos = get_next_pos(i, player_pos)
        if is_valid_move((pos[0] + 1, pos[1] + 1)):
            can += 1
    return can


def is_valid_move(pos):
    try:
        return check_restraints(pos) and main_board[pos[1] - 1][pos[0] - 1] != f'{x_space}*' and main_board[pos[1] - 1][
            pos[0] - 1] != f'{x_space}X'
    except IndexError:
        print(pos)


def get_next_pos(i, player_pos):
    if i == 0:
        pos = (player_pos[0] + 1, player_pos[1] + 2)
    elif i == 1:
        pos = (player_pos[0] - 1, player_pos[1] + 2)
    elif i == 2:
        pos = (player_pos[0] + 2, player_pos[1] + 1)
    elif i == 3:
        pos = (player_pos[0] + 2, player_pos[1] - 1)
    elif i == 4:
        pos = (player_pos[0] + 1, player_pos[1] - 2)
    elif i == 5:
        pos = (player_pos[0] - 1, player_pos[1] - 2)
    elif i == 6:
        pos = (player_pos[0] - 2, player_pos[1] - 1)
    elif i == 7:
        pos = (player_pos[0] - 2, player_pos[1] + 1)
    return pos


def move_player(pos, board):
    global visited, movements
    board[pos_list[1] - 1][pos_list[0] - 1] = f'{x_space}*'
    pos_list[0] = pos[0]
    pos_list[1] = pos[1]
    board[pos_list[1] - 1][pos_list[0] - 1] = f'{x_space}X'
    visited += 1
    movements[(pos_list[1] - 1, pos_list[0] - 1)] = visited
    reset_cells(board)
    set_possible_moves((pos_list[0], pos_list[1]), board)


def reset_cells(board):
    for row in range(0, dimensions[1]):
        for i in range(0, dimensions[0]):
            # TODO: check if X or O instead
            # any(char.isdigit() and not char == '*' for char in board[row][i])
            if regex.search(board[row][i]) is not None:
                board[row][i] = cell


def prompt_move():
    print('Enter your next move:')
    next_move = input().split()
    try:
        next_move = [int(x) for x in next_move]
    except ValueError:
        do_error(2)
    if not is_valid_move(next_move) or regex.search(main_board[next_move[1] - 1][next_move[0] - 1]) is None:
        do_error(2)
    else:
        move_player(next_move, main_board)
        print_board(main_board)
        prompt_move()


def check_solve():
    global state
    i = 0
    fail = True
    solve(True)
    for row in range(0, dimensions[1]):
        for col in range(0, dimensions[0]):
            i += 1
            if i != dimensions[0] * dimensions[1]:
                if movements.get((row, col)) is None:
                    return False
                fail = False
    if not fail:
        # Reset after simulation
        state = ''
        init()
        return True


def print_solution(board):
    i = 0
    for row in range(0, dimensions[1]):
        for col in range(0, dimensions[0]):
            i += 1
            if movements.get((row, col)) is None:
                print('No solution exists!')
                exit()
            if len(str(movements.get((row, col)))) > 1:
                board[row][col] = f'{movements.get((row, col))}'
            else:
                board[row][col] = f'{x_space}{movements.get((row, col))}'
    print("Here's the solution!")
    print_board(board)



def solve(simulation):
    global state
    state = 'solve'
    if simulation:
        state = 'simulate'
    set_possible_moves((pos_list[0], pos_list[1]), main_board)
    # Will exit when finished (if not simulation)
    while len(possible_moves) > 0:
        move_player(min(possible_moves).coordinates(), main_board)


def prompt_solve():
    print('Do you want to try the puzzle? (y/n):')
    answer = input()
    print()
    if answer == 'y':
        if not check_solve():
            print('No solution exists!')
            exit()
        prompt_move()
    elif answer == 'n':
        solve(False)
    else:
        print('Invalid input!')
        prompt_solve()


main_board = []
cell = ''
space = ''
x_space = ''
column_text = '   '
horizontal = ' '
double_space = False
visited = 1
regex = re.compile('\d')
possible_moves = []
movements = {}
state = ''

set_dim()

if len(str(dimensions[1])) > 1:
    double_space = True
# Fills the board and inits proper spacing variables
format_board()

# Get and set position
set_pos()

og_pos = pos_list[1] - 1, pos_list[0] - 1


def init():
    global double_space, x_space, visited, pos_list
    visited = 1

    # Get dimensions
    fill_board(main_board)

    # Set knight position in board
    pos_list = [og_pos[1] + 1, og_pos[0] + 1]
    movements.clear()
    main_board[og_pos[0]][og_pos[1]] = f'{x_space}X'
    movements[(og_pos[0], og_pos[1])] = 1
    set_possible_moves((og_pos[1] + 1, og_pos[0] + 1), main_board)


init()

# Prints and formats board
print_board(main_board)
prompt_solve()