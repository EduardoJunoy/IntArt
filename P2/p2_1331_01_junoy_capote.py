from game import (
    TwoPlayerGameState,
)
from heuristic import (
    simple_evaluation_function,
)
from tournament import (
    StudentHeuristic,
)
from reversi import (
    Reversi,
    from_array_to_dictionary_board,
    from_dictionary_to_array_board
)


def func_glob(n: int, state: TwoPlayerGameState) -> float:
    return n + simple_evaluation_function(state)


class Solution1(StudentHeuristic):  # Esta es nuestra mejor heurística en los rankings
    def get_name(self) -> str:
        return "heuristica_normie"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        player_pieces = 0
        opponent_pieces = 0

        if state.is_player_max(state.player1):
            player_pieces = state.game._player_coins(
                state.board, state.player1.label)
            return player_pieces

        opponent_pieces = state.game._player_coins(
            state.board, state.player2.label)

        return opponent_pieces



class Solution2(StudentHeuristic):
    def get_name(self) -> str:
        return "heuristica_virgin"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        weight_matrix = [
            [100, -10, 11, 6, 6, 11, -10, 100],
            [-10, -20, 1, 2, 2, 1, -20, -10],
            [10, 1, 5, 4, 4, 5, 1, 10],
            [6, 2, 4, 2, 2, 4, 2, 6],
            [6, 2, 4, 2, 2, 4, 2, 6],
            [10, 1, 5, 4, 4, 5, 1, 10],
            [-10, -20, 1, 2, 2, 1, -20, -10],
            [100, -10, 11, 6, 6, 11, -10, 100]
        ]

        heuristic = 0
        for i in range(0, len(weight_matrix)):
            for j in range(0, len(weight_matrix[0])):
                square = state.board.get((i, j))
                if square == state.player1.label:
                    heuristic += 1 * weight_matrix[i][j]
                elif square == state.player2.label:
                    heuristic -= 1 * weight_matrix[i][j]

        if (state.is_player_max(state.player1)):
            return -heuristic
        else:
            return heuristic


    def opening_evaluation(self, state: TwoPlayerGameState) -> float:
        player_pieces = sum(1 for _, square in state.board.items()
                            if square == state.player1.label)
        opponent_pieces = sum(
            1 for _, square in state.board.items() if square == state.player2.label)
        if state.is_player_max(state.player1):
            return player_pieces - opponent_pieces
        else:
            return opponent_pieces - player_pieces

    def midgame_evaluation(self, state: TwoPlayerGameState) -> float:
        heuristic_value = 0
        for i in range(8):
            for j in range(8):
                square = state.board.get((i, j))
                if square == state.player1.label:
                    heuristic_value += self.weight_matrix[i][j]
                elif square == state.player2.label:
                    heuristic_value -= self.weight_matrix[i][j]
        if state.is_player_max(state.player1):
            return -heuristic_value
        else:
            return heuristic_value

    def endgame_evaluation(self, state: TwoPlayerGameState) -> float:
        # Same as opening for this example
        return self.opening_evaluation(state)


class Solution3(StudentHeuristic):
    def __init__(self):
        self.weight_matrix = [
            [100, -10, 11, 6, 6, 11, -10, 100],
            [-10, -20, 1, 2, 2, 1, -20, -10],
            [10, 1, 5, 4, 4, 5, 1, 10],
            [6, 2, 4, 2, 2, 4, 2, 6],
            [6, 2, 4, 2, 2, 4, 2, 6],
            [10, 1, 5, 4, 4, 5, 1, 10],
            [-10, -20, 1, 2, 2, 1, -20, -10],
            [100, -10, 11, 6, 6, 11, -10, 100]
        ]

    def get_name(self):
        return "heuristica_chad"

    def evaluation_function(self, state):
        # Determine the game phase and call the corresponding evaluation function
        # This is a placeholder, you'll need to implement these methods
        game_phase = self.get_game_phase(state)
        if game_phase == 'opening':
            value = self.opening_evaluation(state)
        else:
            value = self.midgame_endgame_evaluation(state)

        if state.is_player_max(state.player1):
            return value
        else:
            return -value

    def get_game_phase(self, state):
        global corners, adjacent_to_corners

        total_pieces = sum(
            1 for _, square in state.board.items() if square is not None)

        corners = [(1, 1), (1, 8), (8, 1), (8, 8)]
        adjacent_to_corners = [(1, 2), (2, 1), (2, 2), (1, 7), (2, 8),
                               (2, 7), (7, 1), (8, 2), (7, 2), (7, 7), (8, 7), (7, 8)]

        if total_pieces <= 16:
            return 'opening'
        else:
            return 'midgame-endgame'

    def opening_evaluation(self, state):
        def get_pos_value(state, player_to_move, next_player):
            player_pieces = [coord for coord, player in state.board.items(
            ) if player == player_to_move]
            threatened_pieces = 0
            for piece in player_pieces:
                for direction in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                    next_square = (piece[0] + direction[0],
                                   piece[1] + direction[1])
                    if state.board.get(next_square) == player_to_move:
                        next_next_square = (
                            next_square[0] + direction[0], next_square[1] + direction[1])
                        if state.board.get(next_next_square) is None:
                            threatened_pieces += 1
                            break

            if len(player_pieces) == threatened_pieces:
                return -9999999

            return -len(player_pieces) - threatened_pieces

        if state.end_of_game:
            return 9999999999

        return get_pos_value(state, state.player1.label, state.player2.label) - get_pos_value(state, state.player2.label, state.player1.label)

    def midgame_endgame_evaluation(self, state):
        def get_pos_value(state, player_to_move, next_player):
            score = 0

            directions = [(0, 1), (1, 0), (0, -1), (-1, 0),
                          (1, 1), (-1, -1), (1, -1), (-1, 1)]

            for corner in corners:
                if state.board.get(corner) == player_to_move:
                    score += 1000

            for adjacent in adjacent_to_corners:
                corresponding_corner = (
                    adjacent[0] if adjacent[0] == 1 else 8, adjacent[1] if adjacent[1] == 1 else 8)
                if state.board.get(corresponding_corner) != player_to_move and state.board.get(adjacent) == player_to_move:
                    score -= 500

            player_pieces = [coord for coord, player in state.board.items(
            ) if player == player_to_move]
            score += len(player_pieces)

            threatened_pieces = 0
            for piece in player_pieces:
                for direction in directions:
                    next_square = (piece[0] + direction[0],
                                   piece[1] + direction[1])
                    if state.board.get(next_square) == next_player:
                        threatened_pieces += 1
                        break
            score -= 2 * threatened_pieces

            return score

        if state.end_of_game:
            return 9999999999

        return get_pos_value(state, state.player1.label, state.player2.label) - get_pos_value(state, state.player2.label, state.player1.label)
