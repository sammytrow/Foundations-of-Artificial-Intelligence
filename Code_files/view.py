import sys

import pygame
import xlsxwriter
from pygame.locals import *

import globals
from agents import *
from boardstate import Boardstate
from time import sleep

#globals.initialize_values()

save_datafile = xlsxwriter.Workbook('comp7018_heuristic_vs_rando.xlsx')
worksheet = save_datafile.add_worksheet()
worksheet.write('A1', 'Round')
worksheet.write('B1', 'Winner')
worksheet.write('C1', 'attempts still available')
worksheet.write('D1', 'enemy attempts still available')
worksheet.write('E1', 'surviving boats')
worksheet.write('F1', 'enemy surviving boats')


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
               prob_heur = [x[0] for x in board.scores]
               if (i,j) in prob_heur:
                   idx = prob_heur.index((i, j))
                   score = board.prob_heur[idx][1]
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


def show_turn():
    ulx = 0 if turn == Player.BLUE else 17 * WIDTH
    rect = Rect(ulx, 0, WIDTH * 5, WIDTH * 12)
    pygame.draw.rect(screen, player_colours[turn.value], rect, 5)


def show_selection():
    if selected != None:
        draw_square((selected[0] + 6, selected[1] + 1), YELLOW, False)


def convert_click_if_in_grid(xy):
    x = xy[0] // WIDTH
    y = xy[1] // WIDTH
    if 6 <= x and x <= 15 and 1 <= y and y <= 10:
        return (x - 6, y - 1)
    else:
        return None


def click_in_zone(xy, player):
    return (player == Player.BLUE and xy[0] < 5 * WIDTH) or \
           (player == Player.RED and 18 * WIDTH < xy[0])


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


def record_data(round, winner, player, turns, enemy_turns, chance):
    counter = 0
    counter2 = 0
    if winner != 'draw':
        for j in range(len(board.lengths_to_lay[0])):
            temp = ship_sunk_for(j, player, board)
            temp2 = ship_sunk_for(j, other_player(player), board)
            if not temp:
                counter += 1
            if not temp2:
                counter2 += 1
    worksheet.write('A' + str(round + 1), str(round))
    worksheet.write('B' + str(round + 1), str(winner))
    worksheet.write('C' + str(round + 1), str(turns))
    worksheet.write('D' + str(round + 1), str(enemy_turns))
    worksheet.write('E' + str(round + 1), str(counter))
    worksheet.write('F' + str(round + 1), str(counter2))
    worksheet.write('G' + str(round + 1), str(chance))


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



board = Boardstate()

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
prob_test = False

while True:

    if win == 1 or draw == 1:
        board = Boardstate()
        turn = Player.BLUE #Need to ensure Player BLUE starts!
        win = 0
        draw = 0


    if player_type[turn.value] != Player_Type.HUMAN:
        if mode != Mode.HANDOVER:
            board = update_last_hit(other_player(turn),board) #workaround for bug
            loc = get_next_move(mode.value, player_type[turn.value], turn, selected, Heuristic_mode.value, board)


        try:
            selected
        except NameError:
            selected = None
        try:
            loc  # if location is undefined, set to None.
        except NameError:
            loc = None

        if loc is not None:
            if mode == Mode.PLACE_START:
                selected = loc
                loc = None
                mode = Mode.PLACE_END

            elif mode == Mode.PLACE_END:
                board = add_ship_for_if_valid(selected, loc, turn,
                                              board)  # lay ship with start (selected) and loc (end)
                #print("ship placed at", selected, loc)
                selected = None
                loc = None
                mode = Mode.ATTEMPT

            elif mode == Mode.ATTEMPT:
                if is_valid_attempt_for(loc, turn, board):  # if it's a valid attempt

                    board = do_attempt(loc, turn, board)  # do the attempt
                    board = update_ships_last_hit(turn, board)  # update the other ship representation
                    loc = None
                    mode = Mode.HANDOVER

        if mode == Mode.HANDOVER:
            if ship_test is False and hit_test is False and attempt_test is False and prob_test is False:
                turn = other_player(turn)
                mode = Mode.ATTEMPT if has_finished_laying(turn, board) else Mode.PLACE_START
                #sleep(0.5)
                time = time + 1
            else:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        turn = other_player(turn)
                        mode = Mode.ATTEMPT if has_finished_laying(turn, board) else Mode.PLACE_START
                        #sleep(0.5)
                        time = time + 1

    if len(board.attempts[turn.value]) == 6:
        if cant_win(turn, board) and cant_win(other_player(turn), board):
            i += 1
            record_data(i, 'draw', get_available_attempts(turn, board), all_ship_sunk_for(turn, board), 0, 0)
            draw = 1

        elif cant_win(turn, board):
            i += 1
            record_data(i, other_player(turn), turn, len(get_available_attempts(turn, board)),
                        len(get_available_attempts(other_player(turn), board)), 1)
            win = 1


        elif cant_win(other_player(turn), board):
            i += 1
            record_data(i, turn, turn, len(get_available_attempts(turn, board)),
                        len(get_available_attempts(other_player(turn), board)), 1)
            win = 1

    if all_ship_sunk_for(other_player(turn), board):
        if cant_win(other_player(turn), board):
            i += 1
            record_data(i, turn, turn, len(get_available_attempts(turn, board)),
                        len(get_available_attempts(other_player(turn), board)), 1)
            win = 1
        else:
            print(turn, "won!")
            i += 1
            record_data(i, turn, turn, len(get_available_attempts(turn, board)),
                        len(get_available_attempts(other_player(turn), board)), 0)
            win = 1
    elif not get_available_attempts(turn, board) and not get_available_attempts(other_player(turn), board):
        i += 1
        print("no available attempts left, bug!!")
        record_data(i, 'draw', get_available_attempts(turn, board), all_ship_sunk_for(turn, board), 0, 0)
        draw = 1

    elif not get_available_attempts(turn, board):
        turn = other_player(turn)
        mode = Mode.ATTEMPT if has_finished_laying(turn,board) else Mode.PLACE_START

    if i == 500:
        print("games complete:" + str(i))
        save_datafile.close()
        quit()

    if win != 1:
        for event in pygame.event.get():
            if player_type[turn.value] == Player_Type.HUMAN:  # if it's a human player, then expect "normal input"
                if event.type == pygame.MOUSEBUTTONDOWN:  # player clicks
                    xy = pygame.mouse.get_pos()  # convert this to an xy position
                    loc = convert_click_if_in_grid(xy)  # convert xy position to (x-6,y-1) if in grid

                try:
                    selected
                except NameError:
                    selected = None
                try:
                    loc  # if location is undefined, set to None.
                except NameError:
                    loc = None

                if loc is not None:
                    if mode == Mode.PLACE_START:
                        if not is_near_pieces_of(loc, turn):  # ships can't be laid adjacent to each other
                            selected = loc  # this will be laid in next mode
                            loc = None
                            mode = Mode.PLACE_END

                    elif mode == Mode.PLACE_END:
                        board = add_ship_for_if_valid(selected, loc, turn,
                                                      board)  # lay ship with start (selected) and loc (end)
                        board = update_board_ship(turn, board)
                        board.update(turn)
                        print("ship placed at",selected,loc)
                        selected = None
                        loc = None
                        mode = Mode.ATTEMPT  # after laying, set mode to ATTEMPT

                    elif mode == Mode.ATTEMPT:
                        if is_valid_attempt_for(loc, turn, board):  # if it's a valid attempt

                            board, turn = do_attempt(loc, turn, board)  # do the attempt
                            board = update_ships_last_hit(turn, board)  # update the other ship representation
                            board = update_board_attempt(turn, board) #update zobrist board representation
                            board.update(turn)
                            print("board hits",board.hits)
                            loc = None
                            mode = Mode.HANDOVER  # Then move to handover step
                    else:  # mode == Mode.HANDOVER
                        pass
                else:
                    if mode == Mode.HANDOVER:
                        for player in [Player.BLUE, Player.RED]:
                            if turn == player and player_type[turn.value] != Player_Type.HUMAN \
                                    and mode == Mode.HANDOVER:
                                xy = [901, 0] if player.value == 0 else [89, 0]
                                board.update(player)
                            # if you click in the other players zone
                            elif turn == player and click_in_zone(xy, other_player(player)):
                                turn = other_player(turn)
                            # if there are still things to lay, then attempt for other player
                            # otherwise, the mode is to start laying
                            mode = Mode.ATTEMPT if has_finished_laying(turn) else Mode.PLACE_START;

        if event.type == QUIT or event.type == KEYUP and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        screen.fill(BLACK)

        show_grid()
        fill_grid()
        show_ships(Player.BLUE, board)
        show_ships(Player.RED, board)


    show_turn()
    show_selection()

    pygame.display.update()
