import pygame
import sys
import math
import pprint
import random

width = 640
height = 400

BLACK = 0,0,0
RED = 255,0,0
BLUE = 0,0,255
WHITE = 255, 255, 255

RADIUS = height/20

PLAYER_TO_COLOR = {1: RED, 2: BLUE}

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

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


    def draw_board(self):
        for row_num in range(self.rows+1):
            row_start = (self.left_disp_offset, self.top_disp_offset + (self.box_size *  row_num))
            row_end = (self.left_disp_offset + (self.box_size * self.cols), self.top_disp_offset + (self.box_size *  row_num))
            pygame.draw.line(self.screen, WHITE, row_start, row_end)
        for col_num in range(self.cols+1):
            col_start = (self.left_disp_offset + (self.box_size * col_num), self.top_disp_offset)
            col_end = (self.left_disp_offset + (self.box_size * col_num), self.top_disp_offset + (self.box_size * self.rows))
            pygame.draw.line(self.screen, WHITE, col_start, col_end)

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
            row = get_row(self.grid, col)
            if row:
                return (col, row)
        return None

    def get_slot_pos_from_indices(self, indices):
        x,y = indices
        board_x_pos = int(self.box_size * (x + 0.5))
        board_y_pos = int(self.box_size * (y + 0.5))
        return self.add_offset((board_x_pos, board_y_pos))

    def draw(self):
        self.draw_board()
        for i, row in enumerate(self.grid):
            for j, col in enumerate(row):
                if col != 0:
                    if col == 1:
                        color = RED
                    if col == 2:
                        color = BLUE
                    pos = self.get_slot_pos_from_indices((j,i))
                    pygame.draw.circle(self.screen, color, pos, RADIUS)

def get_row(grid, col):
    for i, row in enumerate(reversed(grid)):
    #if it's over a column, figure out the bottom
    #slot in the grid to put the piece
        if row[col] == 0:
            return 6-i-1
    return None


def get_distance(mouse, piece):
    mx, my = mouse
    px, py = piece

    dx = mx-px
    dy = my-py

    dx2 = dx**2
    dy2 = dy**2

    distance2 = dx2 + dy2

    return math.sqrt(distance2)

def set_all_ungrabbed(pieces):
    for piece in pieces:
        piece.is_grabbed = False
        piece.offset = (0,0)

def is_row_win(grid):
    for row in reversed(grid):
        streak = 0
        if row[3] != 0:
            is_winner = row[3]
            for column in row:
                if column == is_winner:
                    streak += 1
                else:
                    streak = 0
                if streak >= 4:
                    print "row winner"
                    return is_winner
    return None

def is_col_win(grid):
    row3 = grid[2]
    row4 = grid[3]
    for i in range(7):
        #check to see if row3 and 4 have a match first
        if row3[i] != 0 and row3[i] == row4[i]:
            is_winner = row3[i]
            streak = 0
            for row in reversed(grid):
                if row[i] == is_winner:
                    streak += 1
                else:
                    streak = 0
                if streak >=4:
                    print "column winner"
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
        if f_index <=  6 and row[f_index] == player:
            f_streak += 1
        else:
            f_streak = 0
        if b_index >= 0 and row[b_index] == player:
            b_streak += 1
        else:
            b_streak = 0
        if f_streak == 0 and b_streak == 0:
            return None
    if f_streak == 4 or b_streak == 4:
        return player
    else:
        return None

def is_diag_win(grid):
    for i, row in enumerate(reversed(grid[3:])):
        for j, column in enumerate(row):
            if column != 0:
                top = 2 - i
                bottom = 5 - i
                winner = check_diagonal(column, j,  grid[top:bottom])
                if winner:
                    print "diagonal winner"
                    return winner
    return None

def determine_winner(grid):
    return is_row_win(grid) or is_col_win(grid) or is_diag_win(grid)


b = Board(screen)
red_piece = Piece(screen, 1, (int(width*0.75), height/2))
piece = red_piece
added_to_grid = False
auto = False
'''
grid = [[0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 2, 0],
        [2, 0, 1, 0, 2, 1, 0],
        [1, 0, 2, 2, 0, 2, 0],
        [1, 0, 2, 1, 1, 1, 2]]

print determine_winner(grid)

'''

print "Welcome to Connect Four!"
print "Please move a piece, select keys 1-7, or select 'a' to automate game"

while True:
    screen.fill(BLACK)
    b.draw()
    if piece:
        piece.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_x):
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
        #player wants to reset game
            b = Board(screen) #create a new board
            red_piece = Piece(screen, 1, (int(width*0.75), height/2)) #add a piece to board
            piece = red_piece
            added_to_grid = False
            auto = False

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
                    row = get_row(b.grid, slot)
                    if row:
                        b.grid[row][slot] = piece.player
                        added_to_grid = True

                #see if user selected "a" for automatic
                elif event.key == pygame.K_a:
                    auto = True

    if auto:
        slot = random.randint(0,6)
        row = get_row(b.grid, slot)
        if row:
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
            auto = False
            pprint.pprint(b.grid)
            print "Please press 'r' to restart game"
        else:
            piece = Piece(screen, next_player, (int(width*0.75), height/2))

            #pprint.pprint(b.grid)


    pygame.display.flip()
    clock.tick(100)
