from tkinter import *
from PIL import ImageTk, Image
from alpha_beta_pruning import *

size_of_board = 660
rows = 11
cols = 11
lives = 3
lazers = 3
blackholes = 3


class Game:
    def __init__(self):
        self.window = Tk()
        self.window.title("Ship-Game")
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.blue_ship = BattleShip(300, 600, ImageTk.PhotoImage(Image.open(r"images/ship_blue.png")))
        self.red_ship = BattleShip(300, 0, ImageTk.PhotoImage(Image.open(r"images/ship_red.png")))
        self.player1 = Player("You", self.blue_ship)
        self.player2 = Player("AI", self.red_ship)
        self.board = []
        self.window.bind('<Left>', self.left_key)
        self.window.bind('<Right>', self.right_key)
        self.window.bind('<Up>', self.up_key)
        self.window.bind('<Down>', self.down_key)
        self.window.bind('<Return>', self.enter_key)
        self.window.bind('<space>', self.space_key)
        #self.window.bind("<Key>",self.key_input)
        #self.window.bind("<Button_",self.mouse_input)
        self.init_board()

    def init_board(self):
        self.draw_board()
        self.place_ships()

    def draw_board(self):
        for i in range(rows):
            for j in range(cols):
                self.board.append((i, j))
        for i in range(rows):
            self.canvas.create_line(i * size_of_board / rows, 0, i * size_of_board / rows, size_of_board)
        for i in range(cols):
            self.canvas.create_line(0, i * size_of_board / cols, size_of_board, i * size_of_board / cols)

    def place_ships(self):
        self.canvas.create_image(self.player1.ship.position_x, self.player1.ship.position_y, anchor=NW,
                                 image=self.player1.ship.image)
        self.canvas.create_image(self.player2.ship.position_x, self.player2.ship.position_y, anchor=NW,
                                 image=self.player2.ship.image)

    def update_board(self):
        self.canvas.delete("all")
        self.draw_board()
        self.place_ships()

    def is_position_valid(self, x, y):
        if 0 <= x <= 600 and 0 <= y <= 600:
            return True

    def is_there_a_blackhole(self):
        return False

    def left_key(self, event):
        if self.is_position_valid(self.player1.ship.position_x - 60, self.player1.ship.position_y):
            self.player1.ship.position_x -= 60
        else:
            print("This move is not valid. Try another move.")
        self.update_board()

    def right_key(self, event):
        if self.is_position_valid(self.player1.ship.position_x + 60, self.player1.ship.position_y):
            self.player1.ship.position_x += 60
        else:
            print("This move is not valid. Try another move.")
        self.update_board()

    def up_key(self, event):
        if self.is_position_valid(self.player1.ship.position_x, self.player1.ship.position_y - 60):
            self.player1.ship.position_y -= 60
        else:
            print("This move is not valid. Try another move.")
        self.update_board()

    def down_key(self, event):
        if self.is_position_valid(self.player1.ship.position_x, self.player1.ship.position_y + 60):
            self.player1.ship.position_y += 60
        else:
            print("This move is not valid. Try another move.")
        self.update_board()

    def enter_key(self, event):
        print("Enter key pressed")

    def space_key(self, event):
        print("Space key pressed")

    def mainloop(self):
        self.window.mainloop()


class BattleShip:

    def __init__(self, position_x, position_y, image):
        self.position_x = position_x
        self.position_y = position_y
        self.lives = lives
        self.lazers = lazers
        self.image = image

    def is_out_of_lives(self):
        return self.lives == 0

    def is_out_of_lazers(self):
        return self.lazers == 0


class Player:
    def __init__(self, name, ship):
        self.name = name
        self.ship = ship


if __name__ == '__main__':
    game = Game()
    game.mainloop()
