import pygame as pg
from pygame.locals import *
import sys
import random
from constants import *

# Initialize pygame
pg.init()

# Create the game window
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Tic Tac Toe")

# Initialize the game variables
XO = 'X'
AI = 'O'
FPS = 60

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
                pg.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
            return self.squares[0][0]

        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] and self.squares[2][0] is not None:
            if show:
                color = CIRC_COLOR if self.squares[2][0] == 'O' else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pg.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
            return self.squares[2][0]

        return None
    
    def draw_winning_line(self, winner):
        for col in range(3):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] and self.squares[0][col] is not None:
                color = CIRC_COLOR if self.squares[0][col] == 'O' else CROSS_COLOR
                iPos = (col * SQSIZE + SQSIZE // 2, 20)
                fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                pg.draw.line(screen, color, iPos, fPos, LINE_WIDTH)

        for row in range(3):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] and self.squares[row][0] is not None:
                color = CIRC_COLOR if self.squares[row][0] == 'O' else CROSS_COLOR
                iPos = (20, row * SQSIZE + SQSIZE // 2)
                fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                pg.draw.line(screen, color, iPos, fPos, LINE_WIDTH)

        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] and self.squares[0][0] is not None:
            color = CIRC_COLOR if self.squares[0][0] == 'O' else CROSS_COLOR
            iPos = (20, 20)
            fPos = (WIDTH - 20, HEIGHT - 20)
            pg.draw.line(screen, color, iPos, fPos, LINE_WIDTH)

        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] and self.squares[2][0] is not None:
            color = CIRC_COLOR if self.squares[2][0] == 'O' else CROSS_COLOR
            iPos = (20, HEIGHT - 20)
            fPos = (WIDTH - 20, 20)
            pg.draw.line(screen, color, iPos, fPos, LINE_WIDTH)

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
        self.mode = 'PvP'

    def handle_user_input(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.running = False
            elif event.type == pg.MOUSEBUTTONDOWN and not self.board.final_state() and not self.board.is_full():
                if self.mode == 'PvP':
                    self.handle_pvp_move(event)
                elif self.mode == 'AI' and self.player == XO:
                    self.handle_pvp_move(event)

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    self.mode = 'PvP'
                    self.reset()
                elif event.key == pg.K_a:
                    self.mode = 'AI'
                    self.reset()
                elif event.key == pg.K_SPACE and (self.board.final_state() or self.board.is_full()):
                    self.reset()

    def handle_pvp_move(self, event):
        mouse_pos = pg.mouse.get_pos()
        col = mouse_pos[0] // SQSIZE
        row = mouse_pos[1] // SQSIZE
        if self.board.empty_sqr(row, col):
            self.board.mark_sqr(row, col, self.player)
            self.player = 'O' if self.player == 'X' else 'X'

    def minimax(self, board, depth, isMaximizing):
        winner = board.final_state()
        if winner == AI:
            return {'score': 1, 'row': None, 'col': None}
        elif winner == XO:
            return {'score': -1, 'row': None, 'col': None}
        elif board.is_full():
            return {'score': 0, 'row': None, 'col': None}

        if isMaximizing:
            best_score = {'score': -float('inf'), 'row': None, 'col': None}
            for row in range(3):
                for col in range(3):
                    if board.empty_sqr(row, col):
                        board.mark_sqr(row, col, AI)
                        score = self.minimax(board, depth + 1, False)
                        board.squares[row][col] = None
                        board.marked_sqrs -= 1
                        score['row'] = row
                        score['col'] = col
                        best_score = max(best_score, score, key=lambda x:x['score'])
            return best_score

        else:
            best_score = {'score': float('inf'), 'row': None, 'col': None}
            for row in range(3):
                for col in range(3):
                    if board.empty_sqr(row, col):
                        board.mark_sqr(row, col, XO)
                        score = self.minimax(board, depth + 1, True)
                        board.squares[row][col] = None
                        board.marked_sqrs -= 1
                        score['row'] = row
                        score['col'] = col
                        best_score = min(best_score, score, key=lambda x:x['score'])
            return best_score

    def handle_ai_move(self):
        if self.board.is_empty():
            row, col = random.choice([(0, 0), (0, 2), (2, 0), (2, 2)])
        else:
            move = self.minimax(self.board, 0, True)
            row, col = move['row'], move['col']
        self.board.mark_sqr(row, col, self.player)
        self.player = 'X'


    def update_screen(self):
        screen.fill(BG_COLOR)

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

        mode_text = f"Mode: {self.mode}"
        font = pg.font.Font(None, 30)
        text = font.render(mode_text, True, TEXT_COLOR)
        screen.blit(text, (10, 10))

        pg.display.update()    
        
        winner = self.board.final_state()
        if winner:
            self.board.draw_winning_line(winner)
        
    
    def run(self):
        clock = pg.time.Clock()
        while self.running:
            self.handle_user_input()
            if self.mode == 'AI' and self.player == AI and not self.board.final_state() and not self.board.is_full():
                self.handle_ai_move()
                self.player = 'X'
            self.update_screen()
            winner = self.board.final_state()
            if winner:
                self.board.draw_winning_line(winner)
                pg.display.update()
                pg.time.wait(2000)  # pause for 2 seconds to show winning line
                self.reset()
            elif self.board.is_full():
                pg.display.update()
                pg.time.wait(2000)  # pause for 2 seconds to show draw state
                self.reset()
            clock.tick(FPS)

    def reset(self):
        self.board = Board()
        self.player = 'X'
        self.running = True
        self.update_screen()

game = Game()
game.run()

pg.quit()
sys.exit()