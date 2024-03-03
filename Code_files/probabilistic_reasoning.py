import sys
import pygame
import xlsxwriter
from pygame.locals import *
from model import *
from random_ai import *
from model import *
from heuristic_methods import *
from random import shuffle
from itertools import compress,groupby
import random
from boardstate import *
from init_probability_boards import fig_1, fig_2, fig_3, fig_4, fig_5, fig_6
from copy import deepcopy
#from view_prob import fill_grid, show_grid, show_ships

def show_grid():
    letters = [" " + x for x in "ABCDEFGHIJ"]
    digits = [x for x in "123456789"]
    spaced_digits = ["  " + d for d in digits]
    numbers_right = digits + ["10"]
    numbers_left = spaced_digits + ["10"]

    for i in range(10):
        draw_text((6 + i, 0), WHITE, letters[i])
        draw_text((6 + i, 11), WHITE, letters[i])
        draw_text((5, i + 1), WHITE, numbers_left[i])
        draw_text((16, i + 1), WHITE, numbers_right[i])

        for j in range(10):
            draw_square((i + 6, j + 1), WHITE, False)


def fill_grid():
    for i in range(10):  # loop over rows
        for j in range(10):  # loop over columns

            loc = (i + 6, j + 1)
            if ship_test:
                ship_heur = [x[0] for x in board.ship_heuristic]
                if (i,j) in ship_heur:
                    idx = ship_heur.index((i,j))
                    score = board.ship_heuristic[idx][2]
                    draw_text((i+6,j+1), WHITE, str(score))

            if prob_test:
               print("board scores",board.scores)
               prob_heur = [x[0] for x in board.scores]
               total_score = sum(x[1] for x in board.scores)
               if (i,j) in prob_heur:
                   idx = prob_heur.index((i, j))
                   score = board.scores[idx][1]

                   draw_text((i + 6, j + 1), WHITE, str(score))

            if attempt_test:
                if board.attempt_heuristic != []:
                    attempt_heur = [x[0] for x in board.attempt_heuristic[0]]
                    #print("attempt heur ",attempt_heur)
                    if (i, j) in attempt_heur:
                        idx = attempt_heur.index((i, j))
                        score = board.attempt_heuristic[0][idx][1]
                        draw_text((i + 6, j + 1), WHITE, str(score))
            #if hit_test is True:
            #    hit_heur = [x[0][0] for x in board.hit_heuristic]
            #    print("hit heur",hit_heur)
            #    if (i,j) in hit_heur:
            #        idx = hit_heur.index((i,j))
            #        score = board.hit_heuristic[0][idx][1]
            #        print("score",score)
            #        draw_text((i+6,j+1), WHITE, str(score))

            if is_crash((i, j), board):
                draw_square(loc, PURPLE, True)
            elif is_outcome_for(True, (i, j), Player.BLUE, board):
                draw_square(loc, BLUE, True)

            elif is_outcome_for(True, (i, j), Player.RED, board):
                draw_square(loc, RED, True)

            miss_for = lambda c: is_outcome_for(False, (i, j), c, board)
            if miss_for(Player.BLUE) and miss_for(Player.RED):
                draw_cross(loc, PURPLE)
            elif miss_for(Player.BLUE):
                draw_cross(loc, BLUE)
            elif miss_for(Player.RED):
                draw_cross(loc, RED)

            if is_intact_piece_for((i, j), Player.BLUE, board):
                draw_square(loc, BLUE, False)
            elif is_intact_piece_for((i, j), Player.RED, board):
                draw_square(loc, RED, False)


def show_ships(player, board):

    for i in range(len(board.lengths_to_lay[player.value])):
        laid = i < len(board.all_ships[player.value])
        col = player_colours[player.value] if laid else WHITE
        if player.value == 0:
            xs = list([0, 1, 2, 3, 4][-board.lengths_to_lay[player.value][i]:])
        else:
            xs = list([17, 18, 19, 20, 21][:board.lengths_to_lay[player.value][i]])

        locs = [(x, i + 1) for x in xs]
        sunk = laid and ship_sunk_for(i, player, board)
        for loc in locs:
            draw_square(loc, col, sunk)

def draw_square(loc, col, filled):
    rect = Rect(loc[0] * WIDTH, loc[1] * WIDTH, WIDTH, WIDTH)
    thickness = 0 if filled else 3
    pygame.draw.rect(screen, col, rect, thickness)


def draw_cross(loc, col):
    ulx, uly = loc[0] * WIDTH, loc[1] * WIDTH
    pygame.draw.line(screen, col, (ulx, uly), (ulx + WIDTH, uly + WIDTH), 3)
    pygame.draw.line(screen, col, (ulx, uly + WIDTH), (ulx + WIDTH, uly), 3)


def draw_text(loc, col, text):
    myfont = pygame.font.Font(None, WIDTH)
    screen.blit(myfont.render(text, True, col), (loc[0] * WIDTH, loc[1] * WIDTH))

WIDTH = 50
LEFT_EDGEX = 300
RIGHT_EDGEX = 800
BOTTOM_EDGEY = 550
WIN_HEIGHT = WIDTH * 12
WIN_WIDTH = WIDTH * (5 + 12 + 5)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 200, 255)
PURPLE = (200, 100, 200)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)


class Mode(Enum):
    PLACE_START = 0,
    PLACE_END = 1,
    ATTEMPT = 2,
    HANDOVER = 3

#counter = probablistic_attempt(Player.RED, 5, 4, board, count, ship_count)

selected = None
player_colours = [BLUE, RED]
pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT));
pygame.display.set_caption("Gunboats")

turn = Player.BLUE
blue_type = Player_Type.HEURISTIC
red_type = Player_Type.RANDOM
# player_type defined this way, so you can select player_type[turn.value] as blue will be 0
# and red will be 1
player_type = [blue_type, red_type]
mode = Mode.PLACE_START
Heuristic_mode = heuristic_mode.GUESSING_MODE
win = 0
draw = 0
i = 0
time = 1
ship_test = False #for testing only, set to False to play normally
hit_test = False
attempt_test = False
prob_test = True


"""  -------------------------DONT GO ABOVE THIS !!!!!--------------------------------------------------------     """
board = fig_1()


def ship_containing():
    pass

def ship_orientation_with_hit():
    pass

def valid_ships_for_opponent_prob(loc, len, player, board):
    return [ship for ship in ships_from(loc, len) if is_valid_ship_for_opponent_prob(ship, player, board)]



def is_valid_attempt_for_prob(attempt, player, board):
    #print(pieces_of(player,board))
    #print(attempt)
    #print("is attempt in ship",attempt in pieces_of(player,board))
    hits = list(zip(board.attempts[player.value],board.hits[player.value]))
    actual_hits = []
    for counter,attempt2 in enumerate(hits):
        if attempt2[1] is True:
            actual_hits.append(attempt2[0])
        else:
            if counter >= 2:
                actual_hits.append(attempt2[0])
    return attempt not in actual_hits and \
           attempt not in board.crashes and \
           attempt not in pieces_of(player, board)

def is_valid_ship_for_opponent_prob(locs,player,board):
    in_grid = lambda xy: 0 <= xy[0] and 0 <= xy[1] and xy[0] < 10 and xy[1] < 10
    return all([in_grid(loc) and is_valid_attempt_for_prob(loc,player,board) for loc in locs])


board = Boardstate()
def get_available_attempts_for_prob(player, board_attemp):
    board2 = set((i, j) for i in range(10) for j in range(10))  # generate a 10*10 board

    if board_attemp.attempts[player.value]:
        my_hits = []
        my_attempts = board_attemp.attempts[player.value]

        i=0
        while i < len(my_attempts):
            if board_attemp.hits[player.value][i] is True:
                my_hits.append(my_attempts[i])
                i = i + 1
            else:
                i = i + 1
        guesses = set(my_hits)
    else:
        guesses = set()
    my_ships = board_attemp.all_ships[player.value]
    print("board_attempts.all_ships[player.value] ", board_attemp.all_ships[player.value])   #THIS IS THE ISSUE, somehow it stores each ship everytime

    ships = set(my_ships[i][j] for i in range(len(my_ships)) for j in range(len(my_ships[i])))
    ships_guesses_crashes = guesses.union(ships).union(board_attemp.crashes)

    available_attempts = board2.difference(
        ships_guesses_crashes)  # find set difference between board and attempts+ships+crashes
    print("ships_guesses_crashes", len(ships_guesses_crashes), " available_attempts ", len(available_attempts))
    return available_attempts

def ships_on_board(player, board_ship, length):
    print("board_ship.all_ships[player.value] ", board_ship.all_ships[player.value])
    board_attempts = list(get_available_attempts_for_prob(player, board_ship)) #misses don't necessarily stay as misses
    print("board attempts",board_attempts)
    #remove attempts that can't be valid for this length ship
    hits = list(zip(board_ship.attempts[player.value], board_ship.hits[player.value]))
    print("hits", len(hits))
    i = 0
    while i < len(hits) and i < 5:  # loop through first five hits and find the misses
        print("hits[i]",hits[i])
        if hits[i][1] is False:
            if board_ship.lengths_to_lay[player.value][i] < length and hits[i][1] in board_attempts:
                board_attempts = board_attempts.remove(hits[i][0])
        i = i + 1
#i lay attempt at (5,4) on turn 0 --> not a hit (length 5)
#Now considering next attempt
#5 > 4, so remove from consideration length 4 ships to be in this space (opposite of what I need to do)
#if the turn that i made an attempt, the ship length that the opponent laid
    all_possible_ships = []
    for cell in board_attempts:
        ships_from_cell = valid_ships_for_opponent_prob(cell, length, player, board_ship)
        if ships_from_cell != []:
            all_possible_ships.append((cell,ships_from_cell))
    #print("board_ship.all_ships[player.value] ", board_ship.all_ships[0])
    return all_possible_ships

def neighbouring_hits(player, board):
    hits = list(zip(board.attempts[player.value],board.hits[player.value]))
    actual_hits = []
    for attempt in hits:
        if attempt[1] is True:
            actual_hits.append(attempt[0])

    ship_hits = [] #list of ships (i.e. list of lists)
    for hit in actual_hits:
        hit_boundary = [get_boundaries(hit, dir) for dir in
                      [(1, 0), (0, -1), (-1, 0), (0, 1)]]  # [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]

        for boundary in hit_boundary:
            #print("boundary",boundary)
            if boundary in actual_hits and boundary in flatten(ship_hits):
                for count,ship in enumerate(ship_hits):
                    if boundary in ship:
                        ship_hits[count].append(hit)
        if hit not in flatten(ship_hits):
           ship_hits.append([hit])
    return ship_hits

def get_boundaries_x(loc: list, dir: tuple,x) -> tuple:
    return (loc[0] + x * dir[0], loc[1] + x * dir[1])

def valid_ships_containing(ship_squares,player,board,length):
    #we start with [[(2,6),(2,5)]]
    #where to go now?
    if len(ship_squares[0]) == 1:
        hit_dir = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        lengths = list(range(length))
        #print("lengths",lengths)
        locs = [get_boundaries_x(ship_square,hit_direction, len_needed) for ship_square in ship_squares[0] for hit_direction in hit_dir for len_needed in lengths]
        #print("locs",locs)
        #valid_ships = [valid_ships_from(loc, length, player, board) for loc in locs]

    else:
        #print("ship squares",ship_squares)
        hit_dir = [(ship_squares[0][1][0] - ship_squares[0][0][0],ship_squares[0][1][1]-ship_squares[0][0][1]),(ship_squares[0][0][0] - ship_squares[0][1][0],ship_squares[0][0][1]-ship_squares[0][1][1])]
        #print("hit dir",hit_dir)
        lengths = list(range(length))
        locs = [get_boundaries_x(ship_square,hit_direction, len_needed) for ship_square in ship_squares[0] for hit_direction in hit_dir for len_needed in lengths]
    new_board1 = deepcopy(board)
    for square in ship_squares[0]:
        idx = new_board1.attempts[player.value].index(square)
        new_board1.attempts[player.value].remove(square)
        del new_board1.hits[player.value][idx]
    valid_ships = [valid_ships_for_opponent_prob(loc,length,player,new_board1) for loc in locs]
    all_valid_ships = []
    #print("valid ships", valid_ships)
    for i,ship in enumerate(valid_ships):
        if len(ship) != 1:
            for j,element in enumerate(ship):

                #print("flat ship squares",flatten(ship_squares))
                #print("ship",ship)
                #print("element",element)
                if all(item in element for item in flatten(ship_squares)):
                    #print("to add",valid_ships[i][j])
                    all_valid_ships.append(element)
        else:
            #print("flat ship squares", flatten(ship_squares))
            #print("ship", ship)
            if all(item in ship for item in flatten(ship_squares)):
                all_valid_ships.append(ship)
    all_valid_ships.sort()
    return list(all_valid_ships for all_valid_ships,_ in itertools.groupby(all_valid_ships)) #no duplicates

def ship_from(loc, len, dir):
    return [(loc[0] + dir[0] * i, loc[1] + dir[1] * i) for i in range(len)]

def ships_from(loc, len):
    return [ship_from(loc, len, dir) for dir in [(1, 0), (0, -1), (-1, 0), (0, 1)]]


def probablistic_attempt(player, len_needed1, len_needed2, board, counter, ship_counter, need_orientation, ship_passed):
    max_attempts = max([len(attempt) for attempt in board.attempts])
    max_attempts = 5 if max_attempts > 5 else max_attempts
    length_ships = board.lengths_to_lay[player.value][max_attempts-1]
    ships = ships_on_board(player, board, len_needed1)
    #print("ships",ships)
    neighbour_hits = neighbouring_hits(player,board) #groups ships into island

    valid_orientations = valid_ships_containing(neighbour_hits,player,board,len_needed1)
    # Ship length 5 in valid orientations, with all possible 4 ship places
    # Ship length 5 in all possible places, with all orientations of  4 ship

    #Ship length 5 all possible places including valid orientations
    #If need orientation passed as True (ship length 5 not using ship orientation), then calculating ship orientation in 4
    #If need orientation passed as False (ship length 5 using ship orientation), then calculating all other ship places in 4

    insert_orientations = True
    for ship_list in ships:  #ships is ((cell),[[ship1],[ship2]])
        if need_orientation is True:
            for x in valid_orientations:
                ship_list[1].append(x)
            #insert_orientations = False
        for ship in ship_list[1]:  #ships is ((cell),[[ship1],[ship2]])
            #                                      #loop through the actual ships from a cell
            #print("ship list",ship_list[1])
            #print("ship", ship)  # loop through the actual ships from a cell
            #print("valid orientations",valid_orientations)
            #if ship in valid_orientations and len_needed1 == 5:

            print("counter", counter)
            if need_orientation is True and len_needed1 == 4 and ship not in valid_orientations:
                #print("skipping")
                continue

            if need_orientation is False and len_needed1 == 4 and ship in valid_orientations:
                continue

            #print("ship in valid orientations 1",ship in valid_orientations,"len needed",len_needed1)
            #counter += 1

            if ship_passed is not None:
                print("adding extra scores")

                for element in ship_passed:
                    board_score_cells = [x[0] for x in score_board.scores]
                    hits = list(zip(board.attempts[player.value], board.hits[player.value]))
                    actual_hits3 = []
                    for hit3 in hits:
                        if hit3[1]:
                            actual_hits3.append(hit3[0])
                    if element in board_score_cells and element not in actual_hits3:
                        indx = board_score_cells.index(element)
                        score_board.scores[indx][1] = score_board.scores[indx][1] + 1  # increment score by 1
                    else:
                        if element not in actual_hits3:
                            score_board.scores.append([element, 1])  # append item with score of 1

            for item in ship: #loop through each element of ship
                board_score_cells = [x[0] for x in score_board.scores]
                hits = list(zip(board.attempts[player.value],board.hits[player.value]))
                actual_hits2 = []
                for hit2 in hits:
                    if hit2[1]:
                        actual_hits2.append(hit2[0])
                if item in board_score_cells and item not in actual_hits2:
                    indx = board_score_cells.index(item)
                    score_board.scores[indx][1] = score_board.scores[indx][1] + 1          #increment score by 1
                else:
                    if item not in actual_hits2:
                        score_board.scores.append([item, 1])                             #append item with score of 1

            counter += 1

            new_board = deepcopy(board)
            new_board = add_ship(ship, player, new_board)  # add this ship to the board

            if len_needed2 == 0:
                pass

            else:
                if ship in valid_orientations:
                    # print("ship in valid orientations 2", ship in valid_orientations)
                    counter = probablistic_attempt(player, 4, 0, new_board, counter, ship_counter, False, ship)
                else:
                    counter = probablistic_attempt(player, 4, 0, new_board, counter, ship_counter, True, ship)


    return counter

board = fig_6()

score_board = Boardstate()
print("board", board)
count = 0
ship_count = 0

counter = probablistic_attempt(Player.RED, 5, 4, board, count, ship_count, True, None)
board.scores = score_board.scores
#ships = ships_on_board(Player.RED, board,4)
#print("ships",ships)

#valid_ships_50 = valid_ships_for_opponent_prob((5,0), 4, Player.RED, board)
#print("valid ships (5,0)", valid_ships_50)
#ships = neighbouring_hits(Player.RED,board)


#valid_ships = valid_ships_containing(ships,Player.RED,board,4)



print(len(board.scores), " scores", board.scores)
total_score = sum([x[1] for x in board.scores])
print("total score",  total_score)


prob_board = [x[1]/total_score for x in board.scores]
i = 0
for x in board.scores:
    board.scores[i][1] = round((100* x[1])/counter,1)
    i += 1
print(len(board.scores), " scores", board.scores)

print("is it 1 :S: ", sum(prob_board))

while True:
    screen.fill(BLACK)
    show_grid()
    fill_grid()
    show_ships(Player.BLUE, board)
    show_ships(Player.RED, board)
    pygame.display.update()
