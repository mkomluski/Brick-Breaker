import time
import tkinter
import os
import random

from collections import namedtuple, deque
from tkinter import Tk

from entities.ball import Ball
from entities.brick import Brick
from entities.paddle import Paddle
from entities.powerup import PowerUp
from levels.level_manager import LevelManager
from utils.collisions import check_collisions
from utils.constants import *
from utils.enums import BrickState, BrickType, GameState, PowerUpType
from utils.screens import draw_game_over_screen, draw_start_screen, draw_transition_screen
from utils.storage import check_highscore, new_highscore

Point = namedtuple("Point", ["x", "y"])


class Game:
    def __init__(self):
        self.ball = None
        self.paddle = None
        self.tk = Tk()
        self.canvas = tkinter.Canvas(self.tk, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background=BG_COLOR)
        self.canvas.pack()
        self.score_text = None
        self.lives_text = None
        self.highscore = check_highscore()
        self.current_score = 0
        self.level_manager = LevelManager()
        self.bricks = []
        self.powerups = []
        self.game_state = GameState.START
        self.start_screen_items = []
        self.transition_screen_items = []
        self.game_over_screen_items = []
        self.continuing = os.path.exists("data/save.txt")
        self.lives = PLAYER_LIVES
        self.wide_paddle_start = None

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
            if check_collisions(self.ball.get_rect(), self.paddle.get_rect()) and self.ball.speed_y > 0:
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
                if check_collisions(self.ball.get_rect(), brick.get_rect()):
                    any_collision = True

                    if not self.ball.in_collision:
                        self.ball.in_collision = True

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
                            self.spawn_power_up(brick)
                            if brick.type == BrickType.EXPLODING:
                                self.handle_explosion(brick)
                            self.ball.in_collision = False
                    break

            if not any_collision:
                self.ball.in_collision = False

            if self.ball.get_rect()[3] > CANVAS_HEIGHT:
                self.ball_out_of_bounds()
            elif not any(brick.type != BrickType.INDESTRUCTIBLE for brick in self.bricks):
                self.game_state = GameState.TRANSITION
                self.transition_screen()

            fell_down = set()
            picked_up = set()

            for power_up in self.powerups:
                power_up.move()

                if power_up.get_rect()[3] > CANVAS_HEIGHT:
                    fell_down.add(power_up)
                elif check_collisions(power_up.get_rect(), self.paddle.get_rect()):
                    picked_up.add(power_up)
            
            for p in fell_down:
                self.powerup_out_of_bounds(p)

            for p in picked_up:
                p.remove_when_picked_up()
                self.activate_powerup(p)
                self.powerups.remove(p)
        
        if self.wide_paddle_start is not None and time.time() - self.wide_paddle_start > WIDE_PADDLE_DURATION:
            self.activate_wide_paddle()

        self.tk.after(20, self.game_loop)

    def ball_out_of_bounds(self):
        self.lives -= 1
        self.canvas.itemconfig(self.lives_text, text=f"{self.lives}♡")
        if self.lives == 0:
            self.game_state = GameState.GAME_OVER
            self.game_over_screen()
        else:
            self.ball.reset()

    def powerup_out_of_bounds(self, powerup):
        powerup.remove_when_picked_up()
        self.powerups.remove(powerup)

    def start_screen(self):
        play_label = "Continue Playing" if self.continuing else "Play"

        self.start_screen_items = draw_start_screen(self.canvas, play_label, self.on_play_click, self.on_highscore_click, self.on_exit_click)

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
        if self.lives_text:
            self.canvas.delete(self.lives_text)
        
        self.wide_paddle_start = None

        self.canvas.bind("<Motion>", self.update_state)
        self.score_text = self.canvas.create_text(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2, text=str(self.current_score), font=("Arial", 24, "bold"), fill="#303055")
        self.lives_text = self.canvas.create_text(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2 - 50, text=f"{str(self.lives)}♡", font=("Arial", 24, "bold"), fill="#303055")

        self.paddle = Paddle(self.canvas, CANVAS_WIDTH // 2)
        self.ball = Ball(self.canvas, CANVAS_WIDTH // 2)

        self.load_levels()

    def transition_screen(self):
        displayed = f"Level {self.level_manager.current_level} completed!"
        
        self.transition_screen_items = draw_transition_screen(self.canvas, displayed, self.on_next_click, self.on_save_exit_click)

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
            f.write(f"{self.level_manager.current_level} {self.current_score}")

        self.tk.quit()

    def next_level(self):
        self.game_state = GameState.PLAYING
        self.ball.reset()
        self.load_levels()

    def load_save(self):
        with open("data/save.txt", "r") as f:
            items = f.read().split()
            self.level_manager.current_level = int(items[0])
            self.current_score = int(items[1])
        
        os.remove("data/save.txt")

        self.gameplay_start()
    
    def game_over_screen(self):
        if self.current_score > self.highscore:
            displayed = f"Game Over!\nNew Highscore: {self.current_score}"
            new_highscore(self.current_score)
        else:
            displayed = "Game Over!"
        
        self.game_over_screen_items = draw_game_over_screen(self.canvas, displayed, self.on_play_again_click, self.on_exit_click)

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
        self.highscore = check_highscore()
        self.gameplay_start()

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
            self.spawn_power_up(b)
    
    def handle_scoring(self, brick_type):
        self.current_score += brick_type.value
        
        if self.current_score > self.highscore:
            self.canvas.itemconfig(self.score_text, text="★"+str(self.current_score))
        else:
            self.canvas.itemconfig(self.score_text, text=str(self.current_score))

    def spawn_power_up(self, brick):
        if random.random() < POWER_UP_DROP_CHANCE:
            powerup_type = random.choice(list(PowerUpType))
            self.powerups.append(PowerUp(self.canvas, brick.position.x + BRICK_WIDTH/2, brick.position.y + BRICK_HEIGHT/2, powerup_type))

    def activate_powerup(self, power):
        match power.type:
            case PowerUpType.EXTRA_LIFE:
                self.activate_extra_life()
            case PowerUpType.WIDE_PADDLE:
                self.activate_wide_paddle()
            case PowerUpType.HAMMER_BALL:
                pass
            case PowerUpType.MULTI_BALL:
                pass
            case PowerUpType.FIREBALL:
                pass

    def activate_extra_life(self):
        self.lives += 1
        self.canvas.itemconfig(self.lives_text, text=f"{self.lives}♡")

    def activate_wide_paddle(self):
        if self.wide_paddle_start is None:
            self.wide_paddle_start = time.time()
            self.paddle.activate_wide()
        else:
            self.wide_paddle_start = None
            self.paddle.activate_wide()

    def activate_hammer_ball(self):
        pass

    def activate_multi_ball(self):
        pass

    def activate_fireball(self):
        pass