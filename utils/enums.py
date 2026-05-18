from enum import Enum

class BrickType(Enum):
    NORMAL = 1
    EXPLODING = 2
    INDESTRUCTIBLE = 3
    MULTIHIT = 4

class BrickState(Enum):
    ALIVE = 1
    DESTROYED = 2