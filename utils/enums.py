from enum import Enum


class BrickType(Enum):
    NORMAL = 1
    EXPLODING = 2
    MULTIHIT = 3
    INDESTRUCTIBLE = 4


class BrickState(Enum):
    ALIVE = 1
    DESTROYED = 2


class GameState(Enum):
    PLAYING = 1
    TRANSITION = 2
    GAME_OVER = 3
    START = 4
