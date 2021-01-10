from tkinter import *
from PIL import ImageTk, Image
from alpha_beta_pruning import *

size_of_board = 660
rows = 11
cols = 11

class Game:
    def __init__(self):
        self.window = Tk()
        self.window.title("Ship-Game")
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.blue_ship = ImageTk.PhotoImage(Image.open(r"images/ship_blue.png"))
        self.red_ship = ImageTk.PhotoImage(Image.open(r"images/ship_red.png"))
        self.board = []
        #self.window.bind("<Key>",self.key_input)
        #self.window.bind("<Button_",self.mouse_input)
        self.init_board()

    def init_board(self):
        for i in range(rows):
            for j in range(cols):
                self.board.append((i, j))
        for i in range(rows):
            self.canvas.create_line(i*size_of_board/rows, 0, i*size_of_board/rows, size_of_board)
        for i in range(cols):
            self.canvas.create_line(0, i*size_of_board/cols, size_of_board, i*size_of_board/cols)
        self.canvas.create_image(300, 0, anchor=NW, image=self.red_ship)
        self.canvas.create_image(300, 600, anchor=NW, image=self.blue_ship)

    def mainloop(self):
        self.window.mainloop()

if __name__ == '__main__':
    game = Game()
    game.mainloop()

