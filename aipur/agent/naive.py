import random

from aipur.agent.base import Agent
from aipur.moves import Move, MoveType, is_valid_movetype, DrawSingle, DrawAllCamels, SellGoods, DrawMultiple
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
            discard = [random.choice(player_state.hand)] if len(player_state.hand) == 7 else None
            return DrawSingle(card_choice, discard=discard)
        elif chosen_move_type == MoveType.DrawAllCamels:
            return DrawAllCamels()
        elif chosen_move_type == MoveType.SellGoods:
            sellable = RandomBot._determine_sellables(player_state.hand)
            sell_good = random.choice(list(sellable.keys()))
            sell_min = 2 if sell_good not in [Goods.Leather, Goods.Spices, Goods.Cloth] else 1
            sell_count = random.randint(sell_min, sellable[sell_good])
            return SellGoods(sell_good, sell_count)
        elif chosen_move_type == MoveType.DrawMultiple:
            return RandomBot.make_draw_multiple_action(game_state, player_state)

    @staticmethod
    def make_draw_multiple_action(game_state, player_state):
        max_draw = len(_without_camels(game_state.market))
        max_replace = len(player_state.hand) + len(player_state.paddock)
        max_total = min(max_draw, max_replace)
        how_many = random.randint(2, max_total) if max_total > 2 else 2

        to_draw = random.sample(_without_camels(game_state.market), k=how_many)
        to_replace = random.sample(player_state.hand + player_state.paddock, k=how_many)

        # goods which are exchanged for other goods are no problem, but if we put camels
        # into the market we effectively increase the hand size
        added_goods = to_replace.count(Goods.Camel)
        if len(player_state.hand) + added_goods > 7:
            n_discard = len(player_state.hand) + added_goods - 7
            player_hand_after_move = player_state.hand[:]
            for replaced in _without_camels(to_replace):
                player_hand_after_move.remove(replaced)
            player_hand_after_move.extend(_without_camels(to_draw))
            assert len(player_hand_after_move) == len(player_state.hand) + added_goods
            to_discard = random.sample(player_hand_after_move, k=n_discard)
        else:
            to_discard = None

        return DrawMultiple(draw=to_draw, replace=to_replace, discard=to_discard)

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
