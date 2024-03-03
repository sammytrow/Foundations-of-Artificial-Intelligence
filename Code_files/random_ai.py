from agent_methods import *
from random import randint
from model import *
import model


def random_ship_start(player,board):
    board_set = list(get_available_ship_spaces(player,board))
    len_needed = length_needed(player,board)
    for i in range(len(board_set)):
        rand = randint(0, len(board_set) - 1)  # rand int between 0 and len(board)-1 due to indexing
        #print("random ship start = ", board_set[rand])
        # check if ship is valid, need [board[rand]] as is_valid_ship_from expects list
        if valid_ships_from(board_set[rand], len_needed, player, board) != []:
            return board_set[rand]
 #       else:
 #           if player.value == 0:
 #               globals.cannot_lay_blue.append(board[rand])
 #           else:
 #               globals.cannot_lay_red.append(board[rand])
 #   return ('no','no')



def random_ship_end(loc, player,board):
    len_needed = length_needed(player,board)
    valid_ships = valid_ships_from(loc, len_needed, player, board)
    rand = randint(0, len(valid_ships) - 1)  # pick random ship (of length len_needed)
    ship_end = valid_ships[rand][len_needed - 1]  # pick the last element of the random ship
    # since ship starts from ship_start
    return ship_end


def random_attempt(player, board):
    possible_attempts = get_available_attempts(player, board)
    possible_attempts = list(possible_attempts)
    if not possible_attempts:
        return None
    rand = randint(0, len(possible_attempts) - 1)
    return possible_attempts[rand]
