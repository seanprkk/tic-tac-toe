"""
This file contains the ai player class to play tic-tac-toe in main.py.
"""

import numpy as np
import pandas as pd

pos = [['top-left-square','top-middle-square','top-right-square'],
       ['middle-left-square','middle-middle-square','middle-right-square'],
       ['bottom-left-square','bottom-middle-square','bottom-right-square']]

data = "data/tic-tac-toe.data.csv"
icon_map = {"b":" ","o":"O","x":"X","positive":"X","negative":"O"}

class AIPlayer:

    def __init__(self, i):
        self.prev_games = pd.read_csv(data)
        self.icon = i
        #self.map_data()
        
    def map_data(self):
        for col in self.prev_games.columns:
            self.prev_games[col] = self.prev_games[col].map(icon_map)

    def check_win(self, board):
        for row in range(3):
            if all([cell == self.icon for cell in board[row]]):
                return True
        for col in range(3):
            if all([board[row][col] == self.icon for row in range(3)]):
                return True
        if all([board[i][i] == self.icon for i in range(3)]) or \
            all([board[i][3 - 1 - i] == self.icon for i in range(3)]):
            return True
        return False


    def get_cond_win_rate(self, current_path, this_pos):
        x = self.prev_games
        board = [["" for _ in range(3)] for _ in range(3)]
        for path in current_path:
            row = path[0][0]
            col = path[0][1]
            icon = path[1]
            x = x[x[pos[row][col]] == icon]
            board[row][col] = icon
        x = x[x[pos[this_pos[0]][this_pos[1]]] == self.icon]
        board[this_pos[0]][this_pos[1]] = self.icon
        if (self.check_win(board)):
            return 3
        elif (len(x)==0):
            return 2
        else:
            return np.mean(x['Class'] == self.icon)


    # TODO: some game instances not trained; needs to try new paths (infrequent) before securing win.
    def choose_pos(self, current_path):
        best_prob = -1
        for row in range(3):
            for col in range(3):
                pos = (row,col)
                if pos in [path[0] for path in current_path]:
                    continue
                prob = self.get_cond_win_rate(current_path,pos)
                if (prob > best_prob):
                    best_pos = pos
                    best_prob = prob
                    print(best_pos, best_prob)
        print("Returns: ", best_pos)
        return best_pos

    def add_game(self,path,blank_icon,winner):
        new_game = {} #continue here
        for p in path:
            row = p[0][0]
            col = p[0][1]
            icon = p[1]
            new_game[pos[row][col]] = icon
        for row in range(3):
            for col in range(3):
                if pos[row][col] not in new_game.keys():
                    new_game[pos[row][col]] = blank_icon
        new_game['Class'] = winner
        self.prev_games.loc[len(self.prev_games)] = new_game
    
    def store_data(self):
        self.prev_games.to_csv(data,index=False)
        print("Game record saved to: " + data)
    