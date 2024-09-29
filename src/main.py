"""
This file handles and runs the tic-tac-toe game.
"""

import sys
import pygame

from src.ai_player import AIPlayer


# Constants
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Define player / computer
player_icon = "O"
computer_icon = "X"
blank_icon = " "

# Game board
board = [[blank_icon for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

#Previous paths
#Each path format: [[first move],[second mvoe]]
#At the same index, results displays whether or not computer has won.
record = []
results = []

# Function to draw the grid
def draw_grid():
    screen.fill(WHITE)
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, BLACK, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, BLACK, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# Function to draw X and O on the board
def draw_marks():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == player_icon:
                pygame.draw.line(screen, RED, 
                                 (col * SQUARE_SIZE + 20, row * SQUARE_SIZE + 20), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - 20, row * SQUARE_SIZE + SQUARE_SIZE - 20), 
                                 LINE_WIDTH)
                pygame.draw.line(screen, RED, 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - 20, row * SQUARE_SIZE + 20), 
                                 (col * SQUARE_SIZE + 20, row * SQUARE_SIZE + SQUARE_SIZE - 20), 
                                 LINE_WIDTH)
            elif board[row][col] == computer_icon:
                pygame.draw.circle(screen, BLUE, 
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 
                                   SQUARE_SIZE // 2 - 20, LINE_WIDTH)

# Function to check for a winner
def check_winner(player):
    for row in range(BOARD_ROWS):
        if all([cell == player for cell in board[row]]):
            return True
    for col in range(BOARD_COLS):
        if all([board[row][col] == player for row in range(BOARD_ROWS)]):
            return True
    if all([board[i][i] == player for i in range(BOARD_ROWS)]) or \
       all([board[i][BOARD_ROWS - 1 - i] == player for i in range(BOARD_ROWS)]):
        return True
    return False

# Function to check for a draw
def check_draw():
    return all([cell != blank_icon for row in board for cell in row])

def reset_board():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = blank_icon

# Main game loop
def main():

    player_turn = True  # True for player, False for computer
    current_path = []   # [(pos,icon)] => ex. [((1,2),"O"),((0,2),"X")]

    comp_player = AIPlayer(computer_icon)

    def update_box(player, row, col):
        board[row][col] = player
        current_path.append(((row,col),player))

    def end_round(result): 
        # cp_point: 1 if comp wins, -1 if player wins, 0 if draw
        if (result == blank_icon):
            print("Draw.")
        elif (result == player_icon):
            print("Player wins.")
        else:
            print("Computer wins.")
        comp_player.update_data()
        reset_board()
        main()


    while True:
        draw_grid()
        draw_marks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0]
                mouseY = event.pos[1]

                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                if board[clicked_row][clicked_col] == blank_icon:
                    update_box(player_icon,clicked_row,clicked_col)
                    if check_winner(player_icon):
                        end_round(player_icon)
                    player_turn = False

            if not player_turn:
                (picked_row, picked_col) = comp_player.choose_pos(current_path) 
                update_box(computer_icon,picked_row,picked_col)
                if check_winner(computer_icon):
                    end_round(computer_icon)
                player_turn = True

        if check_draw():
            end_round(blank_icon)

        pygame.display.update()

if __name__ == "__main__":
    main()
