import pygame
import sys
import math

width = 640
height = 400

BLACK = 0,0,0
RED = 255,0,0
BLUE = 0,0,255
WHITE = 255, 255, 255

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

class Piece:
    def __init__(self, screen, color, center_pos, radius=height/20):
        self.screen = screen
        self.color = color
        self.pos = center_pos
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


    def draw(self):
        for row_num in range(self.rows+1):
            row_start = (self.left_disp_offset, self.top_disp_offset + (self.box_size *  row_num))
            row_end = (self.left_disp_offset + (self.box_size * self.cols), self.top_disp_offset + (self.box_size *  row_num))
            pygame.draw.line(self.screen, WHITE, row_start, row_end)
        for col_num in range(self.cols+1):
            col_start = (self.left_disp_offset + (self.box_size * col_num), self.top_disp_offset)
            col_end = (self.left_disp_offset + (self.box_size * col_num), self.top_disp_offset + (self.box_size * self.rows))
            pygame.draw.line(self.screen, WHITE, col_start, col_end)

    def translate_mouse_pos(self, mouse_pos):
        mx, my = mouse_pos
        return mx - self.left_disp_offset, my - self.top_disp_offset

    def mouse_over_col(self, mouse_pos):
        mx, my = self.translate_mouse_pos(mouse_pos)
        col = mx / self.box_size
        if col in range(self.cols):
            print "col:", col
            return col
        else:
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

def get_grabbed(pieces):
    return [piece for piece in pieces if piece.is_grabbed]

def set_all_ungrabbed(pieces):
    for piece in pieces:
        piece.is_grabbed = False
        piece.offset = (0,0)

b = Board(screen)
red_piece = Piece(screen, RED, (width/2, height/2))
blue_piece = Piece(screen, BLUE, (100,100))
pieces = [red_piece, blue_piece]
grabbed_list = []

while True:
    screen.fill(BLACK)
    b.draw()

    for piece in pieces:
        piece.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for piece in pieces:
                piece.is_grabbed = piece.is_mouse_over(event)
                if piece.is_grabbed:
                    piece.set_offset(event.pos)
        if event.type == pygame.MOUSEMOTION and any([piece.is_grabbed for piece in pieces]):
            grabbed_list = get_grabbed(pieces)
            for piece in grabbed_list:
                piece.move(event.pos)
        if event.type == pygame.MOUSEBUTTONUP:
            b.mouse_over_col(event.pos)
            set_all_ungrabbed(pieces)



    pygame.display.flip()
    clock.tick(100)
