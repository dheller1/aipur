import random

from aipur.types import Goods, BonusTiles


class GameState:
    def __init__(self, goods_bonus_plates, bonus_tiles, cards):
        self.goods_bonus_plates = goods_bonus_plates
        self.bonus_tiles = bonus_tiles
        self.cards = cards
        random.shuffle(self.cards)

    @classmethod
    def new_game(cls):
        return GameState(
            goods_bonus_plates={
                Goods.Leather: [4, 3, 2] + [1] * 6,
                Goods.Cloth: [5, 3, 3, 2, 2, 1, 1],
                Goods.Spices: [5, 3, 3, 2, 2, 1, 1],
                Goods.Silver: [5] * 5,
                Goods.Gold: [6, 6, 5, 5, 5],
                Goods.Diamonds: [7, 7, 5, 5, 5],
            },
            bonus_tiles={
                BonusTiles.Three: [1, 1, 2, 2, 2, 3, 3],
                BonusTiles.Four: [4, 4, 5, 5, 5, 6, 6],
                BonusTiles.Five: [8, 8, 9, 10, 10],
            },
            cards=([Goods.Diamonds] * 6 +
                   [Goods.Gold] * 6 +
                   [Goods.Silver] * 6 +
                   [Goods.Cloth] * 8 +
                   [Goods.Spices] * 8 +
                   [Goods.Leather] * 10 +
                   [Goods.Camel] * 11)
        )
