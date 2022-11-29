from cgitb import text
from tkinter import Tk, Button, Label, ttk, font
import tkinter as tk
from turtle import title
from board import TicTacToeGame as tttg

x_turn = True
game_instance_over = False
parent_game_board = tttg(is_ai_playing=False, is_x_turn=True)
class StartWindow(Tk):
    def __init__(self):
        super().__init__()

        self.title("Nested Tic tac toe")

        self.label = Label(
        text = """
        Hello! Welcome to the nested tic tac toe game!

        This game consists of 9 instances of the traditional tic tac toe game, arranged in a tic tac toe grid.
        To win the game you must win 3 consecutive tic tac toe instances. These must be linear (vertical / horizontal) or
        diagonal. Think of this as a giant tic tac toe containing small tic tac toe games.

        If you win a game with X, the game will turn blue. For O, it will turn red.


        This is a game built by Daniel Gaytan (dnigaytan07@gmail.com)
        """
        )

        self.label.pack()
        self.button = ttk.Button(self, text="Start game 1v1", command = self.openGameWindow).pack(expand=True)
        self.button = ttk.Button(self, text="Start game 1 v PC", command = self.openGameWindowAI).pack(expand=True)

    def openGameWindow(self):
        game_window = GameWindow(self, False)
        game_window.grab_set()
    
    def openGameWindowAI(self):
        game_window = GameWindow(self,True)
        game_window.grab_set()

class GameWindow(tk.Toplevel):
    game_instances = []
    def __init__(self, parent, is_ai_playing):
        super().__init__(parent, )
        self.parent_board_game = self.createParentBoard()
        self.winner = '/'
        self.is_ai_playing = is_ai_playing
        self.title("Nested Tic tac toe (game)")
        overall_game_display_frame = tk.Frame(master=self)
        overall_game_display_frame.grid()
        self.overall_game_display = tk.Label(master=overall_game_display_frame, text="Lets play!", font=font.Font(size=20))
        self.overall_game_display.grid()
        index = 1
        for x in range(1,4):
            for y in range(3):
                temp_game_instance = GameInstance(self, self.is_ai_playing)
                temp_game_instance.createGameInstance(game_num = index, x=x, y=y, parent_frame=self)
                index += 1
        end_game_frame = tk.Frame(master=self)
        end_game_frame.grid(row=5, column=2)
        self.button = ttk.Button(master=end_game_frame, text="End game", command=super().destroy).pack(expand=True)
    
    def createParentBoard(self):
        return tttg(is_ai_playing=False, is_x_turn=True)
        

class GameInstance(ttk.Frame):
    def __init__(self, parent, is_ai_playing):
        self.is_ai_playing = is_ai_playing
        self.tttgame = tttg(is_ai_playing=self.is_ai_playing,is_x_turn=True)
        self.x_turn = True
        self.game_status = "_"
        self.parent = parent
        super().__init__(parent)
    
    def createGameInstance(self, game_num, x, y, parent_frame):
        game_frame = tk.Frame(master=parent_frame, relief=tk.RAISED, borderwidth=1)
        game_frame.grid(row=x, column=y, padx=15, pady=10)
        game_label = tk.Label(master=game_frame, # text=f"Game {game_num}", font=font.Font(size=15)
        )
        game_label.grid(row=0)
        self.setupGameBoard(parent_frame = game_frame)
    
    def setupGameBoard(self, parent_frame):
        index = 0
        for x in range(3):
            for y in range(3):
                game_frame = tk.Frame(master=parent_frame, relief=tk.RAISED, borderwidth=1)
                game_frame.grid(row=x + 1, column=y, padx=15, pady=15)
                game_label = tk.Label(master=game_frame, text="/", font=font.Font(size=15))
                game_label.grid()
                game_label.bind("<Button-1>", self.placeMark)
                index += 1

    def placeMark(self, event):
        global x_turn
        if(event.widget.cget("text") != '/'):
            return
        x = event.widget.master.grid_info()["row"] - 1
        y = event.widget.master.grid_info()["column"]
        
        if(x_turn):
            event.widget.config(text="X")
        else:
            event.widget.config(text="O")
        winner = self.tttgame.makeMove(x=x, y=y, x_turn=x_turn)

        self.shouldResetGameInstance(winner,event)

        self.setWinnerColor(winner,event)

        if(self.is_ai_playing and winner == '/'):
            print("AI plays")
            winner, x, y = self.tttgame.makeAIMove(x,y)
            self.markAIMove(event.widget.master.master,x,y)

        self.shouldResetGameInstance(winner,event)
        self.setWinnerColor(winner,event)
        if(not self.is_ai_playing):
            x_turn = not x_turn
    
    def destroyFrameContent(self, parent_frame):
        for widget in parent_frame.winfo_children():
            widget.destroy()

    def shouldResetGameInstance(self, winner, event):
        if(winner == '_'):
            master_event = event.widget.master.master
            self.destroyFrameContent(event.widget.master.master)
            self.setupGameBoard(master_event)
            self.tttgame = tttg(is_ai_playing=self.is_ai_playing,is_x_turn=self.x_turn)

    def markAIMove(self, master_event, x, y):
        label_to_change = None
        print("X = ", x)
        print("Y = ", y)
        for widget in master_event.children.values():
            if(widget.grid_info()["row"] - 1 == x and widget.grid_info()["column"] == y):
                label_to_change = widget

        for child in label_to_change.children.values():
            child.config(text="O")

        return
    def setWinnerColor(self, winner, event):
        global parent_game_board
        master_widget = event.widget.master.master
        print("TESTING OVERALL GRID DATA")
        x = master_widget.grid_info()["row"] - 1
        y = master_widget.grid_info()["column"]
        if(winner == 'X'):
            winner = parent_game_board.makeMove(x, y, x_turn=True)
            event.widget.master.master.config(bg="blue")
        elif(winner == 'O'):
            winner = parent_game_board.makeMove(x, y, x_turn=False)
            event.widget.master.master.config(bg="red")
        if(winner != '/' or winner != '_'):
            self.setOverallWinner(winner)
    
    def setOverallWinner(self, winner):
        winner_window = WinnerWindow(self, winner)
        winner_window.grab_set()

class WinnerWindow(tk.Toplevel):
    def __init__(self, parent, winner):
        super().__init__(parent)
        self.winner = winner
        self.title("We have a winner!")
        overall_game_display_frame = tk.Frame(master=self)
        overall_game_display_frame.grid()
        self.overall_game_display = tk.Label(master=overall_game_display_frame, text=f"Game ended! the winner is: {self.winner} ", font=font.Font(size=20))
        self.overall_game_display.grid()
        self.button = ttk.Button(master=overall_game_display_frame, text="Close window", command = self.destroy).grid()

window = StartWindow()
window.mainloop()