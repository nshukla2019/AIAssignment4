class State:
    def __init__(self, state=START):
        self.board = np.zeros([BOARD_ROWS, BOARD_COLS])
        #self.board[1, 1] = -1  #can use this for obstacles if assignment has any
        self.state = state
        self.isEnd = False