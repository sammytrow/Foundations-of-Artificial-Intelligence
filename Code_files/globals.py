
def initialize_values():
    global crashes, lengths_to_lay, blue_ships, red_ships
    global blue_hits_considered, red_hits_considered, all_ships
    global blue_attempts, red_attempts, attempts, blue_hits, red_hits
    global hits, red_ships_blue_player, blue_ships_red_player
    global cannot_lay_red, cannot_lay_blue,board
    crashes = []
    board = [['-' for i in range(10)] for j in range(10)]
    lengths_to_lay = [5, 4, 3, 2, 2]
    blue_ships = []
    red_ships = []
    blue_hits_considered = []
    red_hits_considered = []
    all_ships = [blue_ships, red_ships]

    blue_attempts = []
    red_attempts = []
    attempts = [blue_attempts, red_attempts]

    red_ships_blue_player = []
    blue_ships_red_player = []

    cannot_lay_blue = []
    cannot_lay_red = []