from enum import Enum, unique

@unique
class Action(Enum):
    stick = 0
    hit = 1

@unique
class Role(Enum):
    dealer = "dealer"
    player = "player"
