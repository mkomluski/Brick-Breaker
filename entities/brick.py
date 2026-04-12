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
                    #Here draw the diagonal line
                elif self.hits_taken == 1:
                    self.hits_taken += 1
                    #draw the second line
                elif self.hits_taken == 2:
                    self.remove_when_destroyed()
                else:
                    raise Exception("The BRICK can't take this many hits")
            case BrickType.NORMAL:
                self.remove_when_destroyed()
            case BrickType.INDESTRUCTIBLE:
                #Should do nothing except collision detection which isnt here but in ball
                pass
            case BrickType.EXPLODING:
                self.remove_when_destroyed()

    def remove_when_destroyed(self):
        self.canvas.delete(self.id)