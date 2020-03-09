import enum


class Player(enum.Enum):
    Alex = 1
    Bill = 2


class Goods(enum.Enum):
    Leather = 1
    Spices = 2
    Cloth = 3
    Silver = 4
    Gold = 5
    Diamonds = 6
    Camel = 7


class BonusTiles(enum.Enum):
    Three = 3
    Four = 4
    Five = 5
