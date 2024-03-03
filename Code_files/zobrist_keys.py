import random
zobTable = [[[random.randint(1,2**64 - 1) for i in range(12)]for j in range(8)]for k in range(8)]

def indexing(square):
    if square == 'A': #blue attempt
        return 0
    if square == 'As': #blue attempt then red ship
        return 1
    if square == 'C': #crash
        return 2
    if square == 'Sa': #blue ship then red attempt:
        return 3
    if square == 'S': #blue ship
        return 4
    if square == 'a': # red attempt
        return 5
    if square == 'aS': #red attempt then blue ship
        return 6
    if square == 'sA': #red ship then blue attempt:
        return 7
    if square == 's': #blue ship
        return 8
    if square == 'aA' or square == 'Aa': #blue and red attempt:
        return 9
    else:
        return -1

def computeHash(board):
    h = 0
    for i in range(10):
        for j in range(10):
            if board[i][j] != '-':
                square = indexing(board[i][j])
                h ^= zobTable[i][j][square]
    return h

