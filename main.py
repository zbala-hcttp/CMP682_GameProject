import math
from tkinter import *
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image

width_of_canvas = 1000
height_of_canvas = 650
size_of_board = 600
rows = 11
cols = 11
lives = 3
lasers = 3
blackholes = 3
depth = 0


class Game:
    def __init__(self):
        self.window = Tk()
        self.window.title("Spaceship Game")
        self.canvas = Canvas(self.window, width=width_of_canvas, height=height_of_canvas)
        self.canvas.pack()
        self.blackhole_img = ImageTk.PhotoImage(Image.open(r"images/whirlpool.png"))
        self.blackhole_cells = []
        self.blue_ship = BattleShip(459, 536, 6, 11, ImageTk.PhotoImage(Image.open(r"images/spaceship.png")))
        self.red_ship = BattleShip(459, 34, 6, 1, ImageTk.PhotoImage(Image.open(r"images/ai_spaceship.png")))
        self.player1 = Player("You", self.blue_ship)
        self.player2 = Player("AI", self.red_ship)
        self.turn = True
        self.is_end = "None"
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
        self.canvas.create_rectangle(400, 25, 550, 75, outline="#C70039", width=1.5)
        self.canvas.create_rectangle(400, 525, 550, 575, outline="#2980B9", width=1.5)

    def draw_story(self):
        self.canvas.create_rectangle(10, 25, 180, 575)
        self.canvas.create_text(95, 38, anchor=CENTER, text="Story", fill="#0E6655", font=("Purisa", 12, "bold"))
        self.canvas.create_line(10, 50, 180, 50)
        self.canvas.create_text(13, 55, anchor=NW, fill="#138D75", font=("Purisa", 11),
                                text="Reach to the opposite\nhome before your enemy\nreaches to yours\nand win the game!"
                                     "\n\nWatch out for your\nenemy! He can send\nblackholes to your way or\nhe can sink your "
                                     "ship\nusing lasers.\n\nEach player has 3 lasers\nand 5 blackhole attacks.\n"
                                     "Lasers can be used\nwithin 3 blocks range.\n"
                                     "Spaceships can survive\nonly 3 laser attacks."
                                     "\n\nGood luck!")

    def draw_warnings(self):
        self.canvas.create_rectangle(200, 600, 750, 640)
        turn = "AI's turn"
        if self.turn:
            turn = "Your turn"
        self.canvas.create_text(475, 610, anchor=CENTER, text=turn, fill="#D81B60", font=("Purisa", 12))
        self.canvas.create_text(203, 620, anchor=NW, text="Warning >> " + self.warning_text,
                                fill="#CB4335", font=("Purisa", 12, "bold"))

    def draw_player2_info(self):
        self.canvas.create_rectangle(770, 25, 990, 275)
        self.canvas.create_text(880, 38, anchor=CENTER, text=self.player2.name, fill="#BF0238", font=("Purisa", 12, "bold"))
        self.canvas.create_line(770, 50, 990, 50)
        self.canvas.create_text(773, 55, anchor=NW, fill="#C70039", font=("Purisa", 11),
                                text="lives : " + str(self.player2.lives) +
                                     "\nblackholes : " + str(self.player2.ship.blackholes))

    def draw_player1_info(self):
        self.canvas.create_rectangle(770, 325, 990, 575)
        self.canvas.create_text(880, 338, anchor=CENTER, text=self.player1.name, fill="#1B618E", font=("Purisa", 12, "bold"))
        self.canvas.create_line(770, 350, 990, 350)
        self.canvas.create_text(773, 355, anchor=NW, fill="#2471A3", font=("Purisa", 11),
                                text="lives : " + str(self.player1.lives) +
                                     "\nblackholes : " + str(self.player1.ship.blackholes))

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
        for i in range(len(self.blackhole_cells)):
            self.canvas.create_image((self.blackhole_cells[i][0] - 1) * 50 + 209,
                                     (self.blackhole_cells[i][1] - 1) * 50 + 34,
                                     anchor=NW, image=self.blackhole_img)

    def new_game(self):
        self.turn = True
        self.player1.lives = lives
        self.player1.ship = BattleShip(459, 536, 6, 11, ImageTk.PhotoImage(Image.open(r"images/spaceship.png")))
        self.player2.lives = lives
        self.player2.ship = BattleShip(459, 34, 6, 1, ImageTk.PhotoImage(Image.open(r"images/ai_spaceship.png")))
        self.blackhole_cells = []

    def is_position_valid(self, x, y):
        if 200 <= x <= 750 and 25 <= y <= 575:
            return True

    def is_cell_empty(self, x, y):
        if self.player2.ship.cell_x == x and self.player2.ship.cell_y == y:
            return False
        for i in range(len(self.blackhole_cells)):
            if self.blackhole_cells[i][0] == x and self.blackhole_cells[i][1] == y:
                return False
        return True

    def move(self, player, cell_x, cell_y):
        if self.is_position_valid(player.ship.position_x + 50*cell_x, player.ship.position_y + 50*cell_y)\
                and self.is_cell_empty(player.ship.cell_x + cell_x, player.ship.cell_y + cell_y):
            player.ship.position_x += 50*cell_x
            player.ship.cell_x += cell_x
            player.ship.position_y += 50*cell_y
            player.ship.cell_y += cell_y
            return True
        else:
            return False

    def left_key(self, event):
        if self.turn:
            result = self.move(self.player1, -1, 0)
            if result:
                self.warning_text = ""
            else:
                self.warning_text = "This move is not valid. Try another move."
            self.turn = False
            self.update_board()
            self.has_player1_won()
            self.play()
        else:
            self.warning_text = "It is AI's turn!"
            self.update_board()

    def right_key(self, event):
        if self.turn:
            result = self.move(self.player1, 1, 0)
            if result:
                self.warning_text = ""
            else:
                self.warning_text = "This move is not valid. Try another move."
            self.turn = False
            self.update_board()
            self.has_player1_won()
            self.play()
        else:
            self.warning_text = "It is AI's turn!"
            self.update_board()

    def up_key(self, event):
        if self.turn:
            result = self.move(self.player1, 0, -1)
            if result:
                self.warning_text = ""
            else:
                self.warning_text = "This move is not valid. Try another move."
            self.turn = False
            self.update_board()
            self.has_player1_won()
            self.play()
        else:
            self.warning_text = "It is AI's turn!"
            self.update_board()

    def down_key(self, event):
        if self.turn:
            result = self.move(self.player1, 0, 1)
            if result:
                self.warning_text = ""
            else:
                self.warning_text = "This move is not valid. Try another move."
            self.turn = False
            self.update_board()
            self.play()
        else:
            self.warning_text = "It is AI's turn!"
            self.update_board()

    def space_key(self, event):
        if self.turn and self.player1.lives > 0:
            self.send_laser(self.player1, self.player2)
            self.turn = False
            self.play()
        else:
            self.warning_text = "It is AI's turn!"
            self.update_board()

    def has_player1_won(self):
        if (400 < self.player1.ship.position_x < 550 and 25 < self.player1.ship.position_y < 75) \
                or self.player2.is_out_of_lives():
            self.is_end = "You"
            self.player_won()

    def has_player2_won(self):
        if (400 < self.player2.ship.position_x < 550 and 525 < self.player2.ship.position_y < 575) \
                or self.player1.is_out_of_lives():
            self.is_end = "AI"
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
        distance = math.sqrt(sum((px - qx) ** 2.0 for px, qx
                                 in zip([self.player1.ship.position_x, self.player1.ship.position_y],
                                        [self.player2.ship.position_x, self.player2.ship.position_y])))
        return distance

    def send_laser(self, from_player, to_player):
        if from_player.is_out_of_lives() or to_player.is_out_of_lives():
            print()
        elif self.is_close(from_player, to_player):
            self.canvas.create_line(from_player.ship.position_x, from_player.ship.position_y,
                                    to_player.ship.position_x, to_player.ship.position_y,
                                    fill="yellow", width=3)
            from_player.ship.lasers -= 1
            to_player.lives -= 1
            self.has_player1_won()
            self.has_player2_won()

    def put_blackhole(self, player, x, y):
        if player.is_out_of_lives():
            return False
        if (x == self.player1.ship.cell_x and y == self.player1.ship.cell_y)\
                or (x == self.player2.ship.cell_x and y == self.player2.ship.cell_y):
            return False
        else:
            if player.ship.blackholes > 0:
                for i in range(len(self.blackhole_cells)):
                    if self.blackhole_cells[i][0] == x and self.blackhole_cells[i][1] == y:
                        return False
                player.ship.blackholes -= 1
                return True
            return False

    def mouse_click(self, event):
        if self.turn:
            widget = event.widget
            xc = math.ceil((widget.canvasx(event.x) - 200) / 50)
            yc = math.ceil((widget.canvasy(event.y) - 25) / 50)
            if (xc == self.player1.ship.cell_x and yc == self.player1.ship.cell_y)\
                    or (xc == self.player2.ship.cell_x and yc == self.player2.ship.cell_y)\
                        or (not self.is_position_valid(event.x, event.y)):
                self.warning_text = "Illegal place to send blackhole! Please send another cell."
            else:
                if self.player1.ship.blackholes > 0:
                    for i in range(len(self.blackhole_cells)):
                        if self.blackhole_cells[i][0] == xc and self.blackhole_cells[i][1] == yc:
                            self.warning_text = "There is already a blackhole here!"
                            self.update_board()
                            return
                    self.warning_text = ""
                    self.blackhole_cells.append((xc, yc))
                    self.player1.ship.blackholes -= 1
                    self.turn = False
                    self.update_board()
                    self.play()
                else:
                    self.warning_text = "You have run out of blackholes!"
                    self.update_board()
        else:
            self.warning_text = "It is AI's turn!"
            self.update_board()

    def calculate_euclidean_distance_of_ships(self):
        distance = math.sqrt(sum((px - qx) ** 2.0 for px, qx
                                 in zip([self.player1.ship.position_x, self.player1.ship.position_y],
                                        [self.player2.ship.position_x, self.player2.ship.position_y])))
        return distance

    def is_close(self, from_player, to_player):
        if self.calculate_euclidean_distance_of_ships() < 200 \
                        and from_player.ship.has_lasers:
            return True
        return False

    def has_ended(self):
        if (400 < self.player1.ship.position_x < 550 and 25 < self.player1.ship.position_y < 75) \
                or self.player2.is_out_of_lives():
            return "You"
        if (400 < self.player2.ship.position_x < 550 and 525 < self.player2.ship.position_y < 575) \
                or self.player1.is_out_of_lives():
            return "AI"
        return "None"

    def max_alpha_beta(self, alpha, beta):
        maxv = -2
        action = ""
        cell_x = 0
        cell_y = 0
        global depth
        depth += 1
        result = self.has_ended()

        if result == "AI" or self.player1.is_out_of_lives():
            return (1, "nothing", 0, 0)
        elif result == "You" or self.player2.is_out_of_lives():
            return (-1, "nothing", 0, 0)
        elif depth >= 1000:
            return (0, "nothing", 0, 0)

        if self.is_close(self.player2, self.player1):
            print("laser AI")
            self.player2.ship.lasers -= 1
            self.player1.lives -= 1
            action = "laser"
            (m, a, x, y) = self.min_alpha_beta(alpha, beta)
            print(str(m) + " " + str(alpha) + " " + str(beta))
            if m > maxv:
                maxv = m
                action = a
                cell_x = x
                cell_y = y
            self.player2.ship.lasers += 1
            self.player1.lives += 1
            if maxv >= beta:
                return (maxv, action, cell_x, cell_y)
            if maxv > alpha:
                alpha = maxv

        for i in [0, -1, 1]:
            for j in [1, 0]:
                if i == j or i == -j:
                    continue
                if self.move(self.player2, i, j):
                    print("AI move "+ str(i) + " " + str(j))
                    action = "move"
                    cell_x = i
                    cell_y = j
                    (m, a, x, y) = self.min_alpha_beta(alpha, beta)
                    if m > maxv:
                        maxv = m
                        action = a
                        cell_x = x
                        cell_y = y
                    self.move(self.player2, -i, -j)
                    if maxv >= beta:
                        return (maxv, action, cell_x, cell_y)
                    if maxv > alpha:
                        alpha = maxv

        for i in range(1, 12):
            for j in range(1, 12):
                if (j == 1 and (i == 5 or i == 6 or i == 7)) or \
                        (j == 11 and (i == 5 or i == 6 or i == 7)):
                    continue
                if self.put_blackhole(self.player2, i, j):
                    self.blackhole_cells.append((i, j))
                    action = "blackhole"
                    cell_x = i
                    cell_y = j
                    (m, a, x, y) = self.min_alpha_beta(alpha, beta)
                    if m > maxv:
                        maxv = m
                        action = a
                        cell_x = x
                        cell_y = y
                    self.blackhole_cells.pop()
                    self.player2.ship.blackholes += 1
                    if maxv >= beta:
                        return (maxv, action, cell_x, cell_y)
                    if maxv > alpha:
                        alpha = maxv

        return (maxv, action, cell_x, cell_y)

    def min_alpha_beta(self, alpha, beta):
        minv= 2
        action = ""
        x = 0
        y = 0
        global depth
        depth += 1
        result = self.has_ended()
        if result == "AI":
            return (1, "nothing", 0, 0)
        elif result == "You":
            return (-1, "nothing", 0, 0)
        elif depth >= 1000:
            return (0, "nothing", 0, 0)

        if self.is_close(self.player1, self.player2):
            action = "laser"
            self.player1.ship.lasers -= 1
            self.player2.lives -= 1
            (m, a, x, y) = self.max_alpha_beta(alpha, beta)
            if m < minv:
                minv = m
                action = a
                cell_x = x
                cell_y = y
            self.player1.ship.lasers += 1
            self.player2.lives += 1
            if minv <= alpha:
                return (minv, action, cell_x, cell_y)
            if minv < beta:
                beta = minv

        for i in [0, -1, 1]:
            for j in [-1, 0]:
                if i == j or i == -j:
                    continue
                if self.move(self.player1, i, j):
                    action = "move"
                    cell_x = i
                    cell_y = j
                    (m, a, x, y) = self.max_alpha_beta(alpha, beta)
                    if m < minv:
                        minv = m
                        action = a
                        cell_x = x
                        cell_y = y
                    self.move(self.player1, -i, -j)
                    if minv <= alpha:
                        return (minv, action, cell_x, cell_y)
                    if minv < beta:
                        beta = minv

        for i in range(1, 12):
            for j in range(1, 12):
                if self.put_blackhole(self.player1, i, j):
                    action = "blackhole"
                    cell_x = i
                    cell_y = j
                    self.blackhole_cells.append((i, j))
                    (m, a, x, y) = self.max_alpha_beta(alpha, beta)
                    if m < minv:
                        minv = m
                        action = a
                        cell_x = x
                        cell_y = y
                    self.blackhole_cells.pop()
                    self.player1.ship.blackholes += 1
                    if minv <= alpha:
                        return (minv, action, cell_x, cell_y)
                    if minv < beta:
                        beta = minv

        return (minv, action, cell_x, cell_y)

    def play(self):
        (minv, action, x, y) = self.max_alpha_beta(-2, 2)
        if action == "laser":
            self.send_laser(self.player2, self.player1)
        elif action == "move":
            self.move(self.player2, x, y)
        elif action == "blackhole":
            self.blackhole_cells.append((x, y))
        print(action+ " " + str(x)+ " "+str(y))
        self.turn = True
        self.update_board()
        self.has_player2_won()

    def mainloop(self):
        self.window.mainloop()


class BattleShip:

    def __init__(self, position_x, position_y, cell_x, cell_y, image):
        self.position_x = position_x
        self.position_y = position_y
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.lasers = lasers
        self.blackholes = blackholes
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
