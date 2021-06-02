import time
from game import (
    TwoPlayerGameState,
)
from tournament import (
    StudentHeuristic,
)
from reversi import (
    Reversi,
    from_array_to_dictionary_board,
    from_dictionary_to_array_board,
)


class PositionalHeuristic(StudentHeuristic):

    def get_name(self) -> str:
        return "posi_ju"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        weights = [[100, -20, 10, 5, 5, 10, -20, 100],
                   [-20, -50, -2, -2, -2, -2, -50, -20],
                   [10, -2, -1, -1, -1, -1, -2, 10],
                   [5, -2, -1, -1, -1, -1, -2, 5],
                   [5, -2, -1, -1, -1, -1, -2, 5],
                   [10, -2, -1, -1, -1, -1, -2, 10],
                   [-20, -50, -2, -2, -2, -2, -50, -20],
                   [100, -20, 10, 5, 5, 10, -20, 100]]

        heur = 0
        for i in range(0, len(weights)):
            for j in range(0, len(weights[0])):
                square = state.board.get((i, j))
                if square == state.player1.label:
                    heur += 1 * weights[i][j]
                elif square == state.player2.label:
                    heur -= 1 * weights[i][j]

        if(state.is_player_max(state.player1)):
            return -heur
        else:
            return heur


class PPCr(StudentHeuristic):

    def get_name(self) -> str:
        return "PPCr_ju"

    def positional(self, state: TwoPlayerGameState) -> float:
        weights = [[100, -20, 10, 5, 5, 10, -20, 100],
                   [-20, -50, -2, -2, -2, -2, -50, -20],
                   [10, -2, -1, -1, -1, -1, -2, 10],
                   [5, -2, -1, -1, -1, -1, -2, 5],
                   [5, -2, -1, -1, -1, -1, -2, 5],
                   [10, -2, -1, -1, -1, -1, -2, 10],
                   [-20, -50, -2, -2, -2, -2, -50, -20],
                   [100, -20, 10, 5, 5, 10, -20, 100]]

        heur = 0
        for i in range(0, len(weights)):
            for j in range(0, len(weights[0])):
                square = state.board.get((i, j))
                if square == state.player1.label:
                    heur += 1 * weights[i][j]
                elif square == state.player2.label:
                    heur -= 1 * weights[i][j]

        if(state.is_player_max(state.player1)):
            return -heur
        else:
            return heur

    def mobility(self, state: TwoPlayerGameState) -> float:
        heuristic = state.game._choice_diff(state.board)

        if(state.is_player_max(state.player1)):
            return heuristic
        else:
            return -heuristic

    def corner(self, state: TwoPlayerGameState) -> float:
        heuristic = state.game._corner_diff(state.board)
        if(state.is_player_max(state.player1)):
            return heuristic
        else:
            return -heuristic

    def coin(self, state: TwoPlayerGameState) -> float:
        heuristic = state.game._coin_diff(state.board)

        if(state.is_player_max(state.player1)):
            return -heuristic
        else:
            return heuristic

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        movements = (-4 + len(state.board))
        max_mov = 8 * 8
        if movements <= 24:
            return self.corner(state)
        elif max_mov - movements <= 14:
            return self.coin(state)
        else:
            return self.positional(state)


class Evaluation(StudentHeuristic):

    def get_name(self) -> str:
        return "eval_ju"

    def mobility(self, state: TwoPlayerGameState) -> float:
        heuristic = state.game._choice_diff(state.board)

        if(state.is_player_max(state.player1)):
            return heuristic
        else:
            return -heuristic

    def corner(self, state: TwoPlayerGameState) -> float:
        heuristic = state.game._corner_diff(state.board)
        if(state.is_player_max(state.player1)):
            return heuristic
        else:
            return -heuristic

    def coin(self, state: TwoPlayerGameState) -> float:
        heuristic = state.game._coin_diff(state.board)

        if(state.is_player_max(state.player1)):
            return -heuristic
        else:
            return heuristic

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return 0.20 * self.mobility(state) + 0.10 * \
            self.coin(state) + 0.7 * self.corner(state)
