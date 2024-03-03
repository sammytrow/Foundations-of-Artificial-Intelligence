from boardstate import Boardstate

###########minimax with Iterative deepening###########
class Minimax_ID:

    def __init__(self):
        self.best_move = 0
        self.best_move_loc = 0

    def best_move_IDS(self, bs: Boardstate, max_depth, maximizingPlayer):
        best_move_score=  float('-inf')
        best_move_loc = ()
        best_move = 0
        for depth in range(1,max_depth+1):
                bs.states_min_max = bs.get_minmax_boardstate()
                bs.current_score = bs.get_current_score()
                score = self.minimax(bs, depth, maximizingPlayer)
                print("depth,score",depth,score, "\n")
                if score> best_move_score:
                    best_move_score = score
                    best_move_loc = self.best_move_loc
                    best_move = self.best_move
                    print(self.best_move,self.best_move_loc,"\n")
        return best_move,best_move_loc

    def minimax(self, bs: Boardstate, depth, maximizingPlayer):
        available_moves, move_position = bs.get_available_moves()
        if bs.end_node:
            #print("end node reached, score is",bs.current_score)
            return bs.current_score
        elif not depth:
            #print("depth end node reached, score is", bs.current_score)
            return bs.current_score
        elif maximizingPlayer:
            best_move_score = float('-inf')
            self.best_move = available_moves[0]
            for m in range(len(available_moves)):
                next_level_boardstate = bs.predict_boardstate(available_moves[m], move_position[m],True)
                score = max(best_move_score, self.minimax(bs, (depth-1), False))
                if (score > best_move_score):
                    best_move_score = score
                    self.best_move = available_moves[m]
                    self.best_move_loc = move_position[m]
                previous_level_boardstate = bs.reverse_boardstate(available_moves[m], move_position[m])
            return best_move_score
        else:
            best_move_score = float('inf')
            self.best_move = available_moves[0]
            for m in range(len(available_moves)):
                next_level_boardstate = bs.predict_boardstate(available_moves[m], move_position[m],False)
                score = min(best_move_score, self.minimax(bs, (depth-1), True))
                if score < best_move_score:
                    best_move_score = score
                    self.best_move = available_moves[m]
                    self.best_move_loc = move_position[m]
                previous_level_boardstate = bs.reverse_boardstate(available_moves[m], move_position[m])
            return best_move_score

def minmax_attempt(player, board):
    #print(board.states_min_max,"\n")
    #print(board.current_score, "\n")
    minmax = Minimax_ID()
    Max_depth = 2
    best_move,best_move_loc = minmax.best_move_IDS(board, Max_depth, True)
    if not best_move:
        print("best move is none")
        return None
    print("MInmax best move loc", best_move_loc, "\n")
    print("MInmax best move", best_move, "\n")
    print("MInmax boardstate", board.states_min_max, "\n")
    return best_move_loc

#################Testing MInimAX#################################
#bs = Boardstate()
#bs.states =[['-', '-', '-', 'Bs', 'Bs', 'Rh', 'Rh', '-', '-', '-'],
#             ['Rh', '-', 'Bm', '-', 'Bh', 'Bh', 'Bh', 'Bh', 'Rs', 'Rh'],
#             ['Rh', '-', '-', '-', 'Bm', 'Rh', '-', '-', '-', 'Rh'],
#             ['Rh', '-', '-', 'Rm', 'Rm', 'Rh', '-', '-', '-', 'Rh'],
#             ['Rh', 'Bh', 'Bh', '-', '-', '-', '-', '-', '-', '-'],
#             ['Rh', '-', '-', '-', 'Rm', '-', '-', '-', '-', '-'],
#             ['-', 'Bh', 'Bh', '-', 'Rm', '-', '-', '-', '-', 'Bh'],
#             ['-', '-', '-', 'Bm', '-', '-', 'Bm', '-', '-', 'Bh'],
#             ['-', '-', '-', 'Bh', 'Bh', 'Bh', 'Bh', '-', '-', 'Bh'],
#             ['Rh', 'Rh', '-', '-', '-', '-', '-', '-', '-', '-']]
#bs.current_score = 1
#minmax = Minimax_ID()
#score= minmax.minimax(bs, 3, True)
#print(score, minmax.best_move, minmax.best_move_loc)