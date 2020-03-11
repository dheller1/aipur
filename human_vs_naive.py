import colorama
import time

from aipur.agent.naive import RandomBot
from aipur.game import GameState
from aipur.types import Player


def print_hand(player_state):
    print(f"{player_state.player}'s hand: ", end='')
    print(' '.join([str(c) for c in player_state.hand]), end='')
    paddock = player_state.paddock
    if len(paddock) > 1:
        print(f' and {len(paddock)} camels.')
    elif len(paddock) == 1:
        print(' and one camel.')
    if len(paddock) == 0:
        print(' and no camels.')


def main():
    colorama.init()

    alex = RandomBot()
    bill = RandomBot()

    game = GameState.new_game()
    while not game.is_over():
        print(f'Market: ', end='')
        print(' '.join([str(c) for c in game.market]))

        print(f"It is {game.current_player}'s turn.", end=' ')
        print(f'There are {len(game.draw_pile)} cards in the draw pile.')
        print_hand(game.player_states[game.current_player])

        if game.current_player == Player.Alex:
            move = alex.select_move(game, game.player_states[game.current_player])
        else:
            move = bill.select_move(game, game.player_states[game.current_player])

        print('Move - ' + str(move))
        game.apply_move(move)
        print()
        # time.sleep(0.3)


if __name__ == '__main__':
    main()
