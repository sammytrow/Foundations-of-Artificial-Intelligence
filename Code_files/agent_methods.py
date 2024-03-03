from model import *
import globals

def get_boundaries(loc: list, dir: tuple) -> tuple:
    return (loc[0] + dir[0], loc[1] + dir[1])


def get_available_ship_spaces(player: Enum, board) -> list:
    board_set = set((i, j) for i in range(10) for j in range(10))  # generate a 10*10 board
    my_ships = board.all_ships[player.value]
    ships = set(my_ships[i][j] for i in range(len(my_ships)) for j in
                range(len(my_ships[i])))  # go through elements of a players ships
    ship_boundaries = set(get_boundaries(ship, dir) for ship in ships for dir in
                          [(1, 0), (0, -1), (-1, 0), (0, 1)])  # we can't place in next to ships
    ships_with_boundaries = ships.union(ship_boundaries)  # add together ships and their boundaries
    available_guesses = board_set.difference(
        ships_with_boundaries)  # find set difference between board and ships+boundaries placed
    #print(available_guesses)  # These are the available places to put a ship
    return available_guesses


def get_available_attempts(player, board):
    board2 = set((i, j) for i in range(10) for j in range(10))  # generate a 10*10 board
    # my_attempts = player.attempts
    if board.attempts[player.value]:
        my_attempts = board.attempts[player.value]
        guesses = set(my_attempts)
    else:
        guesses = set()
    my_ships = board.all_ships[player.value]
    ships = set(my_ships[i][j] for i in range(len(my_ships)) for j in range(len(my_ships[i])))
    ships_guesses_crashes = guesses.union(ships).union(board.crashes)
    #available_attempts = player.attempts.difference(
    available_attempts = board2.difference(
        ships_guesses_crashes)  # find set difference between board and attempts+ships+crashes
    return available_attempts


def update_ships_last_hit(player, board):
    player_hit_bool = board.hits[player.value]
    player_attempts = board.attempts[player.value]
    player_other_ships = board.ships_other_player[player.value]
    if player_hit_bool[-1]:  # if last attempt was a hit
        for ship in player_other_ships:
            if player_attempts[-1] in [get_boundaries(ship_value, dir) for ship_value in ship for dir in
                                       [(1, 0), (0, -1), (-1, 0), (0, 1)]]:
                ship.append(player_attempts[-1])
                board.ships_other_player[player.value] = player_other_ships
                return board
        if player_other_ships == board.ships_other_player[player.value]:
            player_other_ships.append([player_attempts[-1]])
            board.ships_other_player[player.value] = player_other_ships
            return board
    else:
        return board
