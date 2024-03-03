from enum import Enum
import itertools
import globals

class Player(Enum):
    BLUE = 0
    RED = 1

#class Player:
#    def __init__(self, color):
#        self.ships = []
#        self.value = color
#        self.lengths_to_lay = [5, 4, 3, 2, 2]
#        self.attempts = []
#        self.hits = []
#        self.other_ships = []

class Player_Type(Enum):
    HUMAN = 0
    RANDOM = 1
    HEURISTIC = 2
    MINIMAX = 3


class heuristic_mode(Enum):
    GUESSING_MODE = 0
    HIT_MODE = 1


def reinitialise_board(board):
    board.crashes = []
    board.lengths_to_lay = [[5, 4, 3, 2, 2],[5, 4, 3, 2, 2]]
    board.attempts = []
    board.hits = []
    #globals.blue_hits_considered = []
    #globals.red_hits_considered = []
    board.ships_other_player = [[],[]]
    board.all_ships = [[], []]
    board.states = [['-' for i in range(10)] for j in range(10)]
    return board


def update_board_attempt(player, board):
    attempt = board.attempts[player.value][-1]
    #print("ATTEMPTS",board.attempts[player.value])
    #print("player value",player.value)
    #print("attempt=",attempt)
    #print("Cell state: " + board.states[attempt[0]][attempt[1]])
    if player.value == 0:
        if board.states[attempt[0]][attempt[1]] == '-':
            board.states[attempt[0]][attempt[1]] = 'A'
        else:
            board.states[attempt[0]][attempt[1]] = board.states[attempt[0]][attempt[1]] + 'A'
    else:
        if board.states[attempt[0]][attempt[1]] == '-':
            board.states[attempt[0]][attempt[1]] = 'a'
        else:
            board.states[attempt[0]][attempt[1]] = board.states[attempt[0]][attempt[1]] + 'a'
    return board

def update_board_ship(player, board):
    ship = board.all_ships[player.value][-1]
    if player.value == 0:
        for square in ship:
            if board.states[square[0]][square[1]] == '-':
                print("Cell state: " + board.states[square[0]][square[1]])
                board.states[square[0]][square[1]] = 'S'
            else:
                print("Cell state: " + board.states[square[0]][square[1]])
                board.states[square[0]][square[1]] = board.states[square[0]][square[1]] + 'S'
    else:
        for square in ship:
            if board.states[square[0]][square[1]] == '-':
                print("Cell state: " + board.states[square[0]][square[1]])
                board.states[square[0]][square[1]] = 's'
            else:
                print("Cell state: " + board.states[square[0]][square[1]])
                board.states[square[0]][square[1]] = board.states[square[0]][square[1]] + 's'
    return board


def update_board_crash(board):
    last_crash = board.crashes[-1]
    board.states[last_crash[0]][last_crash[1]] = 'C'
    return board


def cant_win(player, board):
    if has_finished_laying(player,board) and has_finished_laying(other_player(player),board):
        guessed = board.attempts[player.value]
        other_ships = board.all_ships[other_player(player).value]
        i = 0
        while i < len(guessed):
            j = 0
            while j < len(other_ships):
                if player == Player.BLUE: #Blue goes first
                    if guessed[i] in other_ships[j] and i <= j:  # if guess before ship placed, you can't win
                        #need to consider i = j as BLUE player is going first
                        return True
                else: #player is Player.RED
                    if guessed[i] in other_ships[j] and i <= j:  # if guess before ship placed, you can't win
                        return True
                j = j + 1
            i = i + 1
        return False

def update_last_hit(player,board):
    my_attempts = board.attempts[player.value]
    my_hits = board.attempts[player.value]
    enemy_ships = board.all_ships[other_player(player).value]
    if len(my_hits) > 0:
        if my_hits[-1] is False:
            if my_attempts[-1] in flatten(enemy_ships) and my_attempts[-1] not in board.crashes:
                print("it's happening",my_attempts[-1],flatten(enemy_ships))
                board.attempts[player.value][-1] = True
                return board
            return board
        return board
    return board


def other_player(player):
    return Player(1 - player.value)


def is_outcome_for(hit_not_miss, loc, player, board):
    outcomes = list(zip(board.attempts[player.value], board.hits[player.value]))
    crash_true = list(zip(board.crashes, [True] * len(board.crashes)))
    crashes_and_outcomes = list(set(crash_true).union(set(outcomes)))
    return (loc, hit_not_miss) in crashes_and_outcomes

def flatten(x):
    flat = list(itertools.chain.from_iterable(x))
    return flat

def pieces_of(player,board):
    flatten = lambda xss: list(itertools.chain.from_iterable(xss))
    return flatten(board.all_ships[player.value])


def is_intact_piece_for(loc, player, board):
    return loc in pieces_of(player, board) and not is_crash(loc, board) \
              and not is_outcome_for(True, loc, other_player(player), board)



def is_crash(loc, board):
    return loc in board.crashes


def is_near_pieces_of(loc, player, board):
    near = lambda xy, wz: abs(xy[0] - wz[0]) <= 1 and abs(xy[1] - wz[1]) <= 1
    return any([p != None and near(loc, p) for p in pieces_of(player, board)])


def ship_from(loc, len, dir):
    return [(loc[0] + dir[0] * i, loc[1] + dir[1] * i) for i in range(len)]


def ships_from(loc, len):
    return [ship_from(loc, len, dir) for dir in [(1, 0), (0, -1), (-1, 0), (0, 1)]]


def is_valid_ship_from(locs, player, board):
    in_grid = lambda xy: 0 <= xy[0] and 0 <= xy[1] and xy[0] < 10 and xy[1] < 10
    return all([in_grid(loc) and not is_near_pieces_of(loc, player, board) for loc in locs])


def valid_ships_from(loc, len, player, board):
    return [ship for ship in ships_from(loc, len) if is_valid_ship_from(ship, player, board)]


def get_boundaries(loc: list, dir: tuple) -> tuple:
    return (loc[0] + dir[0], loc[1] + dir[1])


def update_ships_crash(player,board):
    player_other_ships = board.ships_other_player[other_player(player).value]
    for ship in player_other_ships:
        if board.crashes[-1] in [get_boundaries(ship_value, dir) for ship_value in ship for dir in
                                   [(1, 0), (0, -1), (-1, 0), (0, 1)]]:
            ship.append(board.crashes[-1])
            board.ships_other_player[other_player(player).value] = player_other_ships
            return board
    if player_other_ships == board.ships_other_player[other_player(player).value]:
        player_other_ships.append([board.crashes[-1]])
        board.ships_other_player[other_player(player).value] = player_other_ships
        return board
    else:
        return board


def add_ship(locs, player, board):
    board.all_ships[player.value].append(locs)

    new_crashes = [loc for loc in locs if loc in pieces_of(other_player(player),board)]
    if new_crashes == []:
        return board
    else:
        for crash in new_crashes:
            board.crashes.append(crash) #update crashes
            board = update_board_crash(board) #update states for zobrist
            board = update_ships_crash(player,board) #updating other ships representation
            board = update_ships_crash(other_player(player),board) # update the crash for the other player
        return board


def add_ship_for_if_valid(start, end, player, board):
    len_needed = length_needed(player,board)
    ends = lambda l: (l[0], l[-1])
    only_ship = [s for s in valid_ships_from(start, len_needed, player, board) \
                 if ends(s) == (start, end)]
    if only_ship:
        #print("valid ship",True)
        board = add_ship(only_ship[0], player, board)
    else:
        print("invalid ship",start, end)
    return board
    


def has_finished_laying(player,board):
    return len(board.all_ships[player.value]) == len(board.lengths_to_lay[player.value])


def is_valid_attempt_for(attempt, player, board):
    return attempt not in board.attempts[player.value] and \
           attempt not in board.crashes and \
           attempt not in pieces_of(player, board)

def not_hit_piece(attempt,player,board):
    pieces = flatten(board.all_ships[player.value])
    crashes = board.crashes
    attempts_other_player = board.attempts[other_player(player).value]
    return attempt in pieces and attempt not in attempts_other_player and pieces not in crashes


def do_attempt(attempt, player, board):
    #print("attempt",attempt)
    #print("ships",board.all_ships)
    board.hits[player.value].append(is_intact_piece_for(attempt, other_player(player), board))
    #print("is_it_a_hit?",is_intact_piece_for(attempt, other_player(player), board))
    #print("is it a hit? new code",not_hit_piece(attempt,other_player(player),board))
    if is_intact_piece_for(attempt, other_player(player), board) != not_hit_piece(attempt,other_player(player),board):
        return True
    board.attempts[player.value].append(attempt)
    return board


def ship_sunk_for(shipi, player, board):
    # return if a particular ship is sunk
    ship = board.all_ships[player.value][shipi]
    return all([is_outcome_for(True, loc, other_player(player), board) for loc in ship])


def all_ship_sunk_for(player, board):
    # all_ship_laid AND all ships sunk
    # return len(player.ships) == len(player.lengths_to_lay) and \
    return len(board.all_ships[player.value]) == len(board.lengths_to_lay[player.value]) and \
           all([ship_sunk_for(i, player, board) for i in range(len(board.lengths_to_lay[player.value]))])

def length_needed(player,board):
    return board.lengths_to_lay[player.value][len(board.all_ships[player.value])]