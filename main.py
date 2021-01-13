import math
from tkinter import *
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image
from alpha_beta_pruning import *

width_of_canvas = 1000
height_of_canvas = 650
size_of_board = 600
rows = 11
cols = 11
lives = 3
lasers = 3
whirlpools = 5
bombs = 3


class Game:
    def __init__(self):
        self.window = Tk()
        self.window.title("Ship-Game")
        self.canvas = Canvas(self.window, width=width_of_canvas, height=height_of_canvas)
        self.canvas.pack()
        self.whirlpool_img = ImageTk.PhotoImage(Image.open(r"images/whirlpool.png"))
        self.whirlpool_cells = []
        self.blue_ship = BattleShip(459, 536, 6, 11, ImageTk.PhotoImage(Image.open(r"images/ship_blue.png")))
        self.red_ship = BattleShip(459, 34, 6, 1, ImageTk.PhotoImage(Image.open(r"images/ship_red.png")))
        self.player1 = Player("You", self.blue_ship)
        self.player2 = Player("AI", self.red_ship)
        self.board = []
        self.window.bind('<Left>', self.left_key)
        self.window.bind('<Right>', self.right_key)
        self.window.bind('<Up>', self.up_key)
        self.window.bind('<Down>', self.down_key)
        # self.window.bind('<Return>', self.enter_key)
        self.window.bind('<space>', self.space_key)
        self.window.bind("<Button-1>", self.mouse_click)
        self.warning_text = ""
        self.init_board()

    def init_board(self):
        self.canvas.delete("all")
        self.draw_board()
        self.place_ships()
        self.draw_story()
        self.draw_warnings()
        self.draw_player1_info()
        self.draw_player2_info()

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
        self.canvas.create_rectangle(400, 25, 550, 75, outline="red", width=1.5)
        self.canvas.create_rectangle(400, 525, 550, 575, outline="blue", width=1.5)

    def draw_story(self):
        self.canvas.create_rectangle(10, 25, 180, 575)
        self.canvas.create_text(95, 38, anchor=CENTER, text="Story", fill="blue", font=("Purisa", 12))
        self.canvas.create_line(10, 50, 180, 50)
        self.canvas.create_text(13, 55, anchor=NW, fill="green", font=("Purisa", 11),
                                text="Reach to the opposite\nport before your enemy\nreaches to yours\nand win the game!"
                                     "\n\nWatch out for your\nenemy! He can send\nwhirpools to your way or\nhe can sink your "
                                     "ship\nusing lasers.\n\nEach player has 3 lasers\nand 5 whirlpool attacks.\n"
                                     "Lasers can be used\nwithin 3 blocks range.\n"
                                     "Ships can survive only\n3 laser attacks."
                                     "\n\nGood luck!")

    def draw_warnings(self):
        self.canvas.create_rectangle(200, 600, 750, 640)
        self.canvas.create_text(203, 603, anchor=NW, text="Warning >> " + self.warning_text,
                                fill="red", font=("Purisa", 12))

    def draw_player2_info(self):
        self.canvas.create_rectangle(770, 25, 990, 275)
        self.canvas.create_text(880, 38, anchor=CENTER, text=self.player2.name, fill="red", font=("Purisa", 12))
        self.canvas.create_line(770, 50, 990, 50)
        self.canvas.create_text(773, 55, anchor=NW, fill="red", font=("Purisa", 11),
                                text="lives : " + str(self.player2.lives) +
                                     "\nwhirlpools : " + str(self.player2.ship.whirlpools))

    def draw_player1_info(self):
        self.canvas.create_rectangle(770, 325, 990, 575)
        self.canvas.create_text(880, 338, anchor=CENTER, text=self.player1.name, fill="blue", font=("Purisa", 12))
        self.canvas.create_line(770, 350, 990, 350)
        self.canvas.create_text(773, 355, anchor=NW, fill="blue", font=("Purisa", 11),
                                text="lives : " + str(self.player1.lives) +
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
        for i in range(len(self.whirlpool_cells)):
            self.canvas.create_image((self.whirlpool_cells[i][0] - 1) * 50 + 209,
                                     (self.whirlpool_cells[i][1] - 1) * 50 + 34,
                                     anchor=NW, image=self.whirlpool_img)

    def new_game(self):
        self.player1.lives = lives
        self.player1.ship = BattleShip(459, 536, 6, 11, ImageTk.PhotoImage(Image.open(r"images/ship_blue.png")))
        self.player2.lives = lives
        self.player2.ship = BattleShip(459, 34, 6, 1, ImageTk.PhotoImage(Image.open(r"images/ship_red.png")))
        self.whirlpool_cells = []

    def is_position_valid(self, x, y):
        if 200 <= x <= 750 and 25 <= y <= 575:
            return True

    def is_cell_empty(self, x, y):
        if self.player2.ship.cell_x == x and self.player2.ship.cell_y == y:
            return False
        for i in range(len(self.whirlpool_cells)):
            if self.whirlpool_cells[i][0] == x and self.whirlpool_cells[i][1] == y:
                return False
        return True

    def left_key(self, event):
        if self.is_position_valid(self.player1.ship.position_x - 50, self.player1.ship.position_y)\
                and self.is_cell_empty(self.player1.ship.cell_x - 1, self.player1.ship.cell_y):
            self.player1.ship.position_x -= 50
            self.player1.ship.cell_x -=1
            self.warning_text = ""
        else:
            self.warning_text = "This move is not valid. Try another move."
        self.update_board()
        self.has_player1_won()

    def right_key(self, event):
        if self.is_position_valid(self.player1.ship.position_x + 50, self.player1.ship.position_y)\
                and self.is_cell_empty(self.player1.ship.cell_x + 1, self.player1.ship.cell_y):
            self.player1.ship.position_x += 50
            self.player1.ship.cell_x += 1
            self.warning_text = ""
        else:
            self.warning_text = "This move is not valid. Try another move."
        self.update_board()
        self.has_player1_won()

    def up_key(self, event):
        if self.is_position_valid(self.player1.ship.position_x, self.player1.ship.position_y - 50)\
                and self.is_cell_empty(self.player1.ship.cell_x, self.player1.ship.cell_y - 1):
            self.player1.ship.position_y -= 50
            self.player1.ship.cell_y -= 1
            self.warning_text = ""
        else:
            self.warning_text = "This move is not valid. Try another move."
        self.update_board()
        self.has_player1_won()

    def down_key(self, event):
        if self.is_position_valid(self.player1.ship.position_x, self.player1.ship.position_y + 50)\
                and self.is_cell_empty(self.player1.ship.cell_x, self.player1.ship.cell_y + 1):
            self.player1.ship.position_y += 50
            self.player1.ship.cell_y += 1
            self.warning_text = ""
        else:
            self.warning_text = "This move is not valid. Try another move."
        self.update_board()

    def space_key(self, event):
        self.send_laser(self.player1, self.player2)

    def has_player1_won(self):
        if (400 < self.player1.ship.position_x < 550 and 25 < self.player1.ship.position_y < 75) or self.player2.is_out_of_lives():
            self.player_won()

    def has_player2_won(self):
        if (400 < self.player2.ship.position_x < 550 and 525 < self.player2.ship.position_y < 575) or self.player1.is_out_of_lives():
            self.player_lost()

    def player_won(self):
        showinfo("Game Over", "YOU WON!")
        self.new_game()
        self.init_board()

    def player_lost(self):
        showinfo("Game Over", "YOU LOST!")
        self.new_game()
        self.init_board()

    def calculate_euclidean_distance_of_ships(self):
        distance = math.sqrt(sum((px - qx) ** 2.0 for px, qx in zip([self.player1.ship.position_x, self.player1.ship.position_y],
                                                                    [self.player2.ship.position_x, self.player2.ship.position_y])))
        return distance

    def send_laser(self, from_player, to_player):
        if self.calculate_euclidean_distance_of_ships() < 200 and from_player.ship.has_lasers:
            self.canvas.create_line(from_player.ship.position_x, from_player.ship.position_y,
                                    to_player.ship.position_x, to_player.ship.position_y,
                                    fill="yellow", width=3)
            from_player.ship.lasers -= 1
            to_player.lives -= 1
            self.has_player1_won()
            self.has_player2_won()

    # def laser_effect(self, player1, player2):
    #     distance = math.dist([player1.ship.position_x, player1.ship.position_y],
    #                          [player2.ship.position_x, player2.ship.position_y])
    #     ratio = 50 / distance
    #     laser_line = self.canvas.create_line(player1.ship.position_x, player1.ship.position_y,
    #                                          player1.ship.position_x + ratio * (player2.ship.position_x - player1.ship.position_x),
    #                                          player1.ship.position_y + ratio * (player2.ship.position_y - player1.ship.position_y),
    #                                          fill="yellow", width=3)
    #     print(player1.ship.position_x)
    #     print(player2.ship.position_x)
    #     self.canvas.move(laser_line, 50, 0)

    def mouse_click(self, event):
        widget = event.widget
        xc = math.ceil((widget.canvasx(event.x) - 200) / 50)
        yc = math.ceil((widget.canvasy(event.y) - 25) / 50)
        if (xc == self.player1.ship.cell_x and yc == self.player1.ship.cell_y)\
                or (xc == self.player2.ship.cell_x and yc == self.player2.ship.cell_y)\
                    or (not self.is_position_valid(event.x, event.y)):
            self.warning_text = "Illegal place to send whirlpool! Please send another cell."
        else:
            if self.player1.ship.whirlpools > 0:
                for i in range(len(self.whirlpool_cells)):
                    if self.whirlpool_cells[i][0] == xc and self.whirlpool_cells[i][1] == yc:
                        self.warning_text = "There is already a whirlpool here!"
                        self.update_board()
                        return
                self.warning_text = ""
                self.whirlpool_cells.append((xc, yc))
                self.player1.ship.whirlpools -= 1
            else:
                self.warning_text = "You have run out of whirlpools!"
        self.update_board()

    def mainloop(self):
        self.window.mainloop()


class BattleShip:

    def __init__(self, position_x, position_y, cell_x, cell_y, image):
        self.position_x = position_x
        self.position_y = position_y
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.lasers = lasers
        self.whirlpools = whirlpools
        self.image = image

    def has_lasers(self):
        return self.lasers > 0


class Player:
    def __init__(self, name, ship):
        self.name = name
        self.ship = ship
        self.lives = lives

    def is_out_of_lives(self):
        return self.lives == 0


if __name__ == '__main__':
    game = Game()
    game.mainloop()
