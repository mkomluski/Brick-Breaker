from utils.constants import *

class Paddle:
    def __init__(self, canvas, x):
        self.canvas = canvas
        self.x = x
        self.y = PADDLE_Y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.color = PADDLE_COLOR
        self.id = self.canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill=self.color)

    def move(self, x):
        self.x = max(0, min(CANVAS_WIDTH - self.width, x))
        self.canvas.coords(self.id, self.x, self.y, self.x + self.width, self.y + self.height)

    def get_rect(self):
        return (self.x, self.y, self.x + self.width, self.y + self.height)