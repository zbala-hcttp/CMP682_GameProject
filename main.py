from tkinter import *
from PIL import ImageTk, Image
from alpha_beta_pruning import *

width_of_canvas = 1000
height_of_canvas = 650
size_of_board = 600
rows = 11
cols = 11
lives = 3
lasers = 3
whirlpools = 3


class Game:
    def __init__(self):
        self.window = Tk()
        self.window.title("Ship-Game")
        self.canvas = Canvas(self.window, width=width_of_canvas, height=height_of_canvas)
        self.canvas.pack()
        self.blue_ship = BattleShip(459, 536, ImageTk.PhotoImage(Image.open(r"images/ship_blue.png")))
        self.red_ship = BattleShip(459, 34, ImageTk.PhotoImage(Image.open(r"images/ship_red.png")))
        self.player1 = Player("You", self.blue_ship)
        self.player2 = Player("AI", self.red_ship)
        self.board = []
        self.window.bind('<Left>', self.left_key)
        self.window.bind('<Right>', self.right_key)
        self.window.bind('<Up>', self.up_key)
        self.window.bind('<Down>', self.down_key)
        self.window.bind('<Return>', self.enter_key)
        self.window.bind('<space>', self.space_key)
        self.warning_text = ""
        self.init_board()
        self.init_story()
        self.init_warnings()
        self.init_player1_info()
        self.init_player2_info()

    def init_board(self):
        self.draw_board()
        self.place_ships()

    def draw_board(self):
        for i in range(rows):
            for j in range(cols):
                self.board.append((i, j))
        for i in range(cols+1):
            self.canvas.create_line(i * size_of_board / (cols+1) + 200, 25,
                                    i * size_of_board / (cols+1) + 200, size_of_board - 25)

        for i in range(rows+1):
            self.canvas.create_line(200, i * size_of_board / (rows+1) + 25, size_of_board + 150,
                                    i * size_of_board / (rows+1) + 25)

    def init_story(self):
        self.draw_story()

    def draw_story(self):
        self.canvas.create_rectangle(10, 25, 180, 575)
        self.canvas.create_text(95, 38, anchor=CENTER, text="Story", fill="blue", font=("Purisa", 12))
        self.canvas.create_line(10, 50, 180, 50)
        self.canvas.create_text(13, 55, anchor=NW, fill="green", font=("Purisa", 11),
                                text="Enemy is waiting to sink\nyour ship! You need "
                                     "to be\naware to the laser attacks\nfrom the enemy "
                                     "and the\nwhirlpools. You have 3\nblocks range to shoot "
                                     "the\nenemy ship with your\nlaser and 5 whirlpool\nattacks."
                                     "You have only 3\nchances to withstand the\nlaser attacks."
                                     "Reach his\nport before he reaches\nyours and win the game!")

    def init_warnings(self):
        self.draw_warnings()

    def draw_warnings(self):
        self.canvas.create_rectangle(200, 600, 750, 640)
        self.canvas.create_text(203, 603, anchor=NW, text="Warning >> " + self.warning_text,
                                fill="red", font=("Purisa", 12))

    def init_player2_info(self):
        self.draw_player2_info()

    def draw_player2_info(self):
        self.canvas.create_rectangle(770, 25, 990, 275)
        self.canvas.create_text(880, 38, anchor=CENTER, text=self.player2.name, fill="red", font=("Purisa", 12))
        self.canvas.create_line(770, 50, 990, 50)
        self.canvas.create_text(773, 55, anchor=NW, fill="red", font=("Purisa", 11),
                                text="lives : " + str(self.player2.ship.lives) +
                                     "\nwhirlpools : " + str(self.player2.ship.whirlpools))

    def init_player1_info(self):
        self.draw_player1_info()

    def draw_player1_info(self):
        self.canvas.create_rectangle(770, 325, 990, 575)
        self.canvas.create_text(880, 338, anchor=CENTER, text=self.player1.name, fill="blue", font=("Purisa", 12))
        self.canvas.create_line(770, 350, 990, 350)
        self.canvas.create_text(773, 355, anchor=NW, fill="blue", font=("Purisa", 11),
                                text="lives : " + str(self.player1.ship.lives) +
                                     "\nwhirlpools : " + str(self.player1.ship.whirlpools))

    def place_ships(self):
        self.canvas.create_image(self.player1.ship.position_x, self.player1.ship.position_y, anchor=NW,
                                 image=self.player1.ship.image)
        self.canvas.create_image(self.player2.ship.position_x, self.player2.ship.position_y, anchor=NW,
                                 image=self.player2.ship.image)

    def update_board(self):
        self.canvas.delete("all")
        self.draw_board()
        self.place_ships()
        self.draw_story()
        self.draw_warnings()
        self.draw_player1_info()
        self.draw_player2_info()

    def is_position_valid(self, x, y):
        if 200 <= x <= 750 and 25 <= y <= 575:
            return True

    def is_there_a_blackhole(self):
        return False

    def left_key(self, event):
        if self.is_position_valid(self.player1.ship.position_x - 50, self.player1.ship.position_y):
            self.player1.ship.position_x -= 50
            self.warning_text = ""
        else:
            self.warning_text = "This move is not valid. Try another move."
            print("This move is not valid. Try another move.")
        self.update_board()

    def right_key(self, event):
        if self.is_position_valid(self.player1.ship.position_x + 50, self.player1.ship.position_y):
            self.warning_text = ""
            self.player1.ship.position_x += 50
        else:
            self.warning_text = "This move is not valid. Try another move."
            print("This move is not valid. Try another move.")
        self.update_board()

    def up_key(self, event):
        if self.is_position_valid(self.player1.ship.position_x, self.player1.ship.position_y - 50):
            self.warning_text = ""
            self.player1.ship.position_y -= 50
        else:
            self.warning_text = "This move is not valid. Try another move."
            print("This move is not valid. Try another move.")
        self.update_board()

    def down_key(self, event):
        if self.is_position_valid(self.player1.ship.position_x, self.player1.ship.position_y + 50):
            self.warning_text = ""
            self.player1.ship.position_y += 50
        else:
            self.warning_text = "This move is not valid. Try another move."
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
        self.lasers = lasers
        self.whirlpools = whirlpools
        self.image = image

    def is_out_of_lives(self):
        return self.lives == 0

    def is_out_of_lasers(self):
        return self.lasers == 0


class Player:
    def __init__(self, name, ship):
        self.name = name
        self.ship = ship


if __name__ == '__main__':
    game = Game()
    game.mainloop()
