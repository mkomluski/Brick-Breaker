from tkinter import Tk
import tkinter

from entities.ball import Ball
from entities.paddle import Paddle
from entities.brick import Brick
from levels.level_manager import LevelManager
from utils.constants import *


class Game:
    def __init__(self):
        self.tk = Tk()
        self.canvas = tkinter.Canvas(self.tk, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background=BG_COLOR)
        self.canvas.pack()
        self.canvas.bind("<Motion>", self.update_state)
        self.paddle = Paddle(self.canvas, CANVAS_WIDTH//2)
        self.ball = Ball(self.canvas, CANVAS_WIDTH//2)
        self.highscore = 0 #0 is a place holder for now, it should read the first line in the highscore.txt
        self.current_score = 0
        self.level_manager = LevelManager()

    def run(self):
        self.game_loop()
        self.tk.mainloop()

    def update_state(self, event):
        self.paddle.move(event.x)

    def ball_out_of_bounds(self):
        pass

    def game_loop(self):
        self.ball.move()
        if(self.check_collisions(self.ball.get_rect(), self.paddle.get_rect()) and self.ball.speed_y > 0):
            self.ball.set_speed(self.ball.speed_x, -self.ball.speed_y)
        self.tk.after(20, self.game_loop)

    def check_collisions(self, rect1, rect2):
        return not (rect1[2] < rect2[0] or rect1[0] > rect2[2] or rect1[3] < rect2[1] or rect1[1] > rect2[3])