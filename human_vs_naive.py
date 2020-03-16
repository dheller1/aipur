import argparse
import colorama
import pickle
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
    parser = argparse.ArgumentParser()
    parser.add_argument('--silent', action='store_true', default=False)
    parser.add_argument('--stats', type=int, help='Simulate N games and save statistics.')
    args = parser.parse_args()

    colorama.init()

    nruns = 1 if not args.stats else args.stats
    results = []
    for i in range(nruns):
        alex = RandomBot()
        bill = RandomBot()

        game = GameState.new_game()
        game.silent = args.silent

        while not game.is_over():
            if not args.silent:
                print(f'Market: ', end='')
                print(' '.join([str(c) for c in game.market]))

                print(f"It is {game.current_player}'s turn.", end=' ')
                print(f'There are {len(game.draw_pile)} cards in the draw pile.')
                print_hand(game.player_states[game.current_player])

            if game.current_player == Player.Alex:
                move = alex.select_move(game, game.player_states[game.current_player])
            else:
                move = bill.select_move(game, game.player_states[game.current_player])

            if not args.silent:
                print('Move - ' + str(move))
            game.apply_move(move)
            assert len(game.player_states[game.current_player].hand) <= 7
            if not args.silent:
                print()

        alex_gold = game.player_states[Player.Alex].gold
        bill_gold = game.player_states[Player.Bill].gold

        results.append(alex_gold)
        results.append(bill_gold)

        if not args.silent:
            print('Game end.')
            print('Score:')
            print(f'{Player.Alex}: {alex_gold} gold')
            print(f'{Player.Bill}: {bill_gold} gold')

            if alex_gold > bill_gold:
                print(f'{Player.Alex} wins!')
            elif bill_gold > alex_gold:
                print(f'{Player.Bill} wins!')
            else:
                print(f"It's a draw!")

    if args.stats:
        with open('results.txt', 'w') as f:
            f.writelines([f'{r}\n' for r in results])
            # pickle.dump(results, f)
        print(f'Wrote {nruns} results to results.txt.')


if __name__ == '__main__':
    main()
