import random

from aipur.types import Goods, BonusTiles, Player
from aipur.moves import is_valid_movetype, MoveType


class PlayerState:
    def __init__(self, player, cards):
        self.player = player
        self.hand = []
        self.paddock = []
        self.add_cards(cards)
        self.gold = 0

    def add_card(self, card):
        if card == Goods.Camel:
            self.paddock.append(card)
        else:
            self.hand.append(card)

    def add_cards(self, cards):
        for c in cards:
            self.add_card(c)


class GameState:
    def __init__(self, goods_bonus_plates, bonus_tiles, draw_pile, players, silent=False):
        self.goods_bonus_plates = goods_bonus_plates
        self.bonus_tiles = bonus_tiles
        self.draw_pile = draw_pile
        self.market = [Goods.Camel] * 3
        self.player_states = {p: PlayerState(p, self.draw(5)) for p in players}
        self.current_player = Player.Alex  # random.choice(players)
        self.market.extend(self.draw(2))
        self.silent = silent

    @classmethod
    def new_game(cls):
        cards = ([Goods.Diamonds] * 6 +
                 [Goods.Gold] * 6 +
                 [Goods.Silver] * 6 +
                 [Goods.Cloth] * 8 +
                 [Goods.Spices] * 8 +
                 [Goods.Leather] * 10 +
                 [Goods.Camel] * 8)  # 3 additional camels are always in the market
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
            players=(Player.Alex, Player.Bill),
        )

    def apply_move(self, move):
        player = self.current_player
        player_state = self.player_states[player]
        move.apply(self, player_state)
        if len(self.market) < 5:
            self._refill_market()
        self.current_player = self.next_player()

    def draw(self, count):
        """ Draws `count` cards from the draw pile (or until empty) and returns them. """
        return [self.draw_pile.pop(0) for i in range(count) if self.draw_pile]

    def next_player(self):
        return Player.Alex if self.current_player == Player.Bill else Player.Bill

    def is_over(self):
        empty_bonus_plates = filter(lambda p: len(p) == 0, self.goods_bonus_plates.values())
        return len(self.draw_pile) == 0 or len(list(empty_bonus_plates)) >= 3

    def _refill_market(self):
        self.market.extend(self.draw(5 - len(self.market)))
