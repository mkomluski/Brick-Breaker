from levels.level_data import LevelData

class LevelManager:
    def __init__(self):
        self.current_level = 0

    def load_next_level(self):
        self.current_level += 1
        return LevelData.generate(self.current_level)