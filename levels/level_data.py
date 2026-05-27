from utils.enums import BrickType
from utils.constants import MIN_BRICKS_ON_SCREEN, MAX_INDESTRUCTIBLE_PER_ROW
import random

class LevelData:
    def __init__(self, level_number: int, brick_layout: list[list[BrickType]]):
        self.level_number = level_number
        self.brick_layout = brick_layout

    @classmethod
    def generate(cls, level_number):
        if level_number == 1:
            allowed_brick_types = [BrickType.NORMAL]
        elif level_number == 2:
            allowed_brick_types = [BrickType.NORMAL, BrickType.MULTIHIT]
        elif level_number == 3:
            allowed_brick_types = [BrickType.NORMAL, BrickType.MULTIHIT, BrickType.EXPLODING]
        elif level_number >= 4:
            allowed_brick_types = [BrickType.NORMAL, BrickType.MULTIHIT, BrickType.EXPLODING, BrickType.INDESTRUCTIBLE]
        else:
            raise ValueError("Invalid level number")
        
        grid = [[None for _ in range(10)] for _ in range(6)]

        positions_list = []
        for index_row, row in enumerate(grid):
            for index_col, _ in enumerate(row):
                positions_list.append((index_row, index_col))
        
        bricks_on_screen = random.randint(MIN_BRICKS_ON_SCREEN, 60)

        from utils.enums import BrickType
from utils.constants import MIN_BRICKS_ON_SCREEN, MAX_INDESTRUCTIBLE_PER_ROW
import random

class LevelData:
    def __init__(self, level_number: int, brick_layout: list[list[BrickType]]):
        self.level_number = level_number
        self.brick_layout = brick_layout

    @classmethod
    def generate(cls, level_number):
        if level_number == 1:
            allowed_brick_types = [BrickType.NORMAL]
        elif level_number == 2:
            allowed_brick_types = [BrickType.NORMAL, BrickType.MULTIHIT]
        elif level_number == 3:
            allowed_brick_types = [BrickType.NORMAL, BrickType.MULTIHIT, BrickType.EXPLODING]
        elif level_number >= 4:
            allowed_brick_types = [BrickType.NORMAL, BrickType.MULTIHIT, BrickType.EXPLODING, BrickType.INDESTRUCTIBLE]
        else:
            raise ValueError("Invalid level number")
        
        grid = [[None for _ in range(10)] for _ in range(6)]

        positions_list = []
        for index_row, row in enumerate(grid):
            for index_col, _ in enumerate(row):
                positions_list.append((index_row, index_col))
        
        bricks_on_screen = random.randint(MIN_BRICKS_ON_SCREEN, 60)

        sampled = random.sample(positions_list, bricks_on_screen)


        indestructible_counts = [0] * 6
        for row, col in sampled:
            grid[row][col] = random.choice(allowed_brick_types)

            if indestructible_counts[row] >= MAX_INDESTRUCTIBLE_PER_ROW:
                grid[row][col] = BrickType.NORMAL

            if grid[row][col] == BrickType.INDESTRUCTIBLE:
                indestructible_counts[row] += 1

        return cls(level_number, grid)