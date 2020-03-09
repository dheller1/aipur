import random

from aipur.types import Goods, BonusTiles, Player


class GameState:
    def __init__(self, goods_bonus_plates, bonus_tiles, draw_pile, current_player):
        self.goods_bonus_plates = goods_bonus_plates
        self.bonus_tiles = bonus_tiles
        self.draw_pile = draw_pile
        self.current_player = current_player
        self.market = []
        self._refill_market()

    @classmethod
    def new_game(cls):
        cards = ([Goods.Diamonds] * 6 +
                 [Goods.Gold] * 6 +
                 [Goods.Silver] * 6 +
                 [Goods.Cloth] * 8 +
                 [Goods.Spices] * 8 +
                 [Goods.Leather] * 10 +
                 [Goods.Camel] * 11)
        random.shuffle(cards)
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
            draw_pile=cards,
            current_player=random.choice((Player.Alex, Player.Bill))
        )

    def next_player(self):
        return Player.Alex if self.current_player == Player.Bill else Player.Bill

    def is_over(self):
        return (len(self.draw_pile) == 0 or
                filter(lambda p: len(p) == 0, self.goods_bonus_plates.values))

    def _refill_market(self):
        while len(self.market) < 5 and self.draw_pile:
            self.market.append(self.draw_pile.pop(0))
