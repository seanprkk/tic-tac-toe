import pygame
import sys
import random
from ai_player import AIPlayer


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

# Game board
board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

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
    return all([cell != " " for row in board for cell in row])

# Function for the computer to make a move
def computer_move():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == " ":
                return row, col

    # best_row = 0
    # best_col = 0
    # best_win_rate = -1
    # for row in range(BOARD_ROWS):
    #     for col in range(BOARD_COLS):
    #         if board[row][col] == " ":
    #             this_win_rate = get_win_rate(row,col)
    #             if this_win_rate > best_win_rate:


def reset_board():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = " "

# Main game loop
def main():

    player_turn = True  # True for player, False for computer
    possible_paths = record
    possible_results = results
    current_path = []

    def filter_paths():
        for path in possible_paths:
            #find paths that follow current path
            if len(path) < len(current_path) or path[:len(current_path)] != current_path:
                possible_paths.remove(path)

    def update_box(player, row, col):
        board[row][col] = player
        current_path.append([row,col])
        filter_paths()
        print(current_path)

    def end_round(cp_point): 
        # cp_point: 1 if comp wins, -1 if player wins, 0 if draw
        if (cp_point == 1):
            print("Computer wins.")
        elif (cp_point == 0):
            print("Draw.")
        else:
            print("Player wins.")
        record.append(current_path)
        results.append(cp_point)
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

                if board[clicked_row][clicked_col] == " ":
                    update_box(player_icon,clicked_row,clicked_col)
                    if check_winner(player_icon):
                        end_round(-1)
                    player_turn = False

            if not player_turn:
                picked_row, picked_col = computer_move() 
                update_box(computer_icon,picked_row,picked_col)
                if check_winner(computer_icon):
                    end_round(1)
                player_turn = True

        if check_draw():
            end_round(0)

        pygame.display.update()

if __name__ == "__main__":
    main()
