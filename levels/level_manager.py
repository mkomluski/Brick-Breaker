class LevelManager:
    def __init__(self, levels):
        self.current_level = 0
        self.levels = levels

    def load_next_level(self):
        try:
            self.current_level += 1
            return self.levels[self.current_level-1]
        except IndexError:
            print("No more levels to load.")
            return None