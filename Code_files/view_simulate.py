import pygame
import sys
from enum import Enum
from pygame.locals import *
import model
from agents import *
import globals
import xlsxwriter

globals.initialize_values()
save_datafile = xlsxwriter.Workbook('comp7018_heuristic_vs_rando.xlsx')
worksheet = save_datafile.add_worksheet()
worksheet.write('A1', 'Round')
worksheet.write('B1', 'Winner')
worksheet.write('C1', 'attempts still available')
worksheet.write('D1', 'surviving hits')


def convert_click_if_in_grid(xy):
    x = xy[0] // WIDTH
    y = xy[1] // WIDTH
    if 6 <= x <= 15 and 1 <= y <= 10:
        return x - 6, y - 1
    else:
        return None


def click_in_zone(xy, player):
    return (player == blue_player and xy[0] < 5 * WIDTH) or \
           (player == red_player and 18 * WIDTH < xy[0])


def record_data(round, winner, turns, shipsleft, bychance):
    worksheet.write('A' + str(round + 1), str(round))
    worksheet.write('B' + str(round + 1), str(winner))
    worksheet.write('C' + str(round + 1), str(turns))
    worksheet.write('D' + str(round + 1), str(shipsleft))
    worksheet.write('E' + str(round + 1), str(bychance))


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


selected = None
player_colours = [BLUE, RED]

turn = Player.BLUE
blue_type = Player_Type.RANDOM
red_type = Player_Type.HEURISTIC
# player_type defined this way, so you can select player_type[turn.value] as blue will be 0
# and red will be 1
player_type = [blue_type, red_type]

mode = Mode.PLACE_START
Heuristic_mode = heuristic_mode.GUESSING_MODE
win = 0
draw = 0
i = 0
print(board.all_ships)
while True:

    if player_type[turn.value] != Player_Type.HUMAN:
        if mode != Mode.HANDOVER:
            loc = get_next_move(mode.value, player_type[turn.value], turn, selected, Heuristic_mode.value)

        if loc is not None:
            if mode == Mode.PLACE_START:
                selected = loc
                loc = None
                mode = Mode.PLACE_END
            elif mode == Mode.PLACE_END:
                add_ship_for_if_valid(selected, loc, turn)  # lay ship with start (selected) and loc (end)
                selected = None
                loc = None
                mode = Mode.ATTEMPT
            elif mode == Mode.ATTEMPT:
                if (is_valid_attempt_for(loc, turn)):  # if it's a valid attempt
                    do_attempt(loc, turn)  # do the attempt
                    board = update_ships_last_hit(turn,board)  # update the other ship representation
                    loc = None
                    mode = Mode.HANDOVER

            if mode == Mode.HANDOVER:
                turn = (other_player(turn))
                mode = Mode.ATTEMPT if has_finished_laying(turn) else Mode.PLACE_START

    if all_ship_sunk_for(other_player(turn)):
        if cant_win(other_player(turn)):
            i += 1
            record_data(i, turn, get_available_attempts(turn, board), all_ship_sunk_for(turn), 1)
            win = 1
        else:
            print(turn, "won!")
            i += 1
            record_data(i, turn, get_available_attempts(turn, board), all_ship_sunk_for(turn), 0)
            win = 1
    elif not get_available_attempts(turn, board) and not get_available_attempts(other_player(turn), board):
        i += 1
        record_data(i, 'draw', get_available_attempts(turn, board), all_ship_sunk_for(turn), 0)
        draw = 1

    elif not get_available_attempts(turn, board):
        turn = other_player(turn)
        mode = Mode.ATTEMPT if has_finished_laying(turn) else Mode.PLACE_START;

    if i == 100:
        print("games complete:" + str(i))
        save_datafile.close()
        quit()

    if win != 1:

        try:
            selected
        except NameError:
            selected = None
        try:
            loc  # if location is undefined, set to None.
        except NameError:
            loc = None
        if loc != None:
            if mode == Mode.PLACE_START:
                if (not is_near_pieces_of(loc, turn)):  # ships can't be laid adjacent to each other
                    selected = loc  # this will be laid in next mode
                    loc = None
                    mode = Mode.PLACE_END
            elif mode == Mode.PLACE_END:
                add_ship_for_if_valid(selected, loc, turn)  # lay ship with start (selected) and loc (end)
                selected = None
                loc = None
                print("ships=", board.all_ships[turn.value])
                mode = Mode.ATTEMPT  # after laying, set mode to ATTEMPT
            elif mode == Mode.ATTEMPT:
                print("attempts=", board.attempts[turn.value])
                print("valid attempt=", is_valid_attempt_for(loc, turn))
                if is_valid_attempt_for(loc, turn):  # if it's a valid attempt
                    do_attempt(loc, turn)  # do the attempt
                    board = update_ships_last_hit(turn,board)  # update the other ship representation
                    loc = None
                    mode = Mode.HANDOVER  # Then move to handover step
                    print("attempts=", board.attempts[turn.value])
            else:  # mode == Mode.HANDOVER
                pass
        else:
            if mode == Mode.HANDOVER:
                for player in [blue_player, red_player]:
                    if turn == player and player_type[turn.value] != Player_Type.HUMAN \
                            and mode == Mode.HANDOVER:
                        print("player_type", player_type[turn.value])
                        print("mode is", mode)
                        xy = [901, 0] if player.value == 0 else [89, 0]
                        print("xy=", xy)
                    # if you click in the other players zone
                    if turn == player and click_in_zone(xy, other_player(player)):
                        # change turn to other player
                        turn = other_player(player)
                        print("turn=", turn)
                        # if there are still things to lay, then attempt for other player
                        # otherwise, the mode is to start laying
                        mode = Mode.ATTEMPT if has_finished_laying(turn) else Mode.PLACE_START;

    if win == 1 or draw == 1:
        reinitialise_board()
        win = 0
        draw = 0
