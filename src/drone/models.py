from enum import Enum

class Action(Enum):
    TRANSMIT = 1
    MOVE_INNER = 2
    MOVE_OUTER = 3

class Grid(Enum):
    INNER = 1
    OUTER = 1
    