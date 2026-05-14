from tkinter import Tk
import tkinter

from entities.ball import Ball
from entities.paddle import Paddle
from entities.brick import Brick
from levels.level_manager import LevelManager
from utils.constants import *
from levels.level_data import level
from collections import namedtuple

Point= namedtuple("Point", ["x", "y"])

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
        self.level_manager = LevelManager([level])
        self.bricks = []
        self.load_levels()

    def run(self):
        self.game_loop()
        self.tk.mainloop()

    def update_state(self, event):
        self.paddle.move(event.x)

    def ball_out_of_bounds(self):
        pass

    def game_loop(self):
        self.ball.move()

        #Collision with paddle
        if(self.check_collisions(self.ball.get_rect(), self.paddle.get_rect()) and self.ball.speed_y > 0):
            self.ball.set_speed(self.ball.speed_x, -self.ball.speed_y)

        #Collision with bricks
        any_collision = False
        for brick in self.bricks:
            if(self.check_collisions(self.ball.get_rect(), brick.get_rect()) and not self.ball.in_collision):
                self.ball.in_collision = True
                any_collision = True

                # From which side the ball is colliding with the brick
                overlap_ball = self.ball.get_rect()
                overlap_brick = brick.get_rect()
                ball_center_x = (overlap_ball[0] + overlap_ball[2]) / 2
                ball_center_y = (overlap_ball[1] + overlap_ball[3]) / 2
                brick_center_x = (overlap_brick[0] + overlap_brick[2]) / 2
                brick_center_y = (overlap_brick[1] + overlap_brick[3]) / 2

                dx = ball_center_x - brick_center_x
                dy = ball_center_y - brick_center_y

                half_w = (overlap_brick[2] - overlap_brick[0]) / 2
                half_h = (overlap_brick[3] - overlap_brick[1]) / 2

                if abs(dx / half_w) > abs(dy / half_h):
                    self.ball.set_speed(-self.ball.speed_x, self.ball.speed_y)
                else:
                    self.ball.set_speed(self.ball.speed_x, -self.ball.speed_y)

                res = brick.update_state()
                if res:
                    self.bricks.remove(brick)
                break

        if not any_collision:
            self.ball.in_collision = False

        self.tk.after(20, self.game_loop)

    def check_collisions(self, rect1, rect2):
        return not (rect1[2] < rect2[0] or rect1[0] > rect2[2] or rect1[3] < rect2[1] or rect1[1] > rect2[3])

    def load_levels(self):
        response = self.level_manager.load_next_level()
        if not response:
            print("No more levels to load.")
            return
        for row_index, row in enumerate(response.brick_layout):
            for col_index, type in enumerate(row):
                if type != None:
                    position = Point(col_index * (BRICK_WIDTH+BRICK_GAP), row_index * (BRICK_HEIGHT+BRICK_GAP))
                    self.bricks.append(Brick(self.canvas, type, position))