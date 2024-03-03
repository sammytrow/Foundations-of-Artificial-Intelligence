from model import *
from agent_methods import *
from random_ai import *
from heuristic import *


class Mode(Enum):
    PLACE_START = 0,
    PLACE_END = 1,
    ATTEMPT = 2,
    HANDOVER = 3


def get_next_move(mode, player_type, player, selected, heuristic_mode, board):
    '''
    :param mode: This is the enum Mode defined in view.py
    :param player_type: This is the enum Player_Type defined in model.py
    :param player: This is the enum Player defined in model.py
    :param selected: Populated if a start for the ship placement has been selected
    :param heuristic_mode: Populated if using player_type HEURISTIC to indicate if in guessing or hit mode
    :return: tuple(x,y)

    Example calls:
    #Need to chose ship start position for RANDOM player, RED player, no start yet selected
    print(get_next_move(Mode.PLACE_START.value,Player_Type.RANDOM,red_player,None))
    #The first length of a ship is 5, so this will assume that whilst game not playing
    print(get_next_move(Mode.PLACE_END.value), player_Type.RANDOM,red_player,(3,4)))

    '''

    if mode == (0,):  # PLACE_START
        if player_type == Player_Type.RANDOM:
            #print("Random ship placement called")
            return (random_ship_start(player,board))

        elif player_type == Player_Type.HEURISTIC:
            return (heuristic_ship(player,board))

        elif player_type == Player_Type.MINIMAX:
            return (1, 1)

    elif mode == (1,):  # PLACE_END
        if player_type == Player_Type.RANDOM:
            #print("random ship end placement called")
            return (random_ship_end(selected, player,board))

        elif player_type == Player_Type.HEURISTIC:
            return heuristic_ship_end(player, selected, board)

        elif player_type == Player_Type.MINIMAX:
            return (1, 1)

    elif mode == (2,):  # ATTEMPT
        if player_type == Player_Type.RANDOM:
            return (random_attempt(player, board))

        elif player_type == Player_Type.HEURISTIC:
            return (heuristic_attempt(player, board))

        elif player_type == Player_Type.MINIMAX:
            return (1, 1)
    else:
        return None
