"""Illustration of tournament.

Authors:
    Alejandro Bellogin <alejandro.bellogin@uam.es>

"""
import timeit


mysetup = """
import numpy as np

from game import Player, TwoPlayerGameState, TwoPlayerMatch
from heuristic import simple_evaluation_function, complex_evaluation_function
from tictactoe import TicTacToe
from tournament import StudentHeuristic, Tournament
from datetime import datetime

from reversi import (
    Reversi,
    from_array_to_dictionary_board,
    from_dictionary_to_array_board,
)
heur = __import__('2391_p2_07_alvarez_juez')


def create_match(player1: Player, player2: Player) -> TwoPlayerMatch:

    dim_board = 8

    initial_board = initial_board = (
        ['........',
         '........',
         '........',
         '...BW...',
         '...WB...',
         '........',
         '........',
         '........']
    )
    initial_board = from_array_to_dictionary_board(initial_board)

    initial_player = player1

    game = Reversi(
        player1=player1,
        player2=player2,
        height=dim_board,
        width=dim_board,
    )

    # Initialize a game state.
    game_state = TwoPlayerGameState(
        game=game,
        board=initial_board,
        initial_player=initial_player,
    )

    return TwoPlayerMatch(game_state, max_sec_per_move=1000, gui=False)






tour = Tournament(max_depth=2, init_match=create_match)
strats = {'o1': [heur.PositionalHeuristic], 'o2': [heur.PositionalHeuristic]}

n = 1
"""

mycode = """
scores, totals, names = tour.run(
    student_strategies=strats,
    increasing_depth=False,
    n_pairs=n,
    allow_selfmatch=False,
)
print(
    'Results for tournament where each game is repeated '
    + '%d=%dx2 times, alternating colors for each player' % (2 * n, n),
)

# print(totals)
# print(scores)

print('\ttotal:', end='')
for name1 in names:
    print('\t%s' % (name1), end='')
print()
for name1 in names:
    print('%s\t%d:' % (name1, totals[name1]), end='')
    for name2 in names:
        if name1 == name2:
            print('\t---', end='')
        else:
            print('\t%d' % (scores[name1][name2]), end='')
    print()

"""


print(timeit.timeit(setup=mysetup,
                    stmt=mycode,
                    number=1))
