from utils.constants import BRICK_HEIGHT, BRICK_WIDTH
from utils.enums import BrickType

class Brick:
    def __init__(self, canvas, type, position):
        self.canvas = canvas
        self.type = type
        self.position = position
        color_map = {
            BrickType.NORMAL: "steelblue",
            BrickType.EXPLODING: "darkorange",
            BrickType.INDESTRUCTIBLE: "grey",
            BrickType.MULTIHIT: "red"
        }
        self.color = color_map[self.type]
        self.hits_taken = 0
        self.crack_lines = []
        self.id = self.canvas.create_rectangle(self.position.x, self.position.y, self.position.x + BRICK_WIDTH, self.position.y + BRICK_HEIGHT, fill=self.color)

    def update_state(self):
        match self.type:
            case BrickType.MULTIHIT:
                if self.hits_taken == 0:
                    self.hits_taken += 1
                    self.crack_lines.append(self.canvas.create_line(self.position.x, self.position.y, self.position.x + BRICK_WIDTH, self.position.y + BRICK_HEIGHT, fill="black", width=2))
                elif self.hits_taken == 1:
                    self.hits_taken += 1
                    self.crack_lines.append(self.canvas.create_line(self.position.x + BRICK_WIDTH, self.position.y, self.position.x, self.position.y + BRICK_HEIGHT, fill="black", width=2))
                elif self.hits_taken == 2:
                    self.remove_when_destroyed()
                else:
                    raise Exception("The BRICK can't take this many hits")
            case BrickType.NORMAL:
                self.remove_when_destroyed()
            case BrickType.INDESTRUCTIBLE:
                # Skips, collision detection is in BALL
                pass
            case BrickType.EXPLODING:
                self.remove_when_destroyed()

    def remove_when_destroyed(self):
        if(BrickType.MULTIHIT == self.type):
            for line in self.crack_lines:
                self.canvas.delete(line)
        self.canvas.delete(self.id)