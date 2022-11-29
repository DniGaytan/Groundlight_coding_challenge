# Class responsible of managing a single game board
import random
import numpy as np

class TicTacToeGame():
    def __init__(self, is_ai_playing: bool, is_x_turn: bool):
        self.is_ai_playing = is_ai_playing
        self.is_x_turn = is_x_turn # X always move first | True
        self.board = [['/', '/', '/'], ['/', '/', '/'], ['/', '/', '/']]

    def makeMove(self, x, y, x_turn):
        self.board[x][y] = 'X' if x_turn else 'O'
        return self.check_status()


    def makeAIMove(self, user_x, user_y):
        x,y = self.letAIMove()
        while(self.board[x][y] == 'X' or self.board[x][y] == 'O' or (x == user_x and y == user_y)):
            x,y = self.letAIMove()
        self.board[x][y] = 'O'
        return (self.check_status(),x,y)

    def letAIMove(self):
        return [random.randint(0,2), random.randint(0,2)] # X, Y

    def check_status(self):
        end, winner = self.check_lines()
        if(end):
            return winner
        end, winner = self.check_diags()
        if(end):
            return winner
        if(self.checkForTie()):
            return '_'
        return '/'
    
    def checkForTie(self):
        for x in self.board:
            for y in x:
                if(y == '/'):
                    return False
        return True

    def check_diags(self):
        right_diag = set([self.board[i][i] for i in range(len(self.board))])
        if(len(right_diag) == 1 and '/' not in right_diag):
            return (True, self.board[1][1])
        left_diag = set([self.board[i][len(self.board) - i - 1] for i in range(len(self.board))])
        if(len(left_diag) == 1 and '/' not in left_diag):
            return (True, self.board[1][1])
        return (False, '/')
    
    def check_lines(self):
        for x in self.board:
            if(len(set(x)) == 1 and '/' not in set(x)):
                return (True, x[0])
        
        transpose_board = np.transpose(self.board)
        for x in transpose_board:
            if(len(set(x)) == 1 and '/' not in set(x)):
                return (True, x[0])
        return (False, '/')

    def checkTurn(self):
        return self.player_x if self.next_turn is self.X_TURN else self.player_o


