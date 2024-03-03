from enum import Enum
from agent_methods import *
'''

We want to create a heuristic that has two different modes:
Guessing Mode
In this mode, to begin with, we will randomly guess until we get a hit. 
This could be improved by favouring middle squares for example. 

Hit Mode
Once we have hit a ship, we want to try adjacent squares to find where the ship is until we are sure we have hit all of it. 

'''


class heuristic_mode(Enum):
    GUESSING_MODE = 0
    HIT_MODE = 1


def valid_ships_for_opponent(loc, len, player, board):
    return [ship for ship in ships_from(loc, len) if is_valid_ship_for_opponent(ship, player, board)]

def is_valid_ship_for_opponent(locs,player,board):
    locations = locs[1:] #consider all squares but the first
    return all([is_valid_attempt_for(loc,player,board) for loc in locations])

def adjacent_squares(player, hits, board):
    board_set = get_available_attempts(player, board)
    #print("board set",board_set)
    #print("set hits",set(hits))
    max_attempts = max([len(attempt) for attempt in board.attempts])
    max_attempts = 5 if max_attempts > 5 else max_attempts
    length_ships = board.lengths_to_lay[player.value][max_attempts - 1]
    if not hits:
        return None

    if hits:
        if len(hits)>1:
            hit_dir = [(hits[1][0] - hits[0][0],hits[1][1]-hits[0][1]),(hits[0][0] - hits[1][0],hits[0][1]-hits[1][1])]
            possible_squares = set(get_boundaries(hit,dir) for hit in hits for dir in hit_dir)
        else:
            print("hits",hits)
            print("length_ships",length_ships)
            valid_ships = valid_ships_for_opponent(hits[0], length_ships, player, board)
            hit_directions = []
            if valid_ships != []:
                for ship in valid_ships:
                    hit_dir = [(ship[1][0] - ship[0][0],ship[1][1]-ship[0][1]),(ship[0][0] - ship[1][0],ship[0][1]-ship[1][1])]
                    hit_directions.append(hit_dir)
            print("hit directions",hit_directions)
            if len(list(set(hit_directions[0]))) == 1:
                possible_squares = set(get_boundaries(hit,dir)  for hit in hits for dir in hit_dir)
            else:
                possible_squares = set(get_boundaries(hit, dir) for hit in hits for dir in [(1, 0), (0, -1), (-1, 0), (0, 1)])
        #print("possible_squares",possible_squares)
        if possible_squares == []:
            return None
        #print("possible squares in board",board_set.intersection(possible_squares))
        return list(board_set.intersection(possible_squares).difference(set(hits)))












#print(adjacent_squares(blue_player,[(1,1),(0,1)]))

