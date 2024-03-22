from game import (
    TwoPlayerGameState,
)
from tournament import (
    StudentHeuristic,
)

import numpy as np
from typing import Sequence
from reversi import from_dictionary_to_array_board
from heuristic import Heuristic


# Clase primer torneo
class ReyMambo(StudentHeuristic):
    def get_name(self) -> str:
        return "Rey Mambo"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return rey_mambo(state)

# Clase segundo torneo


class QuitateElTop(StudentHeuristic):
    def get_name(self) -> str:
        return "Quitate El Top"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return quitate_el_top(state)

# Clase tercer torneo 1


class RayoBarcelona(StudentHeuristic):
    def get_name(self) -> str:
        return "Rayo de Barcelona"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return rayo_barcelona(state)

# Clase tercer torneo 2


class QuitateElTopV2(StudentHeuristic):
    def get_name(self) -> str:
        return "Quitate el top V2"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return quitate_el_topV2(state)

# Clase tercer torneo 2.2


class QuitateElTopV2_2(StudentHeuristic):
    def get_name(self) -> str:
        return "Quitate el top V2_2"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return quitate_el_topV2_2(state)

# Clase cuarto torneo


class QuitateElTopV3(StudentHeuristic):
    def get_name(self) -> str:
        return "Quitate el top V3"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return quitate_el_topV3(state)

# Clase antonio


class antonio(StudentHeuristic):
    def get_name(self) -> str:
        return "Antonio"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return optimal_heuristic(state)

# ----------------------------------------------------------------------------------------
# ---------------------------------------- FUNCIONES--------------------------------------
# ----------------------------------------------------------------------------------------


# Distincion de casillas
corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
corners_diagonal = [(1, 1), (1, 6), (6, 1), (6, 6)]
odd_distance_1 = [(0, 1), (1, 0), (0, 6), (6, 0),
                  (1, 7), (7, 1), (6, 7), (7, 6)]
even_distance_2 = [(0, 2), (2, 0), (0, 5), (5, 0),
                   (2, 7), (7, 2), (5, 7), (7, 5)]
base_lateral = [(0, 3), (3, 0), (0, 4), (4, 0), (3, 7), (7, 3), (4, 7), (7, 4)]
firstLevel_inner = [(2, 3), (2, 4), (3, 2), (3, 5),
                    (4, 2), (4, 5), (5, 3), (5, 4)]
secondLevel_inner = [(3, 3), (3, 4), (4, 3), (4, 4),
                     (2, 2), (2, 5), (5, 2), (5, 5)]
thirdLevel_inner = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (3, 1), (4, 1),
                    (5, 1), (6, 2), (6, 3), (6, 4), (6, 5), (2, 6), (3, 6), (4, 6), (5, 6)]

# Utiles
height = 8
width = 8

earlyGame2midGame = 18
midGame2endGame = 49

# Evolucion de rayo de barcelona con distincion de 3 momentos en la partida (early-game, mid-game y end-game) y variables estaticas distintas en cada una,
# en combinacion con quitate el topV2


def quitate_el_topV3(state: TwoPlayerGameState) -> float:

    coins_player1 = state.game._player_coins(state.board, state.player1.label)
    coins_player2 = state.game._player_coins(state.board, state.player2.label)
    coins = coins_player1 + coins_player2

    # Estados abolutos independientemente del momento
    # Ultimos 2 movimientos, intento ganar el mayor numero de monedas
    if coins >= 63:
        if state.is_player_max(state.player1):
            return coins_player1 - coins_player2
        else:
            return coins_player2 - coins_player1

    # -----------------------------------------------------------------------#
    # Hago la distinción de en que momento de la partida me encuentro
    # Si hay menos de 18 fichas en el tablero, estamos en early-game
    if coins <= earlyGame2midGame:
        heu = quitate_el_topV3_earlyGame(state)
    # Si hay entre 18 y 49 fichas en el tablero, estamos en mid-game
    elif coins <= midGame2endGame:
        heu = quitate_el_topV3_midGame(state)
    # Si hay mas de 49 fichas en el tablero, estamos en end-game
    else:
        heu = quitate_el_topV3_endGame(state)

        # Depending on the match
    if state.is_player_max(state.player1):
        return heu
    else:
        return - heu

# -------------------------------------------------------------------------------------------------------
# ----------------------------------FUNCION DE EARLY QUITATE EL TOP V3-----------------------------------
# -------------------------------------------------------------------------------------------------------
# Funcion de evaluacion para early-game de quitate el topV3


def quitate_el_topV3_earlyGame(state: TwoPlayerGameState) -> float:
    # Set up constants
    score_for_corner = 100
    score_for_corner_diagonal = -100
    score_odd_distance_1 = -30
    score_even_distance_2 = 6
    score_base_lateral = 5
    score_for_firstLevel_inner = 8
    score_for_secondLevel_inner = 12
    score_for_thirLevel_inner = -8
    score_for_player_mobility = 20
    if (state.is_player_max(state.player1)):
        score_for_coin_diff = 1.5
    else:
        score_for_coin_diff = 1

    score_for_flipped_spaces = 120

    heu = 0

    tablero = from_dictionary_to_array_board(state.board, height, width)

# Count corners for player 1 and 2
    for corner in corners:
        if tablero[corner[0]][corner[1]] == state.player1.label:
            heu += score_for_corner
        elif tablero[corner[0]][corner[1]] == state.player2.label:
            heu -= score_for_corner

    # Count corners diagonal for player 1 and 2
    for tile in corners_diagonal:
        if tablero[tile[0]][tile[1]] == state.player1.label:
            heu += score_for_corner_diagonal
        elif tablero[tile[0]][tile[1]] == state.player2.label:
            heu -= score_for_corner_diagonal

    # Count odd distance 1 for player 1 and 2
    for odd in odd_distance_1:
        if tablero[odd[0]][odd[1]] == state.player1.label:
            heu += score_odd_distance_1
        elif tablero[odd[0]][odd[1]] == state.player2.label:
            heu -= score_odd_distance_1

    # Count even distance 2 for player 1 and 2
    for even in even_distance_2:
        if tablero[even[0]][even[1]] == state.player1.label:
            heu += score_even_distance_2
        elif tablero[even[0]][even[1]] == state.player2.label:
            heu -= score_even_distance_2

    # Count base lateral for player 1 and 2
    for base in base_lateral:
        if tablero[base[0]][base[1]] == state.player1.label:
            heu += score_base_lateral
        elif tablero[base[0]][base[1]] == state.player2.label:
            heu -= score_base_lateral

    # Count first level inner for player 1 and 2
    for first in firstLevel_inner:
        if tablero[first[0]][first[1]] == state.player1.label:
            heu += score_for_firstLevel_inner
        elif tablero[first[0]][first[1]] == state.player2.label:
            heu -= score_for_firstLevel_inner

    # Count second level inner for player 1 and 2
    for second in secondLevel_inner:
        if tablero[second[0]][second[1]] == state.player1.label:
            heu += score_for_secondLevel_inner + score_for_firstLevel_inner
        elif tablero[second[0]][second[1]] == state.player2.label:
            heu -= score_for_secondLevel_inner + score_for_firstLevel_inner

    # Count third level inner for player 1 and 2
    for third in thirdLevel_inner:
        if tablero[third[0]][third[1]] == state.player1.label:
            heu += score_for_thirLevel_inner
        elif tablero[third[0]][third[1]] == state.player2.label:
            heu -= score_for_thirLevel_inner

   # Si ningun jugador tiene una esquina no hace falta calcular
    if tablero[0][0] == state.player1.label or tablero[0][7] == state.player1.label or tablero[7][0] == state.player1.label or tablero[7][7] == state.player1.label:
        heu += _calculo_flipped_spaces(state, state.player1.label,
                                       tablero) * score_for_flipped_spaces
    elif tablero[0][0] == state.player2.label or tablero[0][7] == state.player2.label or tablero[7][0] == state.player2.label or tablero[7][7] == state.player2.label:
        heu -= _calculo_flipped_spaces(state, state.player2.label,
                                       tablero) * score_for_flipped_spaces

    # Player movement diff
    moves_player1 = state.game._get_valid_moves(
        state.board, state.player1.label)
    moves_player2 = state.game._get_valid_moves(
        state.board, state.player2.label)

    moves_diff = len(moves_player1) - len(moves_player2)

    heu += moves_diff * score_for_player_mobility

    # Coins diff
    coins_player1 = state.game._player_coins(state.board, state.player1.label)
    coins_player2 = state.game._player_coins(state.board, state.player2.label)

    coins_diff = coins_player1 - coins_player2

    heu += coins_diff * score_for_coin_diff

    return heu

# -------------------------------------------------------------------------------------------------------
# -----------------------------------FUNCION DE MID QUITATE EL TOP V3------------------------------------
# -------------------------------------------------------------------------------------------------------
# Funcion de evaluacion para mid-game de quitate el topV3


def quitate_el_topV3_midGame(state: TwoPlayerGameState) -> float:
    # Set up constants
    score_for_corner = 75
    score_for_corner_diagonal = -50
    score_odd_distance_1 = -30
    score_even_distance_2 = 6
    score_base_lateral = 5
    score_for_firstLevel_inner = 2
    score_for_secondLevel_inner = 6
    score_for_thirdLevel_inner = -8
    score_for_player_mobility = 3
    score_for_coin_diff = 3
    score_for_flipped_spaces = 100

    heu = 0

    tablero = from_dictionary_to_array_board(state.board, height, width)

# Count corners for player 1 and 2
    for corner in corners:
        if tablero[corner[0]][corner[1]] == state.player1.label:
            heu += score_for_corner
        elif tablero[corner[0]][corner[1]] == state.player2.label:
            heu -= score_for_corner

    # Count corners diagonal for player 1 and 2
    for tile in corners_diagonal:
        if tablero[tile[0]][tile[1]] == state.player1.label:
            heu += score_for_corner_diagonal
        elif tablero[tile[0]][tile[1]] == state.player2.label:
            heu -= score_for_corner_diagonal

    # Si tengo la esquina y la diagonal, compenso
    if tablero[0][0] == state.player1.label and tablero[1][1] == state.player1.label:
        heu -= score_for_corner_diagonal
    elif tablero[0][0] == state.player2.label and tablero[1][1] == state.player2.label:
        heu += score_for_corner_diagonal
    if tablero[0][7] == state.player1.label and tablero[1][6] == state.player1.label:
        heu -= score_for_corner_diagonal
    elif tablero[0][7] == state.player2.label and tablero[1][6] == state.player2.label:
        heu += score_for_corner_diagonal
    if tablero[7][0] == state.player1.label and tablero[6][1] == state.player1.label:
        heu -= score_for_corner_diagonal
    elif tablero[7][0] == state.player2.label and tablero[6][1] == state.player2.label:
        heu += score_for_corner_diagonal
    if tablero[7][7] == state.player1.label and tablero[6][6] == state.player1.label:
        heu -= score_for_corner_diagonal
    elif tablero[7][7] == state.player2.label and tablero[6][6] == state.player2.label:
        heu += score_for_corner_diagonal

    # Count odd distance 1 for player 1 and 2
    for odd in odd_distance_1:
        if tablero[odd[0]][odd[1]] == state.player1.label:
            heu += score_odd_distance_1
        elif tablero[odd[0]][odd[1]] == state.player2.label:
            heu -= score_odd_distance_1

    # Si tengo la esquina y la distancia 1, compenso
    if tablero[0][0] == state.player1.label and tablero[0][1] == state.player1.label:
        heu -= score_odd_distance_1
    elif tablero[0][0] == state.player2.label and tablero[0][1] == state.player2.label:
        heu += score_odd_distance_1
    if tablero[0][0] == state.player1.label and tablero[1][0] == state.player1.label:
        heu -= score_odd_distance_1
    elif tablero[0][0] == state.player2.label and tablero[1][0] == state.player2.label:
        heu += score_odd_distance_1
    if tablero[0][7] == state.player1.label and tablero[0][6] == state.player1.label:
        heu -= score_odd_distance_1
    elif tablero[0][7] == state.player2.label and tablero[0][6] == state.player2.label:
        heu += score_odd_distance_1
    if tablero[0][7] == state.player1.label and tablero[1][7] == state.player1.label:
        heu -= score_odd_distance_1
    elif tablero[0][7] == state.player2.label and tablero[1][7] == state.player2.label:
        heu += score_odd_distance_1
    if tablero[7][0] == state.player1.label and tablero[7][1] == state.player1.label:
        heu -= score_odd_distance_1
    elif tablero[7][0] == state.player2.label and tablero[7][1] == state.player2.label:
        heu += score_odd_distance_1
    if tablero[7][0] == state.player1.label and tablero[6][0] == state.player1.label:
        heu -= score_odd_distance_1
    elif tablero[7][0] == state.player2.label and tablero[6][0] == state.player2.label:
        heu += score_odd_distance_1
    if tablero[7][7] == state.player1.label and tablero[7][6] == state.player1.label:
        heu -= score_odd_distance_1
    elif tablero[7][7] == state.player2.label and tablero[7][6] == state.player2.label:
        heu += score_odd_distance_1
    if tablero[7][7] == state.player1.label and tablero[6][7] == state.player1.label:
        heu -= score_odd_distance_1
    elif tablero[7][7] == state.player2.label and tablero[6][7] == state.player2.label:
        heu += score_odd_distance_1

    # Count even distance 2 for player 1 and 2
    for even in even_distance_2:
        if tablero[even[0]][even[1]] == state.player1.label:
            heu += score_even_distance_2
        elif tablero[even[0]][even[1]] == state.player2.label:
            heu -= score_even_distance_2

    # Count base lateral for player 1 and 2
    for base in base_lateral:
        if tablero[base[0]][base[1]] == state.player1.label:
            heu += score_base_lateral
        elif tablero[base[0]][base[1]] == state.player2.label:
            heu -= score_base_lateral

    # Count first level inner for player 1 and 2
    for first in firstLevel_inner:
        if tablero[first[0]][first[1]] == state.player1.label:
            heu += score_for_firstLevel_inner
        elif tablero[first[0]][first[1]] == state.player2.label:
            heu -= score_for_firstLevel_inner

    # Count second level inner for player 1 and 2
    for second in secondLevel_inner:
        if tablero[second[0]][second[1]] == state.player1.label:
            heu += score_for_secondLevel_inner + score_for_firstLevel_inner
        elif tablero[second[0]][second[1]] == state.player2.label:
            heu -= score_for_secondLevel_inner + score_for_firstLevel_inner

    # Count third level inner for player 1 and 2
    for third in thirdLevel_inner:
        if tablero[third[0]][third[1]] == state.player1.label:
            heu += score_for_thirdLevel_inner
        elif tablero[third[0]][third[1]] == state.player2.label:
            heu -= score_for_thirdLevel_inner

   # Si ningun jugador tiene una esquina no hace falta calcular
    if tablero[0][0] == state.player1.label or tablero[0][7] == state.player1.label or tablero[7][0] == state.player1.label or tablero[7][7] == state.player1.label:
        heu += _calculo_flipped_spaces(state, state.player1.label,
                                       tablero) * score_for_flipped_spaces
    elif tablero[0][0] == state.player2.label or tablero[0][7] == state.player2.label or tablero[7][0] == state.player2.label or tablero[7][7] == state.player2.label:
        heu -= _calculo_flipped_spaces(state, state.player2.label,
                                       tablero) * score_for_flipped_spaces

    # Player movement diff
    moves_player1 = state.game._get_valid_moves(
        state.board, state.player1.label)
    moves_player2 = state.game._get_valid_moves(
        state.board, state.player2.label)

    moves_diff = len(moves_player1) - len(moves_player2)

    heu += moves_diff * score_for_player_mobility

    # Coins diff
    coins_player1 = state.game._player_coins(state.board, state.player1.label)
    coins_player2 = state.game._player_coins(state.board, state.player2.label)

    coins_diff = coins_player1 - coins_player2

    heu += coins_diff * score_for_coin_diff

    return heu

# -------------------------------------------------------------------------------------------------------
# -----------------------------------FUNCION DE END QUITATE EL TOP V3------------------------------------
# -------------------------------------------------------------------------------------------------------
# Funcion de evaluacion para end-game de quitate el topV3


def quitate_el_topV3_endGame(state: TwoPlayerGameState) -> float:
    # Set up constants
    score_for_corner = 50
    score_for_corner_diagonal = -50
    score_odd_distance_1 = -30
    score_even_distance_2 = 6
    score_base_lateral = 5
    score_for_firstLevel_inner = 2
    score_for_secondLevel_inner = 6
    score_for_thirdLevel_inner = -8
    score_for_player_mobility = 4
    score_for_coin_diff = 12
    score_for_flipped_spaces = 50

    heu = 0

    tablero = from_dictionary_to_array_board(state.board, height, width)

# Count corners for player 1 and 2
    for corner in corners:
        if tablero[corner[0]][corner[1]] == state.player1.label:
            heu += score_for_corner
        elif tablero[corner[0]][corner[1]] == state.player2.label:
            heu -= score_for_corner

    # Count corners diagonal for player 1 and 2
    for tile in corners_diagonal:
        if tablero[tile[0]][tile[1]] == state.player1.label:
            heu += score_for_corner_diagonal
        elif tablero[tile[0]][tile[1]] == state.player2.label:
            heu -= score_for_corner_diagonal

    # Si tengo la esquina y la diagonal, compenso
    if tablero[0][0] == state.player1.label and tablero[1][1] == state.player1.label:
        heu -= score_for_corner_diagonal
    elif tablero[0][0] == state.player2.label and tablero[1][1] == state.player2.label:
        heu += score_for_corner_diagonal
    if tablero[0][7] == state.player1.label and tablero[1][6] == state.player1.label:
        heu -= score_for_corner_diagonal
    elif tablero[0][7] == state.player2.label and tablero[1][6] == state.player2.label:
        heu += score_for_corner_diagonal
    if tablero[7][0] == state.player1.label and tablero[6][1] == state.player1.label:
        heu -= score_for_corner_diagonal
    elif tablero[7][0] == state.player2.label and tablero[6][1] == state.player2.label:
        heu += score_for_corner_diagonal
    if tablero[7][7] == state.player1.label and tablero[6][6] == state.player1.label:
        heu -= score_for_corner_diagonal
    elif tablero[7][7] == state.player2.label and tablero[6][6] == state.player2.label:
        heu += score_for_corner_diagonal

    # Count odd distance 1 for player 1 and 2
    for odd in odd_distance_1:
        if tablero[odd[0]][odd[1]] == state.player1.label:
            heu += score_odd_distance_1
        elif tablero[odd[0]][odd[1]] == state.player2.label:
            heu -= score_odd_distance_1

    # Si tengo la esquina y la distancia 1, compenso
    if tablero[0][0] == state.player1.label and tablero[0][1] == state.player1.label:
        heu -= score_odd_distance_1
    elif tablero[0][0] == state.player2.label and tablero[0][1] == state.player2.label:
        heu += score_odd_distance_1
    if tablero[0][0] == state.player1.label and tablero[1][0] == state.player1.label:
        heu -= score_odd_distance_1
    elif tablero[0][0] == state.player2.label and tablero[1][0] == state.player2.label:
        heu += score_odd_distance_1
    if tablero[0][7] == state.player1.label and tablero[0][6] == state.player1.label:
        heu -= score_odd_distance_1
    elif tablero[0][7] == state.player2.label and tablero[0][6] == state.player2.label:
        heu += score_odd_distance_1
    if tablero[0][7] == state.player1.label and tablero[1][7] == state.player1.label:
        heu -= score_odd_distance_1
    elif tablero[0][7] == state.player2.label and tablero[1][7] == state.player2.label:
        heu += score_odd_distance_1
    if tablero[7][0] == state.player1.label and tablero[7][1] == state.player1.label:
        heu -= score_odd_distance_1
    elif tablero[7][0] == state.player2.label and tablero[7][1] == state.player2.label:
        heu += score_odd_distance_1
    if tablero[7][0] == state.player1.label and tablero[6][0] == state.player1.label:
        heu -= score_odd_distance_1
    elif tablero[7][0] == state.player2.label and tablero[6][0] == state.player2.label:
        heu += score_odd_distance_1
    if tablero[7][7] == state.player1.label and tablero[7][6] == state.player1.label:
        heu -= score_odd_distance_1
    elif tablero[7][7] == state.player2.label and tablero[7][6] == state.player2.label:
        heu += score_odd_distance_1
    if tablero[7][7] == state.player1.label and tablero[6][7] == state.player1.label:
        heu -= score_odd_distance_1
    elif tablero[7][7] == state.player2.label and tablero[6][7] == state.player2.label:
        heu += score_odd_distance_1

    # Count even distance 2 for player 1 and 2
    for even in even_distance_2:
        if tablero[even[0]][even[1]] == state.player1.label:
            heu += score_even_distance_2
        elif tablero[even[0]][even[1]] == state.player2.label:
            heu -= score_even_distance_2

    # Count base lateral for player 1 and 2
    for base in base_lateral:
        if tablero[base[0]][base[1]] == state.player1.label:
            heu += score_base_lateral
        elif tablero[base[0]][base[1]] == state.player2.label:
            heu -= score_base_lateral

    # Count first level inner for player 1 and 2
    for first in firstLevel_inner:
        if tablero[first[0]][first[1]] == state.player1.label:
            heu += score_for_firstLevel_inner
        elif tablero[first[0]][first[1]] == state.player2.label:
            heu -= score_for_firstLevel_inner

    # Count second level inner for player 1 and 2
    for second in secondLevel_inner:
        if tablero[second[0]][second[1]] == state.player1.label:
            heu += score_for_secondLevel_inner + score_for_firstLevel_inner
        elif tablero[second[0]][second[1]] == state.player2.label:
            heu -= score_for_secondLevel_inner + score_for_firstLevel_inner

    # Count third level inner for player 1 and 2
    for third in thirdLevel_inner:
        if tablero[third[0]][third[1]] == state.player1.label:
            heu += score_for_thirdLevel_inner
        elif tablero[third[0]][third[1]] == state.player2.label:
            heu -= score_for_thirdLevel_inner

   # Si ningun jugador tiene una esquina no hace falta calcular
    if tablero[0][0] == state.player1.label or tablero[0][7] == state.player1.label or tablero[7][0] == state.player1.label or tablero[7][7] == state.player1.label:
        heu += _calculo_flipped_spaces(state, state.player1.label,
                                       tablero) * score_for_flipped_spaces
    elif tablero[0][0] == state.player2.label or tablero[0][7] == state.player2.label or tablero[7][0] == state.player2.label or tablero[7][7] == state.player2.label:
        heu -= _calculo_flipped_spaces(state, state.player2.label,
                                       tablero) * score_for_flipped_spaces

    # Player movement diff
    moves_player1 = state.game._get_valid_moves(
        state.board, state.player1.label)
    moves_player2 = state.game._get_valid_moves(
        state.board, state.player2.label)

    moves_diff = len(moves_player1) - len(moves_player2)

    heu += moves_diff * score_for_player_mobility

    # Coins diff
    coins_player1 = state.game._player_coins(state.board, state.player1.label)
    coins_player2 = state.game._player_coins(state.board, state.player2.label)

    coins_diff = coins_player1 - coins_player2

    heu += coins_diff * score_for_coin_diff

    return heu

# ------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------FIN QUITATE EL TOP V3-----------------------------------------------
# ------------------------------------------------------------------------------------------------------------------


def quitate_el_topV2_2(state: TwoPlayerGameState) -> float:
    """
    Evolution of mambo.
    Still prioriazing corners and sides, but also takes into account parity and mobility.
    """
    # Set up constants
    height = 8
    width = 8
    score_for_corner = 100
    score_for_corner_diagonal = -70
    score_odd_distance_1 = -50
    score_even_distance_2 = 6
    score_base_lateral = 2
    score_for_firstLevel_inner = 10
    score_for_secondLevel_inner = 4
    score_for_player_mobility = 15
    score_for_flipped_spaces = 180

    heu = 0

    tablero = from_dictionary_to_array_board(state.board, height, width)

    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    corners_diagonal = [(1, 1), (1, 6), (6, 1), (6, 6)]
    odd_distance_1 = [(0, 1), (1, 0), (0, 6), (6, 0),
                      (1, 7), (7, 1), (6, 7), (7, 6)]
    even_distance_2 = [(0, 2), (2, 0), (0, 5), (5, 0),
                       (2, 7), (7, 2), (5, 7), (7, 5)]
    base_lateral = [(0, 3), (3, 0), (0, 4), (4, 0),
                    (3, 7), (7, 3), (4, 7), (7, 4)]
    firstLevel_inner = [(2, 2), (2, 3), (2, 4), (2, 5), (3, 2),
                        (3, 5), (4, 2), (4, 5), (5, 2), (5, 3), (5, 4), (5, 5)]
    secondLevel_inner = [(3, 3), (3, 4), (4, 3), (4, 4)]

    # Count corners for player 1 and 2
    for corner in corners:
        if tablero[corner[0]][corner[1]] == state.player1.label:
            heu += score_for_corner
        elif tablero[corner[0]][corner[1]] == state.player2.label:
            heu -= score_for_corner

    # Si ningun jugador tiene una esquina no hace falta calcular
    if heu != 0:
        heu += _calculo_flipped_spaces(state, state.player1.label,
                                       tablero) * score_for_flipped_spaces
        heu -= _calculo_flipped_spaces(state, state.player2.label,
                                       tablero) * score_for_flipped_spaces

    # Count corners diagonal for player 1 and 2
    for tile in corners_diagonal:
        if tablero[tile[0]][tile[1]] == state.player1.label:
            heu += score_for_corner_diagonal
        elif tablero[tile[0]][tile[1]] == state.player2.label:
            heu -= score_for_corner_diagonal

    # Count odd distance 1 for player 1 and 2
    for odd in odd_distance_1:
        if tablero[odd[0]][odd[1]] == state.player1.label:
            heu += score_odd_distance_1
        elif tablero[odd[0]][odd[1]] == state.player2.label:
            heu -= score_odd_distance_1

    # Count even distance 2 for player 1 and 2
    for even in even_distance_2:
        if tablero[even[0]][even[1]] == state.player1.label:
            heu += score_even_distance_2
        elif tablero[even[0]][even[1]] == state.player2.label:
            heu -= score_even_distance_2

    # Count base lateral for player 1 and 2
    for base in base_lateral:
        if tablero[base[0]][base[1]] == state.player1.label:
            heu += score_base_lateral
        elif tablero[base[0]][base[1]] == state.player2.label:
            heu -= score_base_lateral

    # Count first level inner for player 1 and 2
    for first in firstLevel_inner:
        if tablero[first[0]][first[1]] == state.player1.label:
            heu += score_for_firstLevel_inner
        elif tablero[first[0]][first[1]] == state.player2.label:
            heu -= score_for_firstLevel_inner

    # Count second level inner for player 1 and 2
    for second in secondLevel_inner:
        if tablero[second[0]][second[1]] == state.player1.label:
            heu += score_for_secondLevel_inner + score_for_firstLevel_inner
        elif tablero[second[0]][second[1]] == state.player2.label:
            heu -= score_for_secondLevel_inner + score_for_firstLevel_inner

    # Player movement diff
    player1_mobility = len(state.game._get_valid_moves(
        state.board, state.player1.label))
    heu += player1_mobility * score_for_player_mobility
    player2_mobility = len(state.game._get_valid_moves(
        state.board, state.player2.label))
    heu -= player2_mobility * score_for_player_mobility

    # Obtener numero de fichas del tablero
    coins_player1 = 0
    coins_player2 = 0
    for i in range(0, 8):
        for j in range(0, 8):
            if tablero[i][j] == state.player1.label:
                coins_player1 += 1
            if tablero[i][j] == state.player2.label:
                coins_player2 += 1
    coins = coins_player1 + coins_player2
    if coins < 20:
        heu += coins_player1*-20
        heu -= coins_player2*-20
    if coins > 54:
        heu += coins_player1*0.5
        heu -= coins_player2*0.5
    # heu -= player_mobility * coins/64 * score_for_player_mobility

    # Teorico final con victoria
    if (coins_player2 == 0 or coins == 64):
        if coins_player1 > coins_player2:
            heu += 1000000
        else:
            heu -= 1000000

    if coins >= 63:
        heu = coins_player1 - coins_player2

    # Depending on the match
    if state.is_player_max(state.player1):
        return heu
    else:
        return - heu


def quitate_el_topV2(state: TwoPlayerGameState) -> float:
    """
    Evolution of mambo.
    Still prioriazing corners and sides, but also takes into account parity and mobility.
    """
    # Set up constants
    score_for_corner = 100
    score_for_corner_diagonal = -50
    score_odd_distance_1 = -30
    score_even_distance_2 = 6
    score_base_lateral = 2
    score_for_firstLevel_inner = 2
    score_for_secondLevel_inner = 4
    score_for_player_mobility = 6
    score_for_flipped_spaces = 120

    heu = 0

    tablero = from_dictionary_to_array_board(state.board, height, width)

    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    corners_diagonal = [(1, 1), (1, 6), (6, 1), (6, 6)]
    odd_distance_1 = [(0, 1), (1, 0), (0, 6), (6, 0),
                      (1, 7), (7, 1), (6, 7), (7, 6)]
    even_distance_2 = [(0, 2), (2, 0), (0, 5), (5, 0),
                       (2, 7), (7, 2), (5, 7), (7, 5)]
    base_lateral = [(0, 3), (3, 0), (0, 4), (4, 0),
                    (3, 7), (7, 3), (4, 7), (7, 4)]
    firstLevel_inner = [(2, 2), (2, 3), (2, 4), (2, 5), (3, 2),
                        (3, 5), (4, 2), (4, 5), (5, 2), (5, 3), (5, 4), (5, 5)]
    secondLevel_inner = [(3, 3), (3, 4), (4, 3), (4, 4)]

    # Count corners for player 1 and 2
    for corner in corners:
        if tablero[corner[0]][corner[1]] == state.player1.label:
            heu += score_for_corner
        elif tablero[corner[0]][corner[1]] == state.player2.label:
            heu -= score_for_corner

    # Si ningun jugador tiene una esquina no hace falta calcular
    if heu != 0:
        heu += _calculo_flipped_spaces(state, state.player1.label,
                                       tablero) * score_for_flipped_spaces
        heu -= _calculo_flipped_spaces(state, state.player2.label,
                                       tablero) * score_for_flipped_spaces

    # Count corners diagonal for player 1 and 2
    for tile in corners_diagonal:
        if tablero[tile[0]][tile[1]] == state.player1.label:
            heu += score_for_corner_diagonal
        elif tablero[tile[0]][tile[1]] == state.player2.label:
            heu -= score_for_corner_diagonal

    # Count odd distance 1 for player 1 and 2
    for odd in odd_distance_1:
        if tablero[odd[0]][odd[1]] == state.player1.label:
            heu += score_odd_distance_1
        elif tablero[odd[0]][odd[1]] == state.player2.label:
            heu -= score_odd_distance_1

    # Count even distance 2 for player 1 and 2
    for even in even_distance_2:
        if tablero[even[0]][even[1]] == state.player1.label:
            heu += score_even_distance_2
        elif tablero[even[0]][even[1]] == state.player2.label:
            heu -= score_even_distance_2

    # Count base lateral for player 1 and 2
    for base in base_lateral:
        if tablero[base[0]][base[1]] == state.player1.label:
            heu += score_base_lateral
        elif tablero[base[0]][base[1]] == state.player2.label:
            heu -= score_base_lateral

    # Count first level inner for player 1 and 2
    for first in firstLevel_inner:
        if tablero[first[0]][first[1]] == state.player1.label:
            heu += score_for_firstLevel_inner
        elif tablero[first[0]][first[1]] == state.player2.label:
            heu -= score_for_firstLevel_inner

    # Count second level inner for player 1 and 2
    for second in secondLevel_inner:
        if tablero[second[0]][second[1]] == state.player1.label:
            heu += score_for_secondLevel_inner + score_for_firstLevel_inner
        elif tablero[second[0]][second[1]] == state.player2.label:
            heu -= score_for_secondLevel_inner + score_for_firstLevel_inner

    # Player movement diff
    player_mobility = len(state.game._get_valid_moves(
        state.board, state.next_player.label))

    # Obtener numero de fichas del tablero
    coins_player1 = 0
    coins_player2 = 0
    for i in range(0, 8):
        for j in range(0, 8):
            if tablero[i][j] == state.player1.label:
                coins_player1 += 1
            if tablero[i][j] == state.player2.label:
                coins_player2 += 1
    coins = coins_player1 + coins_player2
    heu -= player_mobility * coins/64 * score_for_player_mobility

    # Teorico final con victoria #VER COMO IMPLEMENTAR BIEN ??
    if player_mobility == 0 and (coins_player2 == 0 or coins == 64):
        if coins_player1 > coins_player2:
            heu += 1000000
        else:
            heu -= 1000000

    if coins >= 63:
        heu = coins_player1 - coins_player2

    # Depending on the match
    if state.is_player_max(state.player1):
        return heu
    else:
        return - heu


def simple_evaluation_function(state: TwoPlayerGameState) -> float:
    """Return a random value, except for terminal game states."""
    state_value = 2*np.random.rand() - 1

    if state.end_of_game:
        scores = state.scores
        # Evaluation of the state from the point of view of MAX

        assert isinstance(scores, (Sequence, np.ndarray))
        score_difference = scores[0] - scores[1]


def quitate_el_top(state: TwoPlayerGameState) -> float:
    """
    Evolution of mambo.
    Still prioriazing corners and sides, but also takes into account parity and mobility.
    """
    # Set up constants
    height = 8
    width = 8
    score_for_corner = 50
    score_for_side_odd = -2
    score_for_side_even = 7
    score_for_inter = 1
    score_for_exter = 3
    score_for_player_mobility = -3
    heu = 0

    tablero = from_dictionary_to_array_board(state.board, height, width)

    # Count corners for player 1
    if tablero[0][0] == state.player1.label:
        heu += score_for_corner
    if tablero[0][height - 1] == state.player1.label:
        heu += score_for_corner
    if tablero[width - 1][0] == state.player1.label:
        heu += score_for_corner
    if tablero[width - 1][height - 1] == state.player1.label:
        heu += score_for_corner

    # Count corners for player 2
    if tablero[0][0] == state.player2.label:
        heu -= score_for_corner
    if tablero[0][height - 1] == state.player2.label:
        heu -= score_for_corner
    if tablero[width - 1][0] == state.player2.label:
        heu -= score_for_corner
    if tablero[width - 1][height - 1] == state.player2.label:
        heu -= score_for_corner

    # Count sides take into account parity
    if tablero[0][0] == '.':
        # Sides that will try to get the control of the corner
        if tablero[0][1] == state.player1.label:
            heu += score_for_side_odd
        if tablero[0][2] == state.player1.label:
            heu += score_for_side_even
        if tablero[0][7] != '.':
            if tablero[0][3] == state.player1.label:
                heu += score_for_side_odd
            if tablero[0][4] == state.player1.label:
                heu += score_for_side_even

        if tablero[1][0] == state.player1.label:
            heu += score_for_side_odd
        if tablero[2][0] == state.player1.label:
            heu += score_for_side_even
        if tablero[7][0] != '.':
            if tablero[3][0] == state.player1.label:
                heu += score_for_side_odd
            if tablero[4][0] == state.player1.label:
                heu += score_for_side_even

    if tablero[0][7] == '.':
        # Sides that will try to get the control of the corner
        if tablero[0][6] == state.player1.label:
            heu += score_for_side_odd
        if tablero[0][5] == state.player1.label:
            heu += score_for_side_even
        if tablero[0][0] != '.':
            if tablero[0][4] == state.player1.label:
                heu += score_for_side_odd
            if tablero[0][3] == state.player1.label:
                heu += score_for_side_even

        if tablero[1][7] == state.player1.label:
            heu += score_for_side_odd
        if tablero[2][7] == state.player1.label:
            heu += score_for_side_even
        if tablero[7][7] != '.':
            if tablero[3][7] == state.player1.label:
                heu += score_for_side_odd
            if tablero[4][7] == state.player1.label:
                heu += score_for_side_even

    if tablero[7][0] == '.':
        # Sides that will try to get the control of the corner
        if tablero[7][1] == state.player1.label:
            heu += score_for_side_odd
        if tablero[7][2] == state.player1.label:
            heu += score_for_side_even
        if tablero[7][7] != '.':
            if tablero[7][3] == state.player1.label:
                heu += score_for_side_odd
            if tablero[7][4] == state.player1.label:
                heu += score_for_side_even

        if tablero[6][0] == state.player1.label:
            heu += score_for_side_odd
        if tablero[5][0] == state.player1.label:
            heu += score_for_side_even
        if tablero[0][0] != '.':
            if tablero[4][0] == state.player1.label:
                heu += score_for_side_odd
            if tablero[3][0] == state.player1.label:
                heu += score_for_side_even

    if tablero[7][7] == '.':
        # Sides that will try to get the control of the corner
        if tablero[7][6] == state.player1.label:
            heu += score_for_side_odd
        if tablero[7][5] == state.player1.label:
            heu += score_for_side_even
        if tablero[7][0] != '.':
            if tablero[7][4] == state.player1.label:
                heu += score_for_side_odd
            if tablero[7][3] == state.player1.label:
                heu += score_for_side_even

        if tablero[6][7] == state.player1.label:
            heu += score_for_side_odd
        if tablero[5][7] == state.player1.label:
            heu += score_for_side_even
        if tablero[0][7] != '.':
            if tablero[4][7] == state.player1.label:
                heu += score_for_side_odd
            if tablero[3][7] == state.player1.label:
                heu += score_for_side_even

    # Intern square
    for i in range(2, 6):
        for j in range(2, 6):
            if tablero[i][j] == state.player1.label:
                heu += score_for_inter
            if tablero[i][j] == state.player2.label:
                heu -= score_for_inter

    # Extern square
    for i in range(1, 7):
        if tablero[1][i] == state.player1.label:
            heu -= score_for_exter
        if tablero[6][i] == state.player1.label:
            heu -= score_for_exter

        if tablero[1][i] == state.player2.label:
            heu += score_for_exter
        if tablero[6][i] == state.player2.label:
            heu += score_for_exter

        if tablero[i][1] == state.player1.label:
            heu -= score_for_exter
        if tablero[i][6] == state.player1.label:
            heu -= score_for_exter

        if tablero[i][1] == state.player2.label:
            heu += score_for_exter
        if tablero[i][6] == state.player2.label:
            heu += score_for_exter

    # Player movement diff
    player_mobility = len(state.game._get_valid_moves(
        state.board, state.next_player.label))

    # Obtener numero de fichas del tablero
    coins_player1 = 0
    coins_player2 = 0
    for i in range(0, 8):
        for j in range(0, 8):
            if tablero[i][j] == state.player1.label:
                coins_player1 += 1
            if tablero[i][j] == state.player2.label:
                coins_player2 += 1
    coins = coins_player1 + coins_player2
    heu -= player_mobility * coins/64 * score_for_player_mobility

    # Teorico final con victoria
    if player_mobility == 0:
        if coins_player1 > coins_player2:
            heu += 1000000

    # Depending on the match
    if state.is_player_max(state.player1):
        return heu
    else:
        return - heu


def rey_mambo(state: TwoPlayerGameState) -> float:
    """
    First Heuristic create. Priority: Corners and sides as main.
    We contabilize the corners and sides of the board as a priority
    """
    # Set up constants
    height = 8
    width = 8
    score_for_corner = 40
    score_for_side = 10
    score_for_inter = 1
    score_for_exter = 3
    heu = 0

    tablero = from_dictionary_to_array_board(state.board, height, width)

    # Count corners for player 1
    if tablero[0][0] == state.player1.label:
        heu += score_for_corner
    if tablero[0][height - 1] == state.player1.label:
        heu += score_for_corner
    if tablero[width - 1][0] == state.player1.label:
        heu += score_for_corner
    if tablero[width - 1][height - 1] == state.player1.label:
        heu += score_for_corner

    # Count corners for player 2
    if tablero[0][0] == state.player2.label:
        heu -= score_for_corner
    if tablero[0][height - 1] == state.player2.label:
        heu -= score_for_corner
    if tablero[width - 1][0] == state.player2.label:
        heu -= score_for_corner
    if tablero[width - 1][height - 1] == state.player2.label:
        heu -= score_for_corner

    # Count sides
    for i in range(1, height-1):
        if tablero[0][i] == state.player1.label:
            heu += score_for_side
        if tablero[width - 1][i] == state.player1.label:
            heu += score_for_side

        if tablero[0][i] == state.player2.label:
            heu -= score_for_side
        if tablero[width - 1][i] == state.player2.label:
            heu -= score_for_side

        if tablero[i][0] == state.player1.label:
            heu += score_for_side
        if tablero[i][height - 1] == state.player1.label:
            heu += score_for_side

        if tablero[i][0] == state.player2.label:
            heu -= score_for_side
        if tablero[i][height - 1] == state.player2.label:
            heu -= score_for_side

    # Intern square
    for i in range(2, 6):
        for j in range(2, 6):
            if tablero[i][j] == state.player1.label:
                heu += score_for_inter
            if tablero[i][j] == state.player2.label:
                heu -= score_for_inter

    # Extern square
    for i in range(1, 7):
        if tablero[1][i] == state.player1.label:
            heu -= score_for_exter
        if tablero[6][i] == state.player1.label:
            heu -= score_for_exter

        if tablero[1][i] == state.player2.label:
            heu += score_for_exter
        if tablero[6][i] == state.player2.label:
            heu += score_for_exter

        if tablero[i][1] == state.player1.label:
            heu -= score_for_exter
        if tablero[i][6] == state.player1.label:
            heu -= score_for_exter

        if tablero[i][1] == state.player2.label:
            heu += score_for_exter
        if tablero[i][6] == state.player2.label:
            heu += score_for_exter

    # Depending on the match
    if state.is_player_max(state.player1):
        return +heu
    else:
        return -heu


def quitate_el_top(state: TwoPlayerGameState) -> float:
    """
    Evolution of mambo.
    Still prioriazing corners and sides, but also takes into account parity and mobility.
    """
    # Set up constants
    height = 8
    width = 8
    score_for_corner = 50
    score_for_side_odd = -2
    score_for_side_even = 7
    score_for_inter = 1
    score_for_exter = 3
    score_for_player_mobility = 3

    heu = 0

    tablero = from_dictionary_to_array_board(state.board, height, width)

    # Count corners for player 1
    if tablero[0][0] == state.player1.label:
        heu += score_for_corner
    if tablero[0][height - 1] == state.player1.label:
        heu += score_for_corner
    if tablero[width - 1][0] == state.player1.label:
        heu += score_for_corner
    if tablero[width - 1][height - 1] == state.player1.label:
        heu += score_for_corner

    # Count corners for player 2
    if tablero[0][0] == state.player2.label:
        heu -= score_for_corner
    if tablero[0][height - 1] == state.player2.label:
        heu -= score_for_corner
    if tablero[width - 1][0] == state.player2.label:
        heu -= score_for_corner
    if tablero[width - 1][height - 1] == state.player2.label:
        heu -= score_for_corner

    # Count sides take into account parity
    if tablero[0][0] == '.':
        # Sides that will try to get the control of the corner
        if tablero[0][1] == state.player1.label:
            heu += score_for_side_odd
        if tablero[0][2] == state.player1.label:
            heu += score_for_side_even
        if tablero[0][7] != '.':
            if tablero[0][3] == state.player1.label:
                heu += score_for_side_odd
            if tablero[0][4] == state.player1.label:
                heu += score_for_side_even

        if tablero[1][0] == state.player1.label:
            heu += score_for_side_odd
        if tablero[2][0] == state.player1.label:
            heu += score_for_side_even
        if tablero[7][0] != '.':
            if tablero[3][0] == state.player1.label:
                heu += score_for_side_odd
            if tablero[4][0] == state.player1.label:
                heu += score_for_side_even

    if tablero[0][7] == '.':
        # Sides that will try to get the control of the corner
        if tablero[0][6] == state.player1.label:
            heu += score_for_side_odd
        if tablero[0][5] == state.player1.label:
            heu += score_for_side_even
        if tablero[0][0] != '.':
            if tablero[0][4] == state.player1.label:
                heu += score_for_side_odd
            if tablero[0][3] == state.player1.label:
                heu += score_for_side_even

        if tablero[1][7] == state.player1.label:
            heu += score_for_side_odd
        if tablero[2][7] == state.player1.label:
            heu += score_for_side_even
        if tablero[7][7] != '.':
            if tablero[3][7] == state.player1.label:
                heu += score_for_side_odd
            if tablero[4][7] == state.player1.label:
                heu += score_for_side_even

    if tablero[7][0] == '.':
        # Sides that will try to get the control of the corner
        if tablero[7][1] == state.player1.label:
            heu += score_for_side_odd
        if tablero[7][2] == state.player1.label:
            heu += score_for_side_even
        if tablero[7][7] != '.':
            if tablero[7][3] == state.player1.label:
                heu += score_for_side_odd
            if tablero[7][4] == state.player1.label:
                heu += score_for_side_even

        if tablero[6][0] == state.player1.label:
            heu += score_for_side_odd
        if tablero[5][0] == state.player1.label:
            heu += score_for_side_even
        if tablero[0][0] != '.':
            if tablero[4][0] == state.player1.label:
                heu += score_for_side_odd
            if tablero[3][0] == state.player1.label:
                heu += score_for_side_even

    if tablero[7][7] == '.':
        # Sides that will try to get the control of the corner
        if tablero[7][6] == state.player1.label:
            heu += score_for_side_odd
        if tablero[7][5] == state.player1.label:
            heu += score_for_side_even
        if tablero[7][0] != '.':
            if tablero[7][4] == state.player1.label:
                heu += score_for_side_odd
            if tablero[7][3] == state.player1.label:
                heu += score_for_side_even

        if tablero[6][7] == state.player1.label:
            heu += score_for_side_odd
        if tablero[5][7] == state.player1.label:
            heu += score_for_side_even
        if tablero[0][7] != '.':
            if tablero[4][7] == state.player1.label:
                heu += score_for_side_odd
            if tablero[3][7] == state.player1.label:
                heu += score_for_side_even

    # Intern square
    for i in range(2, 6):
        for j in range(2, 6):
            if tablero[i][j] == state.player1.label:
                heu += score_for_inter
            if tablero[i][j] == state.player2.label:
                heu -= score_for_inter

    # Extern square
    for i in range(1, 7):
        if tablero[1][i] == state.player1.label:
            heu -= score_for_exter
        if tablero[6][i] == state.player1.label:
            heu -= score_for_exter

        if tablero[1][i] == state.player2.label:
            heu += score_for_exter
        if tablero[6][i] == state.player2.label:
            heu += score_for_exter

        if tablero[i][1] == state.player1.label:
            heu -= score_for_exter
        if tablero[i][6] == state.player1.label:
            heu -= score_for_exter

        if tablero[i][1] == state.player2.label:
            heu += score_for_exter
        if tablero[i][6] == state.player2.label:
            heu += score_for_exter

    # Depending on the match
    if state.is_player_max(state.player1):
        return heu
    else:
        return - heu


def quitate_el_topV2(state: TwoPlayerGameState) -> float:
    """
    Evolution of mambo.
    Still prioriazing corners and sides, but also takes into account parity and mobility.
    """
    # Set up constants
    height = 8
    width = 8
    score_for_corner = 100
    score_for_corner_diagonal = -50
    score_odd_distance_1 = -30
    score_even_distance_2 = 6
    score_base_lateral = 2
    score_for_firstLevel_inner = 2
    score_for_secondLevel_inner = 4
    score_for_player_mobility = 6
    score_for_flipped_spaces = 120

    heu = 0

    tablero = from_dictionary_to_array_board(state.board, height, width)

    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    corners_diagonal = [(1, 1), (1, 6), (6, 1), (6, 6)]
    odd_distance_1 = [(0, 1), (1, 0), (0, 6), (6, 0),
                      (1, 7), (7, 1), (6, 7), (7, 6)]
    even_distance_2 = [(0, 2), (2, 0), (0, 5), (5, 0),
                       (2, 7), (7, 2), (5, 7), (7, 5)]
    base_lateral = [(0, 3), (3, 0), (0, 4), (4, 0),
                    (3, 7), (7, 3), (4, 7), (7, 4)]
    firstLevel_inner = [(2, 2), (2, 3), (2, 4), (2, 5), (3, 2),
                        (3, 5), (4, 2), (4, 5), (5, 2), (5, 3), (5, 4), (5, 5)]
    secondLevel_inner = [(3, 3), (3, 4), (4, 3), (4, 4)]

    # Count corners for player 1 and 2
    for corner in corners:
        if tablero[corner[0]][corner[1]] == state.player1.label:
            heu += score_for_corner
        elif tablero[corner[0]][corner[1]] == state.player2.label:
            heu -= score_for_corner

    # Si ningun jugador tiene una esquina no hace falta calcular
    if heu != 0:
        heu += _calculo_flipped_spaces(state, state.player1.label,
                                       tablero) * score_for_flipped_spaces
        heu -= _calculo_flipped_spaces(state, state.player2.label,
                                       tablero) * score_for_flipped_spaces

    # Count corners diagonal for player 1 and 2
    for tile in corners_diagonal:
        if tablero[tile[0]][tile[1]] == state.player1.label:
            heu += score_for_corner_diagonal
        elif tablero[tile[0]][tile[1]] == state.player2.label:
            heu -= score_for_corner_diagonal

    # Count odd distance 1 for player 1 and 2
    for odd in odd_distance_1:
        if tablero[odd[0]][odd[1]] == state.player1.label:
            heu += score_odd_distance_1
        elif tablero[odd[0]][odd[1]] == state.player2.label:
            heu -= score_odd_distance_1

    # Count even distance 2 for player 1 and 2
    for even in even_distance_2:
        if tablero[even[0]][even[1]] == state.player1.label:
            heu += score_even_distance_2
        elif tablero[even[0]][even[1]] == state.player2.label:
            heu -= score_even_distance_2

    # Count base lateral for player 1 and 2
    for base in base_lateral:
        if tablero[base[0]][base[1]] == state.player1.label:
            heu += score_base_lateral
        elif tablero[base[0]][base[1]] == state.player2.label:
            heu -= score_base_lateral

    # Count first level inner for player 1 and 2
    for first in firstLevel_inner:
        if tablero[first[0]][first[1]] == state.player1.label:
            heu += score_for_firstLevel_inner
        elif tablero[first[0]][first[1]] == state.player2.label:
            heu -= score_for_firstLevel_inner

    # Count second level inner for player 1 and 2
    for second in secondLevel_inner:
        if tablero[second[0]][second[1]] == state.player1.label:
            heu += score_for_secondLevel_inner + score_for_firstLevel_inner
        elif tablero[second[0]][second[1]] == state.player2.label:
            heu -= score_for_secondLevel_inner + score_for_firstLevel_inner

    # Player movement diff
    player_mobility = len(state.game._get_valid_moves(
        state.board, state.next_player.label))

    # Obtener numero de fichas del tablero
    coins_player1 = 0
    coins_player2 = 0
    for i in range(0, 8):
        for j in range(0, 8):
            if tablero[i][j] == state.player1.label:
                coins_player1 += 1
            if tablero[i][j] == state.player2.label:
                coins_player2 += 1
    coins = coins_player1 + coins_player2
    heu -= player_mobility * coins/64 * score_for_player_mobility

    # Teorico final con victoria
    if player_mobility == 0 and (coins_player2 == 0 or coins == 64):
        if coins_player1 > coins_player2:
            heu += 1000000
        else:
            heu -= 1000000

    if coins >= 63:
        heu = coins_player1 - coins_player2

    # Depending on the match
    if state.is_player_max(state.player1):
        return heu
    else:
        return - heu


def rayo_barcelona(state: TwoPlayerGameState) -> float:
    """
    Evolution of mambo.
    Still prioriazing corners and sides, but also takes into account parity and mobility.
    """
    # Set up constants
    height = 8
    width = 8
    score_for_corner = 25
    score_for_side_odd = -20
    score_for_side_even = 20
    score_for_inter = 1
    score_for_exter = -3
    score_for_player_mobility = 5
    score_for_coins = 18
    score_for_flipped_spaces = 0
    heu = 0

    tablero = from_dictionary_to_array_board(state.board, height, width)

    # Player movement diff
    player_mobility = len(state.game._get_valid_moves(
        state.board, state.next_player.label))

    # Obtener numero de fichas del tablero
    coins_player1 = 0
    coins_player2 = 0
    for i in range(0, 8):
        for j in range(0, 8):
            if tablero[i][j] == state.player1.label:
                coins_player1 += 1
            if tablero[i][j] == state.player2.label:
                coins_player2 += 1
    coins = coins_player1 + coins_player2

    # Count corners for player 1
    score_gradual_corner_value = (-(coins**20)/64**20 + 1) * score_for_corner

    if tablero[0][0] == state.player1.label:
        heu += score_gradual_corner_value
    if tablero[0][height - 1] == state.player1.label:
        heu += score_gradual_corner_value
    if tablero[width - 1][0] == state.player1.label:
        heu += score_gradual_corner_value
    if tablero[width - 1][height - 1] == state.player1.label:
        heu += score_gradual_corner_value

    # Count corners for player 2
    if tablero[0][0] == state.player2.label:
        heu -= score_gradual_corner_value
    if tablero[0][height - 1] == state.player2.label:
        heu -= score_gradual_corner_value
    if tablero[width - 1][0] == state.player2.label:
        heu -= score_gradual_corner_value
    if tablero[width - 1][height - 1] == state.player2.label:
        heu -= score_gradual_corner_value

    # Count sides take into account parity
    if tablero[0][0] == '.':
        # Sides that will try to get the control of the corner
        if tablero[0][1] == state.player1.label:
            heu += score_for_side_odd
        if tablero[0][2] == state.player1.label:
            heu += score_for_side_even
        if tablero[0][7] != '.':
            if tablero[0][3] == state.player1.label:
                heu += score_for_side_odd
            if tablero[0][4] == state.player1.label:
                heu += score_for_side_even

        if tablero[1][0] == state.player1.label:
            heu += score_for_side_odd
        if tablero[2][0] == state.player1.label:
            heu += score_for_side_even
        if tablero[7][0] != '.':
            if tablero[3][0] == state.player1.label:
                heu += score_for_side_odd
            if tablero[4][0] == state.player1.label:
                heu += score_for_side_even

    if tablero[0][7] == '.':
        # Sides that will try to get the control of the corner
        if tablero[0][6] == state.player1.label:
            heu += score_for_side_odd
        if tablero[0][5] == state.player1.label:
            heu += score_for_side_even
        if tablero[0][0] != '.':
            if tablero[0][4] == state.player1.label:
                heu += score_for_side_odd
            if tablero[0][3] == state.player1.label:
                heu += score_for_side_even

        if tablero[1][7] == state.player1.label:
            heu += score_for_side_odd
        if tablero[2][7] == state.player1.label:
            heu += score_for_side_even
        if tablero[7][7] != '.':
            if tablero[3][7] == state.player1.label:
                heu += score_for_side_odd
            if tablero[4][7] == state.player1.label:
                heu += score_for_side_even

    if tablero[7][0] == '.':
        # Sides that will try to get the control of the corner
        if tablero[7][1] == state.player1.label:
            heu += score_for_side_odd
        if tablero[7][2] == state.player1.label:
            heu += score_for_side_even
        if tablero[7][7] != '.':
            if tablero[7][3] == state.player1.label:
                heu += score_for_side_odd
            if tablero[7][4] == state.player1.label:
                heu += score_for_side_even

        if tablero[6][0] == state.player1.label:
            heu += score_for_side_odd
        if tablero[5][0] == state.player1.label:
            heu += score_for_side_even
        if tablero[0][0] != '.':
            if tablero[4][0] == state.player1.label:
                heu += score_for_side_odd
            if tablero[3][0] == state.player1.label:
                heu += score_for_side_even

    if tablero[7][7] == '.':
        # Sides that will try to get the control of the corner
        if tablero[7][6] == state.player1.label:
            heu += score_for_side_odd
        if tablero[7][5] == state.player1.label:
            heu += score_for_side_even
        if tablero[7][0] != '.':
            if tablero[7][4] == state.player1.label:
                heu += score_for_side_odd
            if tablero[7][3] == state.player1.label:
                heu += score_for_side_even

        if tablero[6][7] == state.player1.label:
            heu += score_for_side_odd
        if tablero[5][7] == state.player1.label:
            heu += score_for_side_even
        if tablero[0][7] != '.':
            if tablero[4][7] == state.player1.label:
                heu += score_for_side_odd
            if tablero[3][7] == state.player1.label:
                heu += score_for_side_even

    # Intern square
    for i in range(2, 6):
        for j in range(2, 6):
            if tablero[i][j] == state.player1.label:
                heu += score_for_inter
            if tablero[i][j] == state.player2.label:
                heu -= score_for_inter

    # Extern square
    for i in range(1, 7):
        if tablero[1][i] == state.player1.label:
            heu += score_for_exter
        if tablero[6][i] == state.player1.label:
            heu += score_for_exter

        if tablero[1][i] == state.player2.label:
            heu -= score_for_exter
        if tablero[6][i] == state.player2.label:
            heu -= score_for_exter

        if tablero[i][1] == state.player1.label:
            heu += score_for_exter
        if tablero[i][6] == state.player1.label:
            heu += score_for_exter

        if tablero[i][1] == state.player2.label:
            heu -= score_for_exter
        if tablero[i][6] == state.player2.label:
            heu -= score_for_exter

    # Restamos mobilidad del jugador (cuanto mayor sea la mobilidad del rival, peor para el usuario)
    heu += player_mobility * coins**2/64**2 * score_for_player_mobility

    # Diferencia de monedas (mas importante a final de partida)
    heu += coins**5 / 64**5 * (coins_player1 - coins_player2) * score_for_coins

    # Teorico final con victoria
    if player_mobility == 0 and (coins_player2 == 0 or coins == 64):
        if coins_player1 > coins_player2:
            heu += 1000000
        else:
            heu += 1000000

    # CODIGO AÑADIDO
    # Añado importancia de las fichas volteadas
    heu += _calculo_flipped_spaces(state, state.player1.label,
                                   tablero) * score_for_flipped_spaces
    heu -= _calculo_flipped_spaces(state, state.player2.label,
                                   tablero) * score_for_flipped_spaces

    # Depending on the match
    if state.is_player_max(state.player1):
        return heu
    else:
        return - heu

# CODIGO AÑADIDO
# ---------------------auxiliar flipped spaces---------------------#


def _calculo_flipped_spaces(state, player_label, tablero) -> int:
    '''
    Calcula el numero de fichas que el rival no te puede robar 
    '''
    flipped_spaces = 0
    flipped_spaces_matrix = np.zeros((state.game.height, state.game.width))

    # Para facilitar lectura de codigo
    corners = [(0, 0), (0, 7), (7, 7), (7, 0)]
    top_edge = [(x, 0) for x in range(1, 7)]
    right_edge = [(7, y) for y in range(1, 7)]
    bottom_edge = [(x, 7) for x in range(1, 7)]
    left_edge = [(0, y) for y in range(1, 7)]

    # Itero sobre las esquinas, y si es mia la marco como flipped
    for corner in corners:
        if tablero[corner[0]][corner[1]] == player_label:
            flipped_spaces_matrix[corner[0]][corner[1]] = 1

    # Consigo casillas flipped borde superior
    for c in top_edge:
        if tablero[c[0]][c[1]] == player_label:
            if (flipped_spaces_matrix[c[0]-1][c[1]] == 1) or (flipped_spaces_matrix[c[0]+1][c[1]] == 1):
                flipped_spaces_matrix[c[0]][c[1]] = 1

    # Consigo casillas flipped borde derecho
    for c in right_edge:
        if tablero[c[0]][c[1]] == player_label:
            if (flipped_spaces_matrix[c[0]][c[1]-1] == 1) or (flipped_spaces_matrix[c[0]][c[1]+1] == 1):
                flipped_spaces_matrix[c[0]][c[1]] = 1

    # Consigo casillas flipped borde inferior
    for c in bottom_edge:
        if tablero[c[0]][c[1]] == player_label:
            if (flipped_spaces_matrix[c[0]-1][c[1]] == 1) or (flipped_spaces_matrix[c[0]+1][c[1]] == 1):
                flipped_spaces_matrix[c[0]][c[1]] = 1

    # Consigo casillas flipped borde izquierdo
    for c in left_edge:
        if tablero[c[0]][c[1]] == player_label:
            if (flipped_spaces_matrix[c[0]][c[1]-1] == 1) or (flipped_spaces_matrix[c[0]][c[1]+1] == 1):
                flipped_spaces_matrix[c[0]][c[1]] = 1

    # REVISAR ESTO??
    # Consigo casillas flipped internas
    for i in range(1, 7):
        for j in range(1, 7):
            if tablero[i][j] == player_label:
                if ((flipped_spaces_matrix[i-1][j] == 1) and (flipped_spaces_matrix[i][j-1] == 1)) or ((flipped_spaces_matrix[i+1][j] == 1) or (flipped_spaces_matrix[i][j+1] == 1)):
                    flipped_spaces_matrix[i][j] = 1

    # Sumo el numero de casillas flipped
    for i in range(state.game.height):
        for j in range(state.game.width):
            if flipped_spaces_matrix[i][j] == 1:
                flipped_spaces += 1

    return flipped_spaces

    if flipped_spaces != 0:
        for i in range(0, 8):
            print(tablero[i])
        for i in range(0, 8):
            print(flipped_spaces_matrix[i])
        print("flipped spaces: ", flipped_spaces, player_label)
    return flipped_spaces


# ------------- ANTONIO -----------------------
# ----------------------------------rewards and penalties----------------------------------#
mobility_reward = 50
coin_reward = 10
stable_position_reward = 20

corner_reward = 100
X_squares_penalty = -50
C_squares_penalty = -30
B_squares_reward = 2
A_squares_reward = 6

inner_square_count_reward = 10


# ----------------------------------positions----------------------------------#

# top left, top right,  bottom right, bottom left
corners = [(0, 0), (0, 7), (7, 7), (7, 0)]

# top edge, right edge, bottom edge, left edge, excluding corners
edge_positions = [
    (x, 0) for x in range(1, 7)] + [(7, y) for y in range(1, 7)] + [(x, 7) for x in range(1, 7)] + [(0, y) for y in range(1, 7)
                                                                                                    ]
top_edge = [(x, 0) for x in range(1, 7)]
right_edge = [(7, y) for y in range(1, 7)]
bottom_edge = [(x, 7) for x in range(1, 7)]
left_edge = [(0, y) for y in range(1, 7)]

# top left, top right, bottom right, bottom left
X_squares = [(1, 1), (6, 1), (6, 6), (1, 6)]

# top left, top right, bottom left, bottom right
C_squares = [(0, 1), (1, 0), (6, 0), (7, 1), (0, 6), (1, 7), (6, 7), (7, 6)]

# top edge, right edge, bottom edge, left edge, excluding corners
B_squares = [(3, 0), (4, 0), (7, 3), (7, 4), (3, 7), (4, 7), (0, 3), (0, 4)]

# top edge, right edge, bottom edge, left edge, excluding corners
A_squares = [(2, 0), (5, 0), (7, 2), (7, 5), (2, 7), (5, 7), (0, 2), (0, 5)]

# inner squares


def inner_squares():
    inner_square_discs = []
    for i in range(2, 6):
        for j in range(2, 6):
            inner_square_discs.append((i, j))
    return inner_square_discs


# ----------------------------------Directions to center----------------------------------#
Top_left = (1, 1)
Top = (0, 1)
Top_right = (-1, 1)
Right = (-1, 0)
Bottom_right = (-1, -1)
Bottom = (0, -1)
Bottom_left = (1, -1)
Left = (1, 0)

# fair game overall


def optimal_heuristic(state: TwoPlayerGameState) -> float:
    mobility_reward = 20
    stable_position_reward = 20
    coin_reward = 0
    board_array = from_dictionary_to_array_board(
        state.board, state.game.height, state.game.width)

    # Weighted evaluation based on different features of the game state.
    evaluation = 0.0
    # 1. Mobility: Encourage moves that maximize available moves.
    player1_mobility = len(state.game._get_valid_moves(
        state.board, state.player1.label))
    player2_mobility = len(state.game._get_valid_moves(
        state.board, state.player2.label))

    # 2. Coin Parity: Encourage having more discs than the opponent.
    player1_coins = state.game._player_coins(state.board, state.player1.label)
    player2_coins = state.game._player_coins(state.board, state.player2.label)

    # redirect depending on the game state
    if player1_coins + player2_coins < 18:
        return minimal_disks_strategy(state)
    if player1_coins + player2_coins >= 50:  # 48 or 50 seems to work well
        return endgame_strat(state)
    x = player1_coins + player2_coins
    if x > 62:
        coin_reward = x
    # 3. Corner Control: Encourage controlling the corners of the board.

    player1_corner = _corner_count(
        state, state.game.player1.label, board_array)
    player2_corner = _corner_count(
        state, state.game.player2.label, board_array)

    # 4. Edge Control: Encourage controlling the edges of the board.
    player1_edges = _border_count(state, state.player1.label, board_array)
    player2_edges = _border_count(state, state.player2.label, board_array)

    # 5. Worst positions: Encourage not having X_squares positions.
    player1_worst_positions = _worst_positions_count(
        state, state.player1.label, board_array)
    player2_worst_positions = _worst_positions_count(
        state, state.player2.label, board_array)

    # 7. Stable positions: Encourage having stable positions.
    player1_stable_positions = _stable_discs_count(
        state, state.player1.label, board_array)
    player2_stable_positions = _stable_discs_count(
        state, state.player2.label, board_array)

    # add the rewards and penalties
    evaluation += (player1_coins*coin_reward +
                   player1_corner*corner_reward + player1_edges +
                   player1_worst_positions*X_squares_penalty + player1_stable_positions*stable_position_reward +
                   player1_mobility*mobility_reward
                   )

    evaluation -= (player2_mobility*mobility_reward + player2_coins*coin_reward +
                   player2_corner*corner_reward +
                   player2_edges + player2_worst_positions * X_squares_penalty +
                   player2_stable_positions*stable_position_reward
                   )

    if state.is_player_max(state.player1):
      # print("Heuristic value_max:  " + str(normalized_evaluation) + "\n")
      return evaluation
    else:
      # print("Heuristic value_min:  " + str(-normalized_evaluation) + "\n")
      return -evaluation

# ---------------------------------Auxiliary functions---------------------------------#


def _border_count(state: TwoPlayerGameState, label, board_array) -> float:

    count = 0
    for position in edge_positions:
        if board_array[position[0]][position[1]] == label:
            if position in A_squares:
                count += 1*A_squares_reward
            if position in B_squares:
                count += 1*B_squares_reward
            if position in C_squares:
                count += 1*C_squares_penalty

    # print("Heuristic border value:  " + str(count) + "\n")
    return count


def _corner_count(state: TwoPlayerGameState, label, board_array) -> float:

    count = 0
    for position in corners:
        if board_array[position[0]][position[1]] == label:
            count += 1
    # print("Heuristic corner value:  " + str(count) + "\n")

    return count


def _worst_positions_count(state: TwoPlayerGameState, label, board_array) -> float:

    count = 0
    for position in X_squares:
        if board_array[position[0]][position[1]] == label:
            count += 1
    # print("Heuristic bad positions value:  " + str(count) + "\n")
    return count


def _inner_square_count(state: TwoPlayerGameState, label, board_array) -> float:
    inner_square_discs = 0
    for i in range(2, 6):
        for j in range(2, 6):
            if board_array[i][j] == label:
                inner_square_discs += 1

    return inner_square_discs


def center_count(state: TwoPlayerGameState, label, board_array) -> float:
    center_discs = 0
    for i in range(3, 5):
        for j in range(3, 5):
            if board_array[i][j] == label:
                center_discs += 1

    return center_discs

# the greater the eval, the best for current player


def check_opponents_options_early(state: TwoPlayerGameState, label, board_array, opponents_moves):
    print("opponents moves: ", opponents_moves)
    inner_square = inner_squares()
    eval = 0
    for position in opponents_moves:
        if position not in inner_square:
            eval += 5
        else:
            eval -= 5
    return eval


def _stable_discs_count(state: TwoPlayerGameState, label, board_array) -> float:
    count = 0
    visited = np.zeros((state.game.height, state.game.width))

    # initial borders
    for i in range(state.game.height):
        for j in range(state.game.width):
            if board_array[i][j] == label:
                if (i, j) in (corners):
                    visited[i][j] = 1

    for k in range(state.game.height-2):  # this is to avoid skipping right and bottom edges
        for i in range(state.game.height):
            for j in range(state.game.width):
                if board_array[i][j] == label:

                    # top edge
                    if (i, j) in (top_edge) and ((visited[0, 0] == 1 and visited[i-1, j] == 1) or (visited[7, 0] == 1 and visited[i+1, j] == 1)):
                        visited[i][j] = 1

                    # right edge
                    if (i, j) in (right_edge) and ((visited[7, 0] == 1 and visited[i, j-1] == 1) or (visited[7, 7] == 1 and visited[i, j+1] == 1)):
                        visited[i][j] = 1

                    # bottom edge
                    if (i, j) in (bottom_edge) and ((visited[7, 7] == 1 and visited[i+1, j] == 1) or (visited[0, 7] == 1 and visited[i-1, j] == 1)):
                        visited[i][j] = 1

                    # left edge
                    if (i, j) in (left_edge) and ((visited[0, 7] == 1 and visited[i, j+1] == 1) or (visited[0, 0] == 1 and visited[i, j-1] == 1)):
                        visited[i][j] = 1

    # completing the matrix
    for i in range(state.game.height):
        for j in range(state.game.width):
            current_position = (i, j)
            # top left portion
            if visited[0, 0] == 1 and current_position not in (corners) and current_position not in edge_positions:
                if visited[i-1, j] == 1 and visited[i, j-1] == 1 and board_array[i][j] == label:
                    visited[i, j] = 1
            # top right portion
            if visited[0, 7] == 1 and current_position not in (corners) and current_position not in edge_positions:
                if visited[i+1, j] == 1 and visited[i, j-1] == 1 and board_array[i][j] == label:
                    visited[i, j] = 1
            # bottom right portion
            if visited[7, 7] == 1 and current_position not in (corners) and current_position not in edge_positions:
                if visited[i+1, j] == 1 and visited[i, j+1] == 1 and board_array[i][j] == label:
                    visited[i, j] = 1
            # bottom left portion
            if visited[7, 0] == 1 and current_position not in (corners) and current_position not in edge_positions:
                if visited[i-1, j] == 1 and visited[i, j+1] == 1 and board_array[i][j] == label:
                    visited[i, j] = 1

    for i in range(state.game.height):
        for j in range(state.game.width):
           if visited[i][j] == 1:
            count += 1

    return count


def parity_evaluation(state: TwoPlayerGameState, board_array):
    # first we divide the board in four quadrants
    quadrants = [[], [], [], []]

    # upper left quadrant
    for i in range(0, 3):
        for j in range(0, 3):
            quadrants[0].append((i, j))

    # up right quadrant
    for i in range(5, 8):
        for j in range(0, 3):
            quadrants[1].append((i, j))

    # down right quadrant
    for i in range(5, 8):
        for j in range(5, 8):
            quadrants[2].append((i, j))

    # down left quadrant
    for i in range(0, 3):
        for j in range(5, 8):
            quadrants[3].append((i, j))
    # now we count the number of empty squares in each quadrant
    empty_squares = [0, 0, 0, 0]
    for i in range(4):
        for position in quadrants[i]:
            x, y = position
            if board_array[x][y] != state.player1.label and board_array[x][y] != state.player2.label:
                empty_squares[i-1] += 1

    return empty_squares


def minimal_disks_strategy(state: TwoPlayerGameState) -> float:
    mobility_reward = 20
    if state.is_player_max(state.player1):
        coin_reward = -1
    else:
        coin_reward = -5
    inner_square_count_reward = 10
    center_count_reward = 7
    board_array = from_dictionary_to_array_board(
        state.board, state.game.height, state.game.width)

    # Weighted evaluation based on different features of the game state.
    evaluation = 0.0
    # 1. Mobility: Encourage moves that maximize available moves.
    player1_mobility = len(state.game._get_valid_moves(
        state.board, state.player1.label))
    player2_mobility = len(state.game._get_valid_moves(
        state.board, state.player2.label))

    # 2. Coin Parity: Encourage having more discs than the opponent.
    player1_coins = state.game._player_coins(state.board, state.player1.label)
    player2_coins = state.game._player_coins(state.board, state.player2.label)

    # 3. Corner Control: Encourage controlling the corners of the board.

    player1_corner = _corner_count(
        state, state.game.player1.label, board_array)
    player2_corner = _corner_count(
        state, state.game.player2.label, board_array)

    # 4. Edge Control: Encourage controlling the edges of the board.
    player1_edges = _border_count(state, state.player1.label, board_array)
    player2_edges = _border_count(state, state.player2.label, board_array)

    # 5. Worst positions: Encourage not having X_squares positions.
    player1_worst_positions = _worst_positions_count(
        state, state.player1.label, board_array)
    player2_worst_positions = _worst_positions_count(
        state, state.player2.label, board_array)

    # 6 Inner square control
    player1_inner_square = _inner_square_count(
        state, state.player1.label, board_array)
    player2_inner_square = _inner_square_count(
        state, state.player2.label, board_array)

    """#7 center control
    player1_center = center_count(state, state.player1.label, board_array)   
    player2_center = center_count(state, state.player2.label, board_array)"""

    # 8 check opponents options
    """opponents_moves_player1 = state.game._get_valid_moves(state.board, state.player2.label)
    evaluation+=check_opponents_options_early(state, state.player2.label, board_array, opponents_moves_player1)
    opponents_moves_player2 = state.game._get_valid_moves(state.board, state.player1.label)
    evaluation -=check_opponents_options_early(state, state.player1.label, board_array, opponents_moves_player2)"""

    # add the rewards and penalties
    evaluation += (player1_coins*coin_reward +
                   player1_corner*corner_reward + player1_edges +
                   player1_worst_positions*X_squares_penalty + player1_inner_square*inner_square_count_reward +
                   player1_mobility*mobility_reward
                   )

    evaluation -= (player2_mobility*mobility_reward + player2_coins*coin_reward +
                   player2_corner*corner_reward +
                   player2_edges + player2_worst_positions * X_squares_penalty +
                   player2_inner_square*inner_square_count_reward

                   )

    if state.is_player_max(state.player1):
      # print("Heuristic value_max:  " + str(normalized_evaluation) + "\n")

      return evaluation
    else:
      # print("Heuristic value_min:  " + str(-normalized_evaluation) + "\n")
      return -evaluation


# in development
def endgame_strat(state: TwoPlayerGameState) -> float:
    mobility_reward = 42  # was 20
    stable_position_reward = 50
    corner_reward = 60  # nueva
    board_array = from_dictionary_to_array_board(
        state.board, state.game.height, state.game.width)

    # Weighted evaluation based on different features of the game state.
    evaluation = 0.0
    # 1. Mobility: Encourage moves that maximize available moves.
    player1_mobility = len(state.game._get_valid_moves(
        state.board, state.player1.label))
    player2_mobility = len(state.game._get_valid_moves(
        state.board, state.player2.label))

    # 2. Coin Parity: Encourage having more discs than the opponent.
    player1_coins = state.game._player_coins(state.board, state.player1.label)
    player2_coins = state.game._player_coins(state.board, state.player2.label)

    # set a linear increase of the coin reward as the game concludes
    x = player1_coins + player2_coins
    coin_reward = (20+(x-57))

    # 3. Corner Control: Encourage controlling the corners of the board.

    player1_corner = _corner_count(
        state, state.game.player1.label, board_array)
    player2_corner = _corner_count(
        state, state.game.player2.label, board_array)

    # 4. Edge Control: Encourage controlling the edges of the board.
    player1_edges = _border_count(state, state.player1.label, board_array)
    player2_edges = _border_count(state, state.player2.label, board_array)

    # 5. Worst positions: Encourage not having X_squares positions.
    player1_worst_positions = _worst_positions_count(
        state, state.player1.label, board_array)
    player2_worst_positions = _worst_positions_count(
        state, state.player2.label, board_array)

    # 7. Stable positions: Encourage having stable positions.
    player1_stable_positions = _stable_discs_count(
        state, state.player1.label, board_array)
    player2_stable_positions = _stable_discs_count(
        state, state.player2.label, board_array)

    # basically seek parity, if it is not in your favour, try get an extra move by forcing the opponent to 0 mobility
    if state.previous_player == state.player2:
        if player2_mobility == 0 and (parity_evaluation(state, board_array)[0] +
                                      parity_evaluation(state, board_array)[1] +
                                      parity_evaluation(state, board_array)[2] +
                                      parity_evaluation(state, board_array)[3]) % 2 != 0:
            evaluation += 100
    else:
        if player1_mobility == 0 and (parity_evaluation(state, board_array)[0] +
                                      parity_evaluation(state, board_array)[1] +
                                      parity_evaluation(state, board_array)[2] +
                                      parity_evaluation(state, board_array)[3]) % 2 != 0:
            evaluation -= 100

    # Seek parity (on your turn, all quadrants must be even)
    if parity_evaluation(state, board_array)[0] % 2 == 0 and parity_evaluation(state, board_array)[0] != 0:
        if state.is_player_max(state.player1):
            evaluation += 50
    else:
        evaluation -= 50

    if parity_evaluation(state, board_array)[1] % 2 == 0 and parity_evaluation(state, board_array)[1] != 0:
        if state.is_player_max(state.player1):
            evaluation += 50
    else:
        evaluation -= 50

    if parity_evaluation(state, board_array)[2] % 2 == 0 and parity_evaluation(state, board_array)[2] != 0:
        if state.is_player_max(state.player1):
            evaluation += 50
    else:
        evaluation -= 50

    if parity_evaluation(state, board_array)[3] % 2 == 0 and parity_evaluation(state, board_array)[3] != 0:
        if state.is_player_max(state.player1):
            evaluation += 50
        else:
            evaluation -= 50

    # add the rewards and penalties
    if (player1_coins + player2_coins <= 62):

        evaluation += (player1_coins*coin_reward +
                       player1_corner*corner_reward + player1_edges +
                       player1_worst_positions*X_squares_penalty + player1_stable_positions*stable_position_reward +
                       player1_mobility*mobility_reward
                       )

        evaluation -= (player2_mobility*mobility_reward + player2_coins*coin_reward +
                       player2_corner*corner_reward +
                       player2_edges + player2_worst_positions * X_squares_penalty +
                       player2_stable_positions*stable_position_reward +
                       player2_mobility*mobility_reward
                       )
    else:
        evaluation += (player1_coins - player2_coins)

    if state.is_player_max(state.player1):
      # print("Heuristic value_max:  " + str(normalized_evaluation) + "\n")

      return evaluation
    else:
      # print("Heuristic value_min:  " + str(-normalized_evaluation) + "\n")
      return -evaluation
