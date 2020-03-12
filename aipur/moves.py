import enum
import random

from aipur.types import Goods, BonusTiles


class MoveType(enum.Enum):
    DrawSingle = 1
    DrawMultiple = 2
    DrawAllCamels = 3
    Discard = 4


class Move:
    def __init__(self, typ):
        self.typ = typ

    def apply(self, game_state, player_state):
        raise NotImplementedError()


class DrawSingle(Move):
    def __init__(self, draw):
        super().__init__(MoveType.DrawSingle)
        self.draw = draw

    def apply(self, game_state, player_state):
        card = game_state.market.pop(game_state.market.index(self.draw))
        player_state.add_card(card)

    def __str__(self):
        return f'Draw single: {self.draw}'


class DrawAllCamels(Move):
    def __init__(self):
        super().__init__(MoveType.DrawAllCamels)

    def apply(self, game_state, player_state):
        while Goods.Camel in game_state.market:
            game_state.market.remove(Goods.Camel)
            player_state.add_card(Goods.Camel)

    def __str__(self):
        return f'Draw all camels'


class DrawMultiple(Move):
    def __init__(self, draw, replace):
        super().__init__(MoveType.DrawMultiple)
        assert len(draw) == len(replace)
        self.draw = draw  # cards to draw from market to hand
        self.replace = replace  # cards to replace from hand into market

    def apply(self, game_state, player_state):
        for i in range(len(self.draw)):
            i1 = game_state.market.index(self.draw[i])
            if self.replace[i] != Goods.Camel:
                i2 = player_state.hand.index(self.replace[i])
                draw_card = game_state.market[i1]
                game_state.market[i1] = player_state.hand[i2]
                player_state.hand[i2] = draw_card
            else:
                player_state.paddock.pop()
                player_state.add_card(game_state.market.pop(i1))
                game_state.market.append(Goods.Camel)

    def __str__(self):
        draw = ', '.join([str(d) for d in self.draw])
        put = ', '.join([str(r) for r in self.replace])
        return f'Draw multiple: {draw}, put back {put}'


class Discard(Move):
    def __init__(self, good_type, count):
        super().__init__(MoveType.Discard)
        self.good_type = good_type  # type of good to sell
        self.count = count  # number of goods to sell

    def apply(self, game_state, player_state):
        goods_bonus_plates = game_state.goods_bonus_plates[self.good_type]
        received_bonus_plates = []
        bonus_plates_empty = False
        for i in range(self.count):
            player_state.hand.remove(self.good_type)
            if goods_bonus_plates:
                value = goods_bonus_plates.pop(0)
                player_state.gold += value
                received_bonus_plates.append(value)
            else:
                bonus_plates_empty = True

        if len(received_bonus_plates) > 1:
            gold_string = '+'.join([str(p) for p in received_bonus_plates]) + f'={sum(received_bonus_plates)}'
        elif len(received_bonus_plates) == 1:
            gold_string = str(received_bonus_plates[0])

        if received_bonus_plates:
            print(f'Player {player_state.player} received {gold_string} gold for selling.')
        if bonus_plates_empty:
            print(f'No more gold received for selling {self.good_type} (bonus tiles are empty).')

        if self.count == 3 and game_state.bonus_tiles[BonusTiles.Three]:
            tile = random.choice(game_state.bonus_tiles[BonusTiles.Three])
            game_state.bonus_tiles[BonusTiles.Three].remove(tile)
            print(f'Player {player_state.player} receives a bonus tile worth ' +
                  f'{tile} gold for selling three goods.')
            player_state.gold += tile
        elif self.count == 4 and game_state.bonus_tiles[BonusTiles.Four]:
            tile = random.choice(game_state.bonus_tiles[BonusTiles.Four])
            game_state.bonus_tiles[BonusTiles.Four].remove(tile)
            print(f'Player {player_state.player} receives a bonus tile worth ' +
                  f'{tile} gold for selling four goods.')
            player_state.gold += tile
        elif self.count == 5 and game_state.bonus_tiles[BonusTiles.Five]:
            tile = random.choice(game_state.bonus_tiles[BonusTiles.Five])
            game_state.bonus_tiles[BonusTiles.Five].remove(tile)
            print(f'Player {player_state.player} receives a bonus tile worth ' +
                  f'{tile} gold for selling five goods.')
            player_state.gold += tile

    def __str__(self):
        sell = ' '.join(str(g) for g in [self.good_type] * self.count)
        return f'Discard goods: {sell}'


def is_valid_movetype(movetype, game_state, player_state):
    if game_state.is_over():
        return False
    elif movetype == MoveType.DrawSingle:
        return any(filter(lambda g: g != Goods.Camel, game_state.market))
    elif movetype == MoveType.DrawMultiple:
        return len(player_state.hand) > 0 and any(filter(lambda g: g != Goods.Camel, game_state.market))
    elif movetype == MoveType.DrawAllCamels:
        return game_state.market.count(Goods.Camel) > 0
    elif movetype == MoveType.Discard:
        hand = player_state.hand
        return (Goods.Leather in hand or Goods.Spices in hand or Goods.Cloth in hand
                or hand.count(Goods.Silver) >= 2 or hand.count(Goods.Gold) >= 2
                or hand.count(Goods.Diamonds) >= 2)
