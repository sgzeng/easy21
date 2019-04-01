from enum import Enum, unique

@unique
class Action(Enum):
    stick = "stick"
    hit = "hit"

@unique
class Role(Enum):
    dealer = "dealer"
    player = "player"
