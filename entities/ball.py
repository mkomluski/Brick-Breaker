from utils.constants import *

class Ball:
    def __init__(self, canvas, x):
        self.canvas = canvas
        self.x = x
        self.y = CANVAS_HEIGHT // 2
        self.radius = BALL_RADIUS
        self.speed_x = BALL_SPEED
        self.speed_y = -BALL_SPEED
        self.color = BALL_COLOR
        self.id = self.canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius, fill=self.color)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.canvas.coords(self.id, self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius)
        if self.x - self.radius <= 0 or self.x + self.radius >= CANVAS_WIDTH:
            self.speed_x *= -1

    def get_rect(self):
        return (self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius)
    
    def set_speed(self, speed_x, speed_y):
        self.speed_x = speed_x
        self.speed_y = speed_y
    
    def reset(self):
        self.x = CANVAS_WIDTH // 2
        self.y = CANVAS_HEIGHT // 2
        self.canvas.coords(self.id, self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius)
    
        self.set_speed(BALL_SPEED, -BALL_SPEED)

        return self
    
    def stop(self):
        self.speed_x = 0
        self.speed_y = 0

        return self