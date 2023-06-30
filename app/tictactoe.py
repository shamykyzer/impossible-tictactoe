import pygame as pg
from pygame.locals import *
import sys
from constants import *

pg.init()

class Board:
    def __init__(self):
        self.squares = [[None] * 3 for _ in range(3)]
        self.marked_sqrs = 0

    def final_state(self, show=False):
        for col in range(3):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] and self.squares[0][col] is not None:
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 'O' else CROSS_COLOR
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pg.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]

        for row in range(3):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] and self.squares[row][0] is not None:
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 'O' else CROSS_COLOR
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pg.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]

        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] and self.squares[0][0] is not None:
            if show:
                color = CIRC_COLOR if self.squares[0][0] == 'O' else CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pg.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[0][0]

        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] and self.squares[2][0] is not None:
            if show:
                color = CIRC_COLOR if self.squares[2][0] == 'O' else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pg.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[2][0]

        return None

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] is None

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(3):
            for col in range(3):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs

    def is_full(self):
        return self.marked_sqrs == 9

    def is_empty(self):
        return self.marked_sqrs == 0

class Game:
    def __init__(self):
        self.board = Board()
        self.player = 'X'
        self.running = True

    def handle_user_input(self):
        for event in pg.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.running = False
            elif event.type == MOUSEBUTTONDOWN and not self.board.final_state() and not self.board.is_full():
                mouse_pos = pg.mouse.get_pos()
                col = mouse_pos[0] // SQSIZE
                row = mouse_pos[1] // SQSIZE
                if self.board.empty_sqr(row, col):
                    self.board.mark_sqr(row, col, self.player)
                    self.player = 'O' if self.player == 'X' else 'X'

    def update_screen(self):
        screen.fill(BG_COLOR)
        
        # Draw grid lines
        for x in range(SQSIZE, WIDTH, SQSIZE):
            pg.draw.line(screen, LINE_COLOR, (x, 0), (x, HEIGHT), LINE_WIDTH)
        for y in range(SQSIZE, HEIGHT, SQSIZE):
            pg.draw.line(screen, LINE_COLOR, (0, y), (WIDTH, y), LINE_WIDTH)
        
        for row in range(3):
            for col in range(3):
                if self.board.squares[row][col] == 'X':
                    x_pos = col * SQSIZE + OFFSET
                    y_pos = row * SQSIZE + OFFSET
                    pg.draw.line(screen, CROSS_COLOR, (x_pos, y_pos), (x_pos + SQSIZE - 2 * OFFSET, y_pos + SQSIZE - 2 * OFFSET), CROSS_WIDTH)
                    pg.draw.line(screen, CROSS_COLOR, (x_pos, y_pos + SQSIZE - 2 * OFFSET), (x_pos + SQSIZE - 2 * OFFSET, y_pos), CROSS_WIDTH)
                elif self.board.squares[row][col] == 'O':
                    x_pos = col * SQSIZE + SQSIZE // 2
                    y_pos = row * SQSIZE + SQSIZE // 2
                    pg.draw.circle(screen, CIRC_COLOR, (x_pos, y_pos), RADIUS, CIRC_WIDTH)
        pg.display.update()

    def run(self):
        while self.running:
            self.handle_user_input()
            self.update_screen()
            if self.board.final_state(show=True) or self.board.is_full():
                self.running = False
                
    
    # --- OTHER METHODS ---
    
    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.update_screen()
        self.next_turn()

    def next_turn(self):
        self.player = 'O' if self.player == 'X' else 'X'

    def reset(self):
        self.board = Board()
        self.player = 'X'
        self.running = True
        self.update_screen()


screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Tic Tac Toe")

game = Game()
game.run()

# Quit the game
pg.quit()
sys.exit()
