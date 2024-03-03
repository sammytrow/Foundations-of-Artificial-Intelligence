from model import *
from random_ai import *
from model import *
from heuristic_methods import *
from random import shuffle
from itertools import compress
import random


def ship_end(cell,len, player, board):
    ships = valid_ships_from(cell,len, player, board)
    return [(ship[0],ship[-1]) for ship in ships]

def heuristic_ship(player, board):
    len_needed = length_needed(player,board)
    board_set = list(set(get_available_ship_spaces(player,board)))
    counter = []
    board.ship_heuristic = []
    shuffle(board_set) #randomise the order
    for cell in board_set:
        cell_score = [get_boundaries(cell, dir) in board_set for dir in
                          [(1, 0), (0, -1), (-1, 0), (0, 1), (1, 1), (-1, -1), (1, -1), (-1, 1)]].count(True)
        #print("cell score",cell_score)
        ships = ship_end(cell,len_needed, player, board)
        valid_ships = valid_ships_from(cell, len_needed, player, board)
        if valid_ships == []:
            continue
        ship_score = [[get_boundaries(ship[1], dir) in board_set for dir in
                                        [(1, 0), (0, -1), (-1, 0), (0, 1), (1, 1),(-1, -1), (1, -1 ), (-1, 1)]].count(True) for ship in ships]
        #print("ships score",ship_score)
        ships_and_scores = list(zip(ships,ship_score))
        print("ships and scores",ships_and_scores)
        ships_and_scores.sort(reverse=True,key=lambda y:y[1])
        ship_max = ships_and_scores[0]
        board.ship_heuristic.append((cell, ship_max[0], cell_score + ship_max[1]))
        if cell_score + ship_max[1] == 16:
            return cell

        counter.append((cell,ship_max[0],cell_score+ship_max[1]))
        board.ship_heuristic.append((cell,ship_max[0],cell_score+ship_max[1]))

    counter.sort(reverse = True,key=lambda y: y[2])
    return counter[0][0]


def heuristic_ship_end(player, loc, board): #to make this work in the GUI (for testing), only one player can be HEURISTIC
    ship_heur = [x[0] for x in board.ship_heuristic]
    idx = ship_heur.index((loc[0], loc[1]))
    return board.ship_heuristic[idx][1][1]


# def update_heuristic_mode(player,board):
#
#
#     other_player_ships = board.ships_other_player[player.value] # ships of other player
#
#
#     print("player_hit_bool",board.player_hit_bool)
#     print("player_attempts=",player_attempts)
#     print("player_hits=",player_hits)
#     print("coloured_hits=",set(blue_hits_considered if player.value == 0 else red_hits_considered))
#     hits_not_considered = list(set(player_hits).difference(set(player_attempts)).difference(set(crashes))) #need to change this
#     print(hits_not_considered)
#     #if len(player_hits)==0:
#     #    return heuristic_mode.GUESSING_MODE
#     if len(hits_not_considered) > 0:
#         if len(hits_not_considered) > 0:
#             print("hits_not_considered=",hits_not_considered)
#             return heuristic_mode.HIT_MODE
#     else:
#         return heuristic_mode.GUESSING_MODE

def get_parity(loc):
    if (loc[0] + loc[1]) % 2:
        return True # even parity
    else:
        return False #odd parity

def heur_attempt(player, board):
    all_board_attempts = list(get_available_attempts(player, board))
    whole_board = list(set((i, j) for i in range(10) for j in range(10)))
    board.attempt_heuristic = []
    #print("available attempts", board_attempts)
    parities = [get_parity(loc) for loc in all_board_attempts]
    opposite_parities = [not parity for parity in parities]
    if parities.count(True) > parities.count(False): #more even than odd left
        board_attempts = list(compress(all_board_attempts,opposite_parities))#pick odd
    else:
        board_attempts = list(compress(all_board_attempts,parities)) #pick even


    #print("board attempts",board_attempts)
    prior = [0]*len(board_attempts) #initialise scores as 1
    i = 0
    while i < len(board_attempts):
        boundaries = [get_boundaries(board_attempts[i], dir) for dir in
                      [(1, 0), (0, -1), (-1, 0), (0, 1)]]
        for boundary in boundaries:
            if is_outcome_for(True,boundary,player,board):
                prior[i] = prior[i] + 1
            else:
                if boundary in whole_board:
                    prior[i] = prior[i] - 1
        i = i + 1
    scores = list(zip(board_attempts,prior))
    if len(board.attempts[player.value]) < 5:
        scores.sort(reverse=True, key=lambda y: y[1])  # pick near the corners before turn 5
    else:
        scores.sort(reverse=False,key = lambda y:y[1]) # pick where we don't know (minimum score)
    if scores == []:
        return random_attempt(player,board) # this should never be called
    else:
        board.attempt_heuristic.append(scores)
        return scores[0][0]


def heuristic_attempt(player, board):
    other_player_ships = board.ships_other_player[player.value]  # ships of other player
    #print("other_player_ships=",other_player_ships)
    possible_ship_attempts = []
    if other_player_ships == []:
        return heur_attempt(player, board)

    if len(other_player_ships[0]) > 0:
        for ship in other_player_ships:  # loop through current ships of enemy
            if len(ship) < 5:  # if ship definitely not complete
                squares = adjacent_squares(player, ship, board)
                #print("ship",ship,"squares",squares)
                if squares != []:
                    possible_ship_attempts.append(squares)

        if possible_ship_attempts == []:
            return heur_attempt(player, board) #now use attempt heuristic


        print("possible_ship_attempts",possible_ship_attempts)
        possible_attempts = flatten(possible_ship_attempts)
        possible_attempts = [(x,possible_attempts.count(x)) for x in list(set(possible_attempts))]
        print("possible_attempts",possible_attempts)
        possible_attempts.sort(reverse=True,key = lambda y:y[1])
        board.hit_heuristic.append(possible_attempts)
        print("hit heuristic",board.hit_heuristic)
        rand = randint(0, len(possible_attempts) - 1)
        return possible_attempts[0][0] # return most likely attempt
    else:
        return heur_attempt(player, board)


def heuristic(board,player):
    eval = len(board.hits[0]) - len(board.hits[1])
    if player.value == 0:
        return eval
    else:
        return -eval


'''
The heuristic could be: 
Number of enemy hits / number of enemy ships sunk / number of distinct ships hit 
(Number of enemy hits - number of own ship hits) 

'''
