import csv

BOARD_ROWS = 0          # need to read this in when reading in the file
BOARD_COLS = 0          # need to read this in when reading in the file
WIN_STATE = (0, 3)      # maybe this is an array of just positive non-zero values?
# LOSE_STATE = (1, 3)     # do we need this
START = (2, 0)          # choose this randomly (has to be non-terminal start state)



if __name__ == "__main__":

    with open('boards/board0.txt', newline = '') as line:
        columnCount = 0
        line_reader = csv.reader(line, delimiter='\t')

        for line in line_reader:
            BOARD_ROWS = BOARD_ROWS + 1                     # num of lines in line_reader is the number of rows
            curLine = ', '.join(line)
            BOARD_COLS = sum(c.isdigit() for c in curLine)  # num of digits in curLine is the number of columns

            print(', '.join(line))

    print()
    print("BOARD_ROWS: " + BOARD_ROWS.__str__())
    print("BOARD_COLS: " + BOARD_COLS.__str__())

