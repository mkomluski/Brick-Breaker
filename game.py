from tkinter import Tk
import tkinter

from entities.ball import Ball
from entities.paddle import Paddle
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

    def run(self):
        self.game_loop()
        self.tk.mainloop()

    def update_state(self, event):
        self.paddle.move(event.x)

    def ball_out_of_bounds(self):
        pass

    def game_loop(self):
        self.ball.move()
        self.tk.after(20, self.game_loop)