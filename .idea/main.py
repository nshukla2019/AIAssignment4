import boardReader

PROBABILITY_TO_DESIRED_DIRECTION = 0.8   # read this value in from command line
PROBABILITY_TO_ANY_OTHER_DIRECTION = round(((1.0 - PROBABILITY_TO_DESIRED_DIRECTION)/2), 1)
WIN_STATE = (-1, -1)                      # maybe this is an array of just positive non-zero values since there could be multiple
START = (-1, -1)                          # choose this randomly (has to be non-terminal start state)
# LOSE_STATE = (1, 3)                     # do we need this
BOARD_ROWS = 0
BOARD_COLS = 0

if __name__ == "__main__":

    board_info = boardReader._readFile('boards/board0.txt')
    BOARD_ROWS = board_info[0]
    BOARD_COLS = board_info[1]

    #WIN_STATE = boardReader._getWinAndLoseStates('boards/board0.txt')
    print()
    print("BOARD_ROWS: " + BOARD_ROWS.__str__())
    print("BOARD_COLS: " + BOARD_COLS.__str__())
    print("PROB TO DESIRED: " + PROBABILITY_TO_DESIRED_DIRECTION.__str__())
    print("PROB TO ANY OTHER DIRECTION: " + PROBABILITY_TO_ANY_OTHER_DIRECTION.__str__())
    print("WI_STATES: " + WIN_STATE.__str__())


