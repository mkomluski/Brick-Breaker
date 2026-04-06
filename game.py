from tkinter import Tk

from entities.ball import Ball
from entities.paddle import Paddle


class Game:
    def __init__(self):
        self.canvas = canvas
        self.paddle = Paddle()
        self.ball = Ball()
        self.tf = Tk()
        self.highscore = 0 #0 is a place holder for now, it should read the first line in the highscore.txt
        self.current_score = 0

    def run(self):
        pass

    def update_state(self):
        #The bind() should be in here i think
        pass

    def ball_out_of_bounds(self):
        pass