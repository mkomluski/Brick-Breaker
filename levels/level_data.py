from utils.enums import BrickType

brick_layout = [
    [BrickType.MULTIHIT, BrickType.EXPLODING, None, BrickType.INDESTRUCTIBLE, None, None, None, None, BrickType.INDESTRUCTIBLE, None],
    [None, None, BrickType.MULTIHIT, BrickType.EXPLODING, None, BrickType.MULTIHIT, BrickType.EXPLODING, BrickType.MULTIHIT, None, None],
    [None, BrickType.MULTIHIT, None, None, BrickType.MULTIHIT, None, None, BrickType.EXPLODING, None, BrickType.MULTIHIT],
    [BrickType.MULTIHIT, None, BrickType.INDESTRUCTIBLE, None, BrickType.INDESTRUCTIBLE, None, BrickType.MULTIHIT, None, BrickType.EXPLODING, None],
    [BrickType.EXPLODING, None, BrickType.MULTIHIT, None, BrickType.EXPLODING, None, BrickType.INDESTRUCTIBLE, None, BrickType.MULTIHIT, None],
    [BrickType.NORMAL, BrickType.NORMAL, BrickType.NORMAL, BrickType.NORMAL, BrickType.NORMAL, BrickType.NORMAL, BrickType.NORMAL, BrickType.NORMAL, BrickType.NORMAL, BrickType.NORMAL]]

class LevelData:
    def __init__(self, level_number: int, brick_layout: list[list[BrickType]]):
        self.level_number = level_number
        self.brick_layout = brick_layout

level = LevelData(1, brick_layout)