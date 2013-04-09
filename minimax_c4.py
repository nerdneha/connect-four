import connect_four
import pprint

ROWS = 3
COLUMNS = 3
TO_WIN = 3

MAX = 1
MIN = 2

BLANK_BOARD = [[0 for i in range(COLUMNS)] for j in range(ROWS)]

def is_row_win(grid):
    mr = (COLUMNS + 1)/2
    for row in reversed(grid):
        streak = 0
        if row[mr] != 0:
            is_winner = row[mr]
            for column in row:
                if column == is_winner:
                    streak += 1
                else:
                    streak = 0
                if streak >= TO_WIN:
                    return is_winner
    return None

def is_col_win(grid):
    mc = grid[((ROWS+1)/2)]
    for i in range(COLUMNS):
        #check to see if row3 and 4 have a match first
        if mc[i] != 0:
            is_winner = mc[i]
            streak = 0
            for row in reversed(grid):
                if row[i] == is_winner:
                    streak += 1
                else:
                    streak = 0
                if streak >= TO_WIN:
                    return is_winner
    return None

def check_diagonal(player, index, grid):
    f_index = index
    b_index = index
    f_streak = 1
    b_streak = 1

    for row in reversed(grid):
        f_index += 1
        b_index -= 1
        if f_index < COLUMNS and row[f_index] == player:
            f_streak += 1
        else:
            f_streak = 0
        if b_index >= 0 and row[b_index] == player:
            b_streak += 1
        else:
            b_streak = 0
        if f_streak == 0 and b_streak == 0:
            return None
    if f_streak == TO_WIN or b_streak == TO_WIN:
        return player
    else:
        return None

def is_diag_win(grid):
    mr = (ROWS + 1)/2
    for i, row in enumerate(reversed(grid[mr:])):
        for j, column in enumerate(row):
            if column != 0:
                top = ROWS - TO_WIN - i
                bottom = ROWS - 1 - i
                winner = check_diagonal(column, j,  grid[top:bottom])
                if winner:
                    return winner
    return None

def determine_winner(grid):
    return is_row_win(grid) or is_col_win(grid) or is_diag_win(grid)

def make_sample_board(b):
    r = ROWS
    b[connect_four.get_row(b,1,ROWS)][1] = MAX
    b[connect_four.get_row(b,0,ROWS)][0] = MIN
    b[connect_four.get_row(b,1,ROWS)][1] = MAX
    b[connect_four.get_row(b,1,ROWS)][1] = MIN
    b[connect_four.get_row(b,0,ROWS)][0] = MAX
    b[connect_four.get_row(b,2,ROWS)][2] = MIN
    return b

def make_move(b, player):
    boards = []
    for i in range(COLUMNS):
        new_b = [row[:] for row in b]
        row = connect_four.get_row(b, i, ROWS)
        if row != None:
            new_b[connect_four.get_row(b, i, ROWS)][i] = player
            boards.append([new_b[:],i] )
    return boards

def no_more_moves(board):
    #if there are no 0's in the top row, there are no more moves
    return not(0 in board[0])

def get_max_or_min(possible_moves, player):
    if player == MAX:
        return max(possible_moves)
    else:
        return min(possible_moves)

def recur_add_player_depth(board, player, boards=[], col=0):
    pp.pprint(board)
    import pdb
    pdb.set_trace()
    winner = determine_winner(board)
    if winner:
        if winner == MAX:
            return (1, col)
        if winner == MIN:
            return (-1, col)
    elif no_more_moves(board):
        return (0, col)
    else:
        boards = make_move(board, player)
        possible_moves = []
        for b, col in boards:
            if player == MAX:
                next_player = MIN
            else:
                next_player = MAX
            recur_result, _ = recur_add_player_depth(b, next_player, boards, col)
            possible_moves.append((recur_result, col))
        return get_max_or_min(possible_moves, player)

no_moves_EXAMPLE = [[1, 2, 2], [1, 1, 1], [2, 1, 2]]

max_1_SOLUTION = [
     [[0, 2, 0], [1, 1, 0], [2, 1, 0]],
     [[0, 2, 0], [0, 1, 0], [2, 1, 0]],
     [[0, 2, 0], [0, 1, 0], [2, 1, 1]]]


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

row_win_EXAMPLE = [[0, 0, 0], [0, 0, 0], [0, 2, 0], [1, 1, 1], [2, 1, 2]]
col_win_EXAMPLE = [[0, 0, 0], [0, 0, 0], [0, 1, 0], [0, 1, 0], [2, 1, 0]]
diag_win_EXAMPLE = [[0, 0, 0], [0, 0, 0], [1, 2, 0], [2, 1, 0], [2, 1, 1]]


if __name__ == '__main__':
    board = make_sample_board(BLANK_BOARD)
    pp = pprint.PrettyPrinter(width = 20)

    assert no_more_moves(board) == False
    assert no_more_moves(no_moves_EXAMPLE) == True

    print recur_add_player_depth(board, MAX)
    '''
    first_level = play_board(board, 1)
    print_board(board, 5)

    assert first_level == min_1_SOLUTION
    assert is_row_win(row_win_EXAMPLE) == True
    assert is_col_win(col_win_EXAMPLE) == True
    assert is_diag_win(diag_win_EXAMPLE) == True
    '''
