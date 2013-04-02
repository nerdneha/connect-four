import connect_four
import pprint

ROWS = 5
COLUMNS = 3

MAX = 1
MIN = 2

BLANK_BOARD = [[0 for i in range(COLUMNS)] for j in range(ROWS)]
def make_sample_board(b):
    r = ROWS
    b[connect_four.get_row(b,1,ROWS)][1] = MAX
    b[connect_four.get_row(b,0,ROWS)][0] = MIN
    b[connect_four.get_row(b,1,ROWS)][1] = MAX
    b[connect_four.get_row(b,1,ROWS)][1] = MIN
    return b

def add_player_to_board(b, player):
    boards = []
    for i in range(COLUMNS):
        new_b = [row[:] for row in b]
        row = connect_four.get_row(b, i, ROWS)
        if row != None:
            new_b[connect_four.get_row(b, i, ROWS)][i] = player
            boards.append(new_b[:])
    return boards

def is_board(board):
    for row in board:
        for column in row:
            if type(column) == type(0):
                return True
    return False



def recur_add_player(boards, player):
    if is_board(boards):
        return add_player_to_board(boards, player)
    else:
        all_the_boards = []
        for b in boards:
            next_iter_boards = recur_add_player(b, player)
            all_the_boards.append(next_iter_boards[:])
        return all_the_boards



def test_max(board, num):
    print
    print "MAX", num
    max_1 = recur_add_player(board, MAX)
    for item in max_1:
        pp.pprint(item)
        print
    return max_1

def test_min(board, num):
    print
    print "MIN", num
    min_1 = recur_add_player(board, MIN)
    for item in min_1:
        pp.pprint(item)
        print
    return min_1

max_1_SOLUTION = [
     [[0, 0, 0], [0, 0, 0], [0, 2, 0], [1, 1, 0], [2, 1, 0]],
     [[0, 0, 0], [0, 1, 0], [0, 2, 0], [0, 1, 0], [2, 1, 0]],
     [[0, 0, 0], [0, 0, 0], [0, 2, 0], [0, 1, 0], [2, 1, 1]]]


min_1_SOLUTION = [
    [[[0, 0, 0], [0, 0, 0], [2, 2, 0], [1, 1, 0], [2, 1, 0]],
     [[0, 0, 0], [0, 2, 0], [0, 2, 0], [1, 1, 0], [2, 1, 0]],
     [[0, 0, 0], [0, 0, 0], [0, 2, 0], [1, 1, 0], [2, 1, 2]]],

    [[[0, 0, 0], [0, 1, 0], [0, 2, 0], [2, 1, 0], [2, 1, 0]],
     [[0, 2, 0], [0, 1, 0], [0, 2, 0], [0, 1, 0], [2, 1, 0]],
     [[0, 0, 0], [0, 1, 0], [0, 2, 0], [0, 1, 0], [2, 1, 2]]],

    [[[0, 0, 0], [0, 0, 0], [0, 2, 0], [2, 1, 0], [2, 1, 1]],
     [[0, 0, 0], [0, 2, 0], [0, 2, 0], [0, 1, 0], [2, 1, 1]],
     [[0, 0, 0], [0, 0, 0], [0, 2, 0], [0, 1, 2], [2, 1, 1]]]]

def play_board(board, depth):
    for i in range(depth):
        max_board = recur_add_player(board, MAX)
        min_board = recur_add_player(max_board, MIN)
        board = min_board
    return board

def is_stable_board(board, i):
    prev_level = play_board(board, i-1)
    cur_level = play_board(board, i)
    return prev_level == cur_level

def find_level(board):
    if is_stable_board(board, ROWS+1):
        return None



if __name__ == '__main__':
    board = make_sample_board(BLANK_BOARD)
    pp = pprint.PrettyPrinter(width = 40)
    #pp.pprint(board)

    first_level = play_board(board, 1)
    assert first_level == min_1_SOLUTION

    print is_stable_board(board, 8)
