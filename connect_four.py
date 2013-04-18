import pygame
import sys
import math
import pprint
import random
import minimax_c4

width = 640
height = 400

BLACK = 0,0,0
RED = 255,0,0
BLUE = 0,0,255
WHITE = 255, 255, 255

RADIUS = height/20

PLAYER_TO_COLOR = {1: RED, 2: BLUE}

PLAYERS_COLOR = {1: "red", 2: "blue"}

ROWS = 6
COLUMNS = 7
TO_WIN = 4

DEPTH_LIMIT = {"medium": 3, "hard": 5}

pygame.font.init()

class Piece:
    def __init__(self, screen, player, pos, radius=height/20):
        self.screen = screen
        self.player = player
        self.pos = pos
        self.color = PLAYER_TO_COLOR[player]
        self.radius = radius
        self.is_grabbed = False
        self.offset = (0,0)

    def set_offset(self, mouse):
        mx, my = mouse
        px, py = self.pos
        self.offset = (mx-px, my-py)

    def move(self, mouse_pos):
        mx, my = mouse_pos
        ox, oy = self.offset
        self.pos = (mx-ox, my-oy)

    def is_mouse_over(self, event):
        mouse_position = event.pos
        distance_to_center = get_distance(mouse_position, self.pos)
        return distance_to_center < self.radius

    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.pos, self.radius)

class Board:
    def __init__(self, screen):
        self.screen = screen
        self.rows = 6
        self.cols = 7
        self.grid = [[0 for i in range(self.cols)] for j in range(self.rows)]
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        self.box_size = screen_height / (self.rows + 2)
        self.left_disp_offset = self.box_size * 2
        self.top_disp_offset = self.box_size
        self.computer_mode = False


    def draw_board(self, winner):
        my_font = pygame.font.SysFont("monospace", 20)
        for row_num in range(self.rows+1):
            row_start = (self.left_disp_offset, self.top_disp_offset + (self.box_size *  row_num))
            row_end = (self.left_disp_offset + (self.box_size * self.cols), self.top_disp_offset + (self.box_size *  row_num))
            pygame.draw.line(self.screen, WHITE, row_start, row_end)
        for col_num in range(self.cols+1):
            col_start = (self.left_disp_offset + (self.box_size * col_num), self.top_disp_offset)
            col_end = (self.left_disp_offset + (self.box_size * col_num), self.top_disp_offset + (self.box_size * self.rows))
            if col_num > 0:
                col_label= my_font.render(str(col_num), 1, WHITE)
                self.screen.blit(col_label, (self.left_disp_offset + (self.box_size * col_num) - self.box_size/2, height-40))
            pygame.draw.line(self.screen, WHITE, col_start, col_end)
        if winner != None:
            if self.computer_mode == True:
                if winner == 2:
                    win_text = "Computer WINS!! Press 'r' to try again"
                else:
                    win_text = "You BEAT the computer!! Press 'r' to play again"
            else:
                win_text = "Player %s (%s) WINS!! Press 'r' to play again" % (winner, PLAYERS_COLOR[winner])
            my_font = pygame.font.SysFont("monospace", 20)
            winner_text = my_font.render(win_text, 1, WHITE)
            self.screen.blit(winner_text, (50, 10))

    def write_board_instructions(self):
        my_font = pygame.font.SysFont("monospace", 15)
        a = my_font.render("Instructions:", 1, (0,255,0))
        b = my_font.render("Move a chip or", 1, WHITE)
        c = my_font.render("select a column", 1, WHITE)

        self.screen.blit(a, (480, 100))
        self.screen.blit(b, (470, 120))
        self.screen.blit(c, (470, 140))

    def remove_offset(self, pos):
        x,y = pos
        return (x - self.left_disp_offset, y - self.top_disp_offset)

    def add_offset(self, pos):
        x,y = pos
        return (x + self.left_disp_offset, y + self.top_disp_offset)

    def get_col(self, pos):
        x, y = self.remove_offset(pos)
        col = x / self.box_size
        if col in range(self.cols):
            #print "col:", col
            return col
        else:
            return None

    def get_indices(self, pos):
        #get the column that the mouse is over
        col = self.get_col(pos)

        #column is an integer between 0 and self.cols
        if col != None:
            row = get_row(self.grid, col, ROWS)
            if row != None:
                return (col, row)
        return None

    def get_slot_pos_from_indices(self, indices):
        x,y = indices
        board_x_pos = int(self.box_size * (x + 0.5))
        board_y_pos = int(self.box_size * (y + 0.5))
        return self.add_offset((board_x_pos, board_y_pos))

    def draw(self, winner):
        self.draw_board(winner)
        self.write_board_instructions()
        for i, row in enumerate(self.grid):
            for j, col in enumerate(row):
                if col != 0:
                    if col == 1:
                        color = RED
                    if col == 2:
                        color = BLUE
                    pos = self.get_slot_pos_from_indices((j,i))
                    pygame.draw.circle(self.screen, color, pos, RADIUS)

def get_row(grid, col, rows):
    for i, row in enumerate(reversed(grid)):
    #if it's over a column, figure out the bottom
    #slot in the grid to put the piece
        if row[col] == 0:
            return rows-i-1
    return None

def get_random_spot(grid):
    slot = random.randint(0,6)
    row = get_row(grid, slot, ROWS)
    return slot, row

def get_distance(mouse, piece):
    mx, my = mouse
    px, py = piece

    dx = mx-px
    dy = my-py

    dx2 = dx**2
    dy2 = dy**2

    distance2 = dx2 + dy2

    return math.sqrt(distance2)

def get_winner(connected_squares):
    if len(set(connected_squares)) == 1:
        member = connected_squares.pop()
        return member

def is_row_win(grid):
    for row in reversed(grid):
        for start in range(COLUMNS - TO_WIN + 1):
            if row[start] != 0:
                connected_squares = [row[start+i] for i in range(TO_WIN)]
                winner = get_winner(connected_squares)
                if winner:
                    return winner

def is_col_win(grid):
    for col_num in range(COLUMNS):
        col = [row[col_num] for row in reversed(grid)]
        for start in range(ROWS - TO_WIN + 1):
            if col[start] != 0:
                connected_squares = [col[start+i] for i in range(TO_WIN)]
                winner = get_winner(connected_squares)
                if winner:
                    return winner

def generate_legal_diagonals(grid):
    diags = []
    #top left -> bottom right
    for row_num in range(ROWS - TO_WIN + 1):
        for col_num in range (COLUMNS - TO_WIN + 1):
            connected_squares = [grid[row_num+i][col_num+i] for i in range(TO_WIN)]
            if 0 not in connected_squares:
                diags.append(connected_squares)
    #bottom left -> top right
    for row_num in range(TO_WIN - 1, ROWS):
        for col_num in range (COLUMNS - TO_WIN + 1):
            connected_squares = [grid[row_num-i][col_num+i] for i in range(TO_WIN)]
            if 0 not in connected_squares:
                diags.append(connected_squares)
    return diags

def is_diag_win(grid):
    for diag in generate_legal_diagonals(grid):
        winner = get_winner(diag)
        if winner:
            return winner

def determine_winner(grid):
    return is_row_win(grid) or is_col_win(grid) or is_diag_win(grid)

def setup_loop(screen):
    screen.fill(BLACK)
    my_font = pygame.font.SysFont("monospace", 20)
    welcome_msg = my_font.render("Welcome to Connect Four!", 1, WHITE)

    a = my_font.render("Please press:", 1, WHITE)
    b = my_font.render("- 'a' to automate game", 1, WHITE)
    c = my_font.render("- 'c' to play against the computer", 1, WHITE)
    d = my_font.render("- 'p' to play a two-player game", 1, WHITE)
    h = 120
    screen.blit(welcome_msg, (160, 60))
    screen.blit(a, (25, h))
    screen.blit(b, (45, h + 25))
    screen.blit(c, (45, h + 50))
    screen.blit(d, (45, h + 75))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                #see if user selected "a" for automatic
                    return "auto"

                if event.key == pygame.K_c:
                #see if user selected "c" for computer
                    return "computer"

                if event.key == pygame.K_p:
                    return "play"

                if event.key == pygame.K_q or event.key == pygame.K_x:
                    sys.exit()
                    return "quit"

def ask_computer_level(screen):
    screen.fill(BLACK)
    my_font = pygame.font.SysFont("monospace", 20)
    welcome_msg = my_font.render("You'll be playing the computer!", 1, WHITE)

    a = my_font.render("Please select the difficulty level:", 1, WHITE)
    b = my_font.render("1: Easy", 1, WHITE)
    c = my_font.render("2: Medium", 1, WHITE)
    d = my_font.render("3: Hard", 1, WHITE)
    h = 120
    screen.blit(welcome_msg, (160, 60))
    screen.blit(a, (25, h))
    screen.blit(b, (45, h + 25))
    screen.blit(c, (45, h + 50))
    screen.blit(d, (45, h + 75))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "easy"

                if event.key == pygame.K_2:
                    return "medium"

                if event.key == pygame.K_3:
                    return "hard"

                if event.key == pygame.K_q or event.key == pygame.K_x:
                    sys.exit()
                    return "quit"
                if event.key == pygame.K_r:
                    return "reset"



def game_loop(screen, clock, mode, level=None):
    b = Board(screen)
    red_piece = Piece(screen, 1, (int(width*0.75), height/2))
    piece = red_piece

    added_to_grid = False
    winner = None

    while True:
        if mode != "reset":
            screen.fill(BLACK)
            b.draw(winner)
            if piece:
                piece.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and (event.key == pygame.K_x or event.key == pygame.K_q)):
                sys.exit()

            if event.type == pygame.KEYDOWN or mode == "reset":
                if event.key == pygame.K_r or mode == "reset":
                #player wants to reset game
                    winner = None
                    level = None
                    mode = setup_loop(screen)
                    b = Board(screen) #create a new board
                    red_piece = Piece(screen, 1, (int(width*0.75), height/2)) #add a piece to board
                    piece = red_piece
                    added_to_grid = False


            if piece:
                if event.type == pygame.MOUSEBUTTONDOWN:
                #if mouse is over the piece, set piece as grabbed
                #and record the offset as the distance from mouse to center
                    piece.is_grabbed = piece.is_mouse_over(event)
                    if piece.is_grabbed:
                        piece.set_offset(event.pos)


                if event.type == pygame.MOUSEMOTION and piece.is_grabbed:
                #if you move while the piece is grabbed, move the piece
                #with you.
                    if piece.is_grabbed:
                        piece.move(event.pos)

                if event.type == pygame.MOUSEBUTTONUP:
                #if you unclick piece over the board, get "indices" of board
                #position to put piece
                    if piece.is_grabbed:
                        indices = b.get_indices(piece.pos)
                        if indices:
                            slot_pos = b.get_slot_pos_from_indices(indices)

                            x,y = indices
                            b.grid[y][x] = piece.player
                            added_to_grid = True


                if event.type == pygame.KEYDOWN:
                    #see if a slot was selected by user (key 1-7)
                    slot = event.key - 49#if you press 1-7 event.key = 49-55
                    if slot <= 6:
                        row = get_row(b.grid, slot, ROWS)
                        if row != None:
                            b.grid[row][slot] = piece.player
                            added_to_grid = True


        if mode == "computer":
            b.computer_mode = True
            if level == None:
                response = ask_computer_level(screen)
                if response in ["easy", "medium", "hard"]:
                    level = response
                else:
                    mode = response
            if piece.player == 2:
                if level == "easy":
                    slot, row = get_random_spot(b.grid)
                if level == "medium" or level == "hard":
                    _, slot = minimax_c4.recur_add_player_depth(b.grid, 2, DEPTH_LIMIT[level], 4, {})
                    row = get_row(b.grid, slot, ROWS)
                if row != None:
                    b.grid[row][slot] = piece.player
                    added_to_grid = True

        if mode == "auto":
            slot, row = get_random_spot(b.grid)
            if row != None:
                b.grid[row][slot] = piece.player
                added_to_grid = True

        if added_to_grid:
            #alternate player 1 and 2
            next_player = (piece.player)%2 + 1

            added_to_grid = False

            winner = determine_winner(b.grid)
            if winner:
                print "********************"
                print "Player %s WINS!!" % (winner)
                print "********************"
                piece = None
                mode = None
                pprint.pprint(b.grid)
                print "Please press 'r' to restart game"
            else:
                piece = Piece(screen, next_player, (int(width*0.75), height/2))

                #pprint.pprint(b.grid)


        pygame.display.flip()
        clock.tick(100)

def get_computer_level():
    return None


if __name__ == '__main__':
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    computer = False

    print "Welcome to Connect Four!"
    print "Please move a piece, select keys 1-7, or select 'a' to automate game"
    print "Select 'c' if you want to play against the computer (you are red)"

    mode = setup_loop(screen)
    game_loop(screen, clock, mode)


