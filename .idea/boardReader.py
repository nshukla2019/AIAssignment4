import csv

def _readFile(boardPath):

    with open(boardPath, newline = '') as line:
        numOfRows = 0
        numOfColumns = 0

        line_reader = csv.reader(line, delimiter='\t')

        for line in line_reader:
            numOfRows = numOfRows + 1                     # num of lines in line_reader is the number of rows
            curLine = ', '.join(line)
            numOfColumns = sum(c.isdigit() for c in curLine)  # num of digits in curLine is the number of columns

            print(', '.join(line))
        return [numOfRows, numOfColumns]

# def _getWinAndLoseStates(boardPath):
#
#     with open(boardPath, newline = '') as line:
#         continue_again = False
#         winStates = []
#         rowCount = 0;
#
#         line_reader = csv.reader(line, delimiter='\t')
#         rowCount = rowCount + 1
#
#         for line in line_reader:
#            curLine = ', '.join(line)
#            for num in curLine:
#                if (num == '-'):
#                    continue_again = True
#                if (num.isdigit()):
#                    if (continue_again == True):
#                        continue
#                    intNum = int(num)
#                    if (intNum > 0):
#                        winStates.append((rowCount, intNum))
#
#         return winStates