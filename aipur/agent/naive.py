import random

from aipur.agent.base import Agent
from aipur.moves import Move, MoveType, is_valid_movetype, DrawSingle, DrawAllCamels, Discard, DrawMultiple
from aipur.types import Goods


def _without_camels(li):
    return [c for c in li if c != Goods.Camel]


class RandomBot(Agent):
    def select_move(self, game_state, player_state):
        available_moves = list(
            filter(lambda m: is_valid_movetype(m, game_state, player_state),
            [m for m in MoveType]))

        chosen_move_type = random.choice(available_moves)
        if chosen_move_type == MoveType.DrawSingle:
            card_choice = random.choice(_without_camels(game_state.market))
            return DrawSingle(card_choice)
        elif chosen_move_type == MoveType.DrawAllCamels:
            return DrawAllCamels()
        elif chosen_move_type == MoveType.Discard:
            sellable = RandomBot._determine_sellables(player_state.hand)
            sell_good = random.choice(list(sellable.keys()))
            sell_min = 2 if sell_good not in [Goods.Leather, Goods.Spices, Goods.Cloth] else 1
            sell_count = random.randint(sell_min, sellable[sell_good])
            return Discard(sell_good, sell_count)
        elif chosen_move_type == MoveType.DrawMultiple:
            max_draw = len(_without_camels(game_state.market))
            max_replace = len(player_state.hand) + len(player_state.paddock)
            max_total = min(max_draw, max_replace)
            how_many = random.randint(1, max_total) if max_total > 1 else 1
            to_draw = random.sample(_without_camels(game_state.market), k=how_many)
            to_replace = random.sample(player_state.hand + player_state.paddock, k=how_many)
            return DrawMultiple(to_draw, to_replace)

    @staticmethod
    def _determine_sellables(player_hand):
        sellable = {}
        for good in Goods:
            if good == Goods.Camel:
                continue
            count = player_hand.count(good)
            if count >= 2:
                sellable[good] = count  # need two silver/gold/diamonds to sell
            elif count >= 1 and good in [Goods.Leather, Goods.Spices, Goods.Cloth]:
                sellable[good] = count
        return sellable
