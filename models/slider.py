import enum

class Slider(enum.Enum):
    BLACK = 1
    OLD_RED = 2
    NEW_RED = 3
    YELLOW = 4

    def __str__(self):
        return self.name




