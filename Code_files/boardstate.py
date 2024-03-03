class Boardstate:

    def __init__(self):
        self.all_ships = [[], []]
        self.states = [['-' for i in range(10)] for j in range(10)]
        self.attempts = [[],[]]
        self.hits = [[], []]
        self.crashes = []
        self.ships_other_player = [[],[]]
        self.lengths_to_lay = [[5,4,3,2,2],[5,4,3,2,2]]
        self.ship_heuristic = []
        self.hit_heuristic = []
        self.attempt_heuristic = []
        self.scores = []

        #for minimax
        self.states_min_max = []
        self.current_score = 0
        self.end_node = 0

    def get_available_moves(self):
        # Blue ship(Bs), Red ship(Rs), Blue hit(Bh), Red hit(Rh) , Blue miss(Bm), Red miss(Rm),
        # Crash(C),Red and Blue miss (RBm)
        self.end_node = 0
        Available_moves =[]
        Move_position = []
        Bs_loc = []
        Rs_loc = []
        Empty_loc = []
        for i in range(10):
            for j in range(10):
                if self.states[i][j] == 'Bs':
                    Bs_loc.append((i, j))
                if self.states[i][j] == 'Rs':
                    Rs_loc.append((i, j))
                if self.states[i][j] == '-':
                    Empty_loc.append((i, j))
        #print("Available blueship cells ", Bs_loc, "\n")
        #print("Available redship cells ", Rs_loc, "\n")
        #print("Available Empty cells ", Empty_loc, "\n")
        if Rs_loc:
            Available_moves.append('Rs')
            Move_position.append(Rs_loc[0])
        if Bs_loc:
            Available_moves.append('Bs')
            Move_position.append(Bs_loc[0])
        if Empty_loc:
            Available_moves.append('-')
            Move_position.append(Empty_loc[0])
        #print("next move",Available_moves, "\n")
        #print("next move position",Move_position, "\n")
        if not Rs_loc or not Bs_loc:
             self.end_node = 1
        return (Available_moves, Move_position)

    def predict_boardstate(self, move, loc, maximizingPlayer):
        # Predict Board states
        if move == 'Bs':
            self.states[loc[0]][loc[1]] = 'Rh'
            self.current_score -= 1
        if move == 'Rs':
            self.states[loc[0]][loc[1]] = 'Bh'
            self.current_score += 1
        if move == '-':
            if maximizingPlayer:
                self.states[loc[0]][loc[1]] = 'Bm'
            else:
                self.states[loc[0]][loc[1]] = 'Rm'
        return self.current_score

    def reverse_boardstate(self, move, loc ):
        print(move, loc, self.states)
        if move == 'Rs':
            self.states[loc[0]][loc[1]] = 'Rs'
            self.current_score -= 1
        elif move == 'Bs':
            self.states[loc[0]][loc[1]] = 'Bs'
            self.current_score += 1
        else:
            self.states[loc[0]][loc[1]] = '-'
        print(move,loc, self.states)
        return self.current_score