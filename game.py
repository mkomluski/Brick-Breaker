import tkinter
import os

from collections import namedtuple, deque
from tkinter import Tk

from entities.ball import Ball
from entities.brick import Brick
from entities.paddle import Paddle
from levels.level_manager import LevelManager
from utils.constants import *
from utils.enums import BrickState, BrickType, GameState

Point = namedtuple("Point", ["x", "y"])


class Game:
    def __init__(self):
        self.ball = None
        self.paddle = None
        self.tk = Tk()
        self.canvas = tkinter.Canvas(self.tk, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background=BG_COLOR)
        self.canvas.pack()
        self.score_text = None
        self.highscore = 0  # 0 is a placeholder for now, it should read the first line in the highscore.txt
        self.current_score = 0
        self.level_manager = LevelManager()
        self.bricks = []
        self.game_state = GameState.START
        self.start_screen_items = []
        self.transition_screen_items = []
        self.game_over_screen_items = []
        self.continuing = os.path.exists("data/save.txt")
        self.lives = PLAYER_LIVES

    def run(self):
        self.start_screen()
        self.game_loop()
        self.tk.mainloop()

    def update_state(self, event):
        self.paddle.move(event.x)

    def game_loop(self):
        if self.game_state == GameState.PLAYING:
            self.ball.move()

            # Collision with paddle
            if self.check_collisions(self.ball.get_rect(), self.paddle.get_rect()) and self.ball.speed_y > 0:
                ball_rect = self.ball.get_rect()
                paddle_rect = self.paddle.get_rect()

                ball_center_x = (ball_rect[0] + ball_rect[2]) / 2
                paddle_center_x = (paddle_rect[0] + paddle_rect[2]) / 2
                paddle_half_width = (paddle_rect[2] - paddle_rect[0]) / 2

                offset = max(-0.6, min(0.6, (ball_center_x - paddle_center_x) / paddle_half_width))

                speed = (self.ball.speed_x ** 2 + self.ball.speed_y ** 2) ** 0.5
                new_speed_x = offset * speed
                new_speed_y = -(speed ** 2 - new_speed_x ** 2) ** 0.5

                self.ball.set_speed(new_speed_x, new_speed_y)

            # Collision with bricks
            any_collision = False
            for brick in self.bricks:
                if self.check_collisions(self.ball.get_rect(), brick.get_rect()) and not self.ball.in_collision:
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
                    if res == BrickState.DESTROYED:
                        self.handle_scoring(brick.type)
                        self.bricks.remove(brick)
                        if brick.type == BrickType.EXPLODING:
                            self.handle_explosion(brick)
                    break

            if not any_collision:
                self.ball.in_collision = False
            
            if self.ball.get_rect()[3] > CANVAS_HEIGHT:
                self.ball_out_of_bounds()
            elif not any(brick.type != BrickType.INDESTRUCTIBLE for brick in self.bricks):
                self.game_state = GameState.TRANSITION
                self.transition_screen()

        self.tk.after(20, self.game_loop)

    def ball_out_of_bounds(self):
        self.lives -= 1
        if self.lives == 0:
            self.game_state = GameState.GAME_OVER
            self.game_over_screen()
        else:
            self.ball.reset()

    def start_screen(self):
        title = self.canvas.create_text(CANVAS_WIDTH // 2, 150, text="Brick Breaker", font=("Arial", 42, "bold"),
                                        fill="WHITE")
        if not self.continuing:
            play_text = self.canvas.create_text(CANVAS_WIDTH // 2, 300, text="Play", font=("Arial", 20), fill="WHITE")
        else:
            play_text = self.canvas.create_text(CANVAS_WIDTH // 2, 300, text="Continue Playing", font=("Arial", 20), fill="WHITE")
        highscore_text = self.canvas.create_text(CANVAS_WIDTH // 2, 360, text="High Score", font=("Arial", 20), fill="WHITE")
        exit_text = self.canvas.create_text(CANVAS_WIDTH // 2, 420, text="Exit", font=("Arial", 20), fill="WHITE")

        self.canvas.tag_bind(play_text, "<Button-1>", self.on_play_click)
        self.canvas.tag_bind(highscore_text, "<Button-1>", self.on_highscore_click)
        self.canvas.tag_bind(exit_text, "<Button-1>", self.on_exit_click)

        self.start_screen_items.append(title)
        self.start_screen_items.append(play_text)
        self.start_screen_items.append(highscore_text)
        self.start_screen_items.append(exit_text)

    def on_play_click(self, event):
        for item in self.start_screen_items:
            self.canvas.delete(item)
        
        if self.continuing:
            self.load_save()
        else:
            self.gameplay_start()

    def on_highscore_click(self, event):
        pass

    def on_exit_click(self, event):
        self.tk.quit()

    def gameplay_start(self):
        self.game_state = GameState.PLAYING
        if self.paddle:
            self.canvas.delete(self.paddle.id)
        if self.ball:
            self.canvas.delete(self.ball.id)
        if self.score_text:
            self.canvas.delete(self.score_text)

        self.canvas.bind("<Motion>", self.update_state)
        self.score_text = self.canvas.create_text(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2, text="0", font=("Arial", 24, "bold"), fill="#303055")

        self.paddle = Paddle(self.canvas, CANVAS_WIDTH // 2)
        self.ball = Ball(self.canvas, CANVAS_WIDTH // 2)

        self.load_levels()

    def transition_screen(self):
        displayed = f"Level {self.level_manager.current_level} completed!"
        title = self.canvas.create_text(CANVAS_WIDTH // 2, 150, text=displayed, font=("Arial", 42, "bold"),
                                        fill="WHITE")
        continue_text = self.canvas.create_text(CANVAS_WIDTH // 2, 300, text="Next Level", font=("Arial", 20), fill="WHITE")
        save_exit_text = self.canvas.create_text(CANVAS_WIDTH // 2, 420, text="Save and Exit", font=("Arial", 20), fill="WHITE")

        self.canvas.tag_bind(continue_text, "<Button-1>", self.on_next_click)
        self.canvas.tag_bind(save_exit_text, "<Button-1>", self.on_save_exit_click)

        self.transition_screen_items.append(title)
        self.transition_screen_items.append(continue_text)
        self.transition_screen_items.append(save_exit_text)

    def on_next_click(self, event):
        for item in self.bricks:
            self.canvas.delete(item.id)
        self.bricks.clear()

        for item in self.transition_screen_items:
            self.canvas.delete(item)
        self.transition_screen_items.clear()

        self.next_level()

    def on_save_exit_click(self, event):
        with open("data/save.txt", "w") as f:
            f.write(str(self.level_manager.current_level))

        self.tk.quit()

    def next_level(self):
        self.game_state = GameState.PLAYING
        self.ball.reset()
        self.load_levels()

    def load_save(self):
        with open("data/save.txt", "r") as f:
            self.level_manager.current_level = int(f.read())
        
        os.remove("data/save.txt")

        self.gameplay_start()

    def game_over_screen(self):
        title = self.canvas.create_text(CANVAS_WIDTH // 2, 150, text="Game Over!", font=("Arial", 42, "bold"),
                                        fill="WHITE")
        play_again_text = self.canvas.create_text(CANVAS_WIDTH // 2, 300, text="Play Again", font=("Arial", 20), fill="WHITE")
        exit_text = self.canvas.create_text(CANVAS_WIDTH // 2, 420, text="Exit", font=("Arial", 20), fill="WHITE")

        self.canvas.tag_bind(play_again_text, "<Button-1>", self.on_play_again_click)
        self.canvas.tag_bind(exit_text, "<Button-1>", self.on_exit_click)

        self.game_over_screen_items.append(title)
        self.game_over_screen_items.append(play_again_text)
        self.game_over_screen_items.append(exit_text)
    
    def on_play_again_click(self, event):
        for item in self.bricks:
            self.canvas.delete(item.id)
        self.bricks.clear()
        
        for item in self.game_over_screen_items:
            self.canvas.delete(item)
        self.game_over_screen_items.clear()

        self.lives = PLAYER_LIVES
        self.level_manager.current_level = 0
        self.current_score = 0
        self.gameplay_start()

    def check_collisions(self, rect1, rect2):
        return not (rect1[2] < rect2[0] or rect1[0] > rect2[2] or rect1[3] < rect2[1] or rect1[1] > rect2[3])

    def load_levels(self):
        response = self.level_manager.load_next_level()
        if not response:
            print("No more levels to load.")
            return
        for row_index, row in enumerate(response.brick_layout):
            for col_index, brick_type in enumerate(row):
                if brick_type is not None:
                    position = Point(col_index * (BRICK_WIDTH + BRICK_GAP), row_index * (BRICK_HEIGHT + BRICK_GAP))
                    self.bricks.append(Brick(self.canvas, brick_type, position))

    def handle_explosion(self, brick):
        dq = deque()
        dq.append(brick)
        destroyed = set()
        while dq:
            current = dq.pop()
            for adj in self.bricks:
                if (
                        (abs(current.position.x - adj.position.x) == BRICK_WIDTH + BRICK_GAP and abs(
                            current.position.y - adj.position.y) == 0) or
                        (abs(current.position.x - adj.position.x) == 0 and abs(
                            current.position.y - adj.position.y) == BRICK_HEIGHT + BRICK_GAP) or
                        (abs(current.position.x - adj.position.x) == BRICK_WIDTH + BRICK_GAP and abs(
                            current.position.y - adj.position.y) == BRICK_HEIGHT + BRICK_GAP)):
                    if adj not in destroyed:
                        if adj.type == BrickType.EXPLODING:
                            dq.append(adj)

                        res = adj.update_state()
                        if res == BrickState.DESTROYED:
                            destroyed.add(adj)

        for b in destroyed:
            self.handle_scoring(b.type)
            self.bricks.remove(b)
    
    def handle_scoring(self, type):
        self.current_score += type.value
        
        self.canvas.itemconfig(self.score_text, text=str(self.current_score))