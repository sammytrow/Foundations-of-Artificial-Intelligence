from model import *
from random_ai import *
from model import *
from heuristic_methods import *
from random import shuffle
from itertools import compress
import random
from boardstate import *

def fig_1():
    board = Boardstate()
    #Blue turn 1
    add_ship([(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)], Player.BLUE, board)
    do_attempt((7, 3), Player.BLUE, board)

    #Red turn 1
    add_ship([(1, 1), (2, 1), (3, 1), (4, 1), (5, 1)], Player.RED, board)

    return board


def fig_2():
    board = fig_1()
    #Blue turn 2
    do_attempt((2, 4), Player.RED, board)
    add_ship([(2, 3), (2, 4), (2, 5), (2, 6)], Player.BLUE, board)
    do_attempt((2, 1), Player.BLUE, board)

    #Red turn 2
    add_ship([(8, 0), (8, 1), (8, 2), (8, 3)], Player.RED, board)
    #do_attempt((2, 6), Player.RED, board)
    return board

def fig_3():
    board = fig_2()
    #Blue turn 2
    do_attempt((2, 6), Player.RED, board)
    #do_attempt((2, 5), Player.RED, board)   #temp
    add_ship([(9, 7), (9, 8), (9, 9)], Player.BLUE, board)
    do_attempt((1, 1), Player.BLUE, board)

    #Red turn 2
    add_ship([(7, 7), (8, 7), (9, 7)], Player.RED, board)
    return board

def fig_4():
    board = fig_3()
    #Blue turn 2
    do_attempt((3, 6), Player.RED, board)
    add_ship([(0, 8), (0, 9)], Player.BLUE, board)
    do_attempt((3, 1), Player.BLUE, board)

    #Red turn 2
    add_ship([(5, 4), (5, 5)], Player.RED, board)
    return board

def fig_5():
    board = fig_4()
    #Blue turn 2
    do_attempt((2, 7), Player.RED, board)
    add_ship([(3, 9), (4, 9)], Player.BLUE, board)
    do_attempt((4, 1), Player.BLUE, board)

    #Red turn 2
    add_ship([(4, 7), (5, 7)], Player.RED, board)
    return board

def fig_6():
    board = fig_5()
    #Blue turn 2
    do_attempt((2, 5), Player.RED, board)
    return board