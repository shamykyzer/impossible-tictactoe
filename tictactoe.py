import pygame as pg
from pygame.locals import *
import sys

pg.init()

XO = 'X'
fps = 30
CLOCK = pg.time.Clock()

screen = pg.display.set_mode((400, 400), 0, 32)
pg.display.set_caption("IMPOSSIBLE Tic Tac Toe")
initiating_window = pg.image.load("gameboard.png")

x_img = pg.image.load("X.jpg")
o_img = pg.image.load("O.jpg")
initiating_window = pg.transform.scale(initiating_window, (400, 400))
x_img = pg.transform.scale(x_img, (120, 120))
o_img = pg.transform.scale(o_img, (120, 120))


winner = None
draw = False
board = [[None] * 3, [None] * 3, [None] * 3]

def update_game_state():
    global XO, winner, draw
    winner = check_winner()
    if winner:
        print(f"Player {winner} wins!")
    draw = check_draw()
    if draw:
        print("It's a draw!")
    if XO == 'X':
        XO = 'O'
    else:
        XO = 'X'

def check_winner():
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            return board[row][0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None

def check_draw():
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                return False
    return True

def handle_user_input():
    global XO, winner, draw
    for event in pg.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN and not winner and not draw:
            mouse_pos = pg.mouse.get_pos()
            col = mouse_pos[0] // 133
            row = mouse_pos[1] // 133
            if board[row][col] is None:
                board[row][col] = XO
                update_game_state()

running = True
while running:
    handle_user_input()
    screen.fill((255, 255, 255))
    screen.blit(initiating_window, (0, 0))
    for row in range(3):
        for col in range(3):
            if board[row][col] == 'X':
                screen.blit(x_img, (col * 133 + 10, row * 133 + 10))
            elif board[row][col] == 'O':
                screen.blit(o_img, (col * 133 + 10, row * 133 + 10))
    pg.display.update()
    CLOCK.tick(fps)

pg.quit()
sys.exit()
