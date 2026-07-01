import tkinter

from utils.constants import POWER_UP_FALLING_SPEED, POWER_UP_RADIUS
from utils.paths import resource_path

class PowerUp:
    def __init__(self, canvas, x, y, power_up_type):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.type = power_up_type
        self.radius = POWER_UP_RADIUS
        self.speed = POWER_UP_FALLING_SPEED
        self.image = tkinter.PhotoImage(file=resource_path("assets/images/Hammer.png"))
        self.id = canvas.create_image(self.x, self.y, image=self.image)

    def move(self):
        self.y += self.speed
        self.canvas.coords(self.id, self.x, self.y)
    
    def get_rect(self):
        return self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius
    
    def remove_when_picked_up(self):
        self.canvas.delete(self.id)