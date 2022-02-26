import random
from enum import IntEnum
import csv
import sys
import time

class Move(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class QFunc():
    def __init__(self, map, action_cost = -0.05,moves = [Move.UP,Move.RIGHT,Move.DOWN,Move.LEFT]):
        self.map = map
        self.moves = moves
        self.action_cost = action_cost
        self.epsilon = 0.1
        self.gamma = 1
        self.Q = self.init_Q()

    def init_Q(self):
        Q = []
        for y in range(self.map.size[1]):
            Q.append([])
            for x in range(self.map.size[0]):
                Q[y].append([])
                for m in range(len(self.moves)):
                    Q[y][x].append(0) #will be an initial value
        return Q

    def lookup_Q(self,pos,move):
        return self.Q[pos[1]][pos[0]][int(move)]

    def lookup_best_Q(self,pos):
        return max(self.Q[pos[1]][pos[0]])

    def lookup_moves(self,pos):
        return self.Q[pos[1]][pos[0]]

    def update_Q(self,pos,move,delta):
        self.Q[pos[1]][pos[0]][int(move)] += delta #use update rule

    def make_move(self,cur_pos):
        moves = self.lookup_moves(cur_pos)
        if random.uniform(0,1) <= self.epsilon:
            next_move = random.randint(0,3)
        else:
            next_move = moves.index(max(moves))
        next_pos = self.map.get_move_transition(pos,Move(next_move))
        if not next_pos in self.map.non_terminals:
            terminal_val = float(self.map.map[next_pos[1]][next_pos[0]])
            delta = self.action_cost + self.gamma*(terminal_val - self.lookup_Q(cur_pos,Move(next_move)))
        else:
            value_next_pos = self.lookup_best_Q(next_pos)
            delta = self.action_cost + self.gamma*(value_next_pos - self.lookup_Q(cur_pos,Move(next_move)))
        self.update_Q(cur_pos,Move(next_move),delta)
        return next_pos

    def get_readable_Q(self):
        readable = []
        for y in range(len(self.Q)):
            readable.append([])
            for x in range(len(self.Q[y])):
                readable[y].append([])
                cur_moves = self.Q[y][x]
                best_move = 0
                best_val = cur_moves[0]
                for m in range(len(cur_moves)):
                    if cur_moves[m] > best_val:
                        best_move = m
                        best_val = cur_moves[m]
                # print(self.map.map[y][x])
                # print(self.map.non_terminals)
                if((x,y) not in self.map.non_terminals):
                    readable[y][x] = str(self.map.map[y][x])
                else:
                    if(best_move == 0):
                        readable[y][x] = '^'
                    elif(best_move == 1):
                        readable[y][x] = '>'
                    elif(best_move == 2):
                        readable[y][x] = 'v'
                    elif(best_move == 3):
                        readable[y][x] = '<'
        return readable



class Map():
    def __init__(self, move_weights,size = [5,5],moves = [Move.UP,Move.RIGHT,Move.DOWN,Move.LEFT], map_str = ''):
        self.size = size
        self.moves = moves
        self.max_fill = [5.5,10.0]
        self.min_fill = [-10.0,-5.5]
        self.fill_weights = [95,2.5,2.5]
        self.move_weights = move_weights
        self.non_terminals = []

        if(map_str ==  ''):

            self.map = self.make_map()
        else:
            print('using saved')
            self.map = self.str_to_map(map_str)

    def map_fill(self):
        max_val = round(random.uniform(self.max_fill[0],self.max_fill[1]),2)
        min_val = round(random.uniform(self.min_fill[0],self.min_fill[1]),2)
        choices = [0,max_val,min_val]
        return random.choices(choices,weights = self.fill_weights,k=1)[0]

    def random_pos(self):
        return (random.randint(0,self.size[0]-1),random.randint(0,self.size[1]-1))

    def random_non_terminal(self):
        return random.choices(self.non_terminals,k=1)[0]

    def make_map(self):
        has_terminals = (False,False) # high,low
        map = []
        for y in range(self.size[1]):
            map.append([])
            for x in range(self.size[0]):
                place = self.map_fill();
                if(place == 0):
                    self.non_terminals.append((x,y))
                has_terminals = (has_terminals[0] or place > 0,has_terminals[1] or place < 0)
                map[y].append(place)
        if (not has_terminals[0]) and (not has_terminals[1]):
            terminal_high = self.random_pos()
            terminal_low = self.random_pos()
            while terminal_low == terminal_high:
                terminal_low = self.random_pos()
            self.non_terminals.remove(terminal_high)
            self.non_terminals.remove(terminal_low)
            map[terminal_high[1]][terminal_high[0]] = round(random.uniform(self.max_fill[0],self.max_fill[1]),2)
            map[terminal_low[1]][terminal_low[0]] = round(random.uniform(self.min_fill[0],self.min_fill[1]),2)
        elif not has_terminals[0]:
            terminal_high = self.random_pos()

            map[terminal_high[1]][terminal_high[0]] = round(random.uniform(self.max_fill[0],self.max_fill[1]),2)

            self.non_terminals.remove(terminal_high)
        elif not has_terminals[1]:
            terminal_low = self.random_pos()

            map[terminal_low[1]][terminal_low[0]] = round(random.uniform(self.min_fill[0],self.min_fill[1]),2)
            self.non_terminals.remove(terminal_low)
        return map

    def str_to_map(self,str):
        map = []
        rows = str.split('\n')
        for row in rows:
            cols = row.split(',')
            map.append(cols)

        self.size = (len(map[0]),len(map))
        for y in range(len(map)):
            for x in range(len(map[y])):
                if map[y][x] == '0':
                    self.non_terminals.append((x,y))
        return map


    def map_to_string(self):
        return '\n'.join([','.join([str(x) for x in self.map[y]]) for y in range(self.size[1])])

    def map_to_file(self,filepath):
        file = open(filepath,'w')
        file.write(self.map_to_string())
        file.close()

    def move_deflection(self,move,direction_right):
        if direction_right:
            return Move(min((int(move)+1),len(self.moves)-1))
        else:
            return Move(max((int(move)-1),0))

    def get_move_transition(self,pos,move):
        choices = [0,1,-1]
        deflect = random.choices(choices,weights = self.move_weights,k=1)[0]
        if(deflect == 1):
            move = self.move_deflection(move,True)
        elif(deflect == -1):
            move = self.move_deflection(move,False)
        if(move == move.UP):
            new_y = max(pos[1]-1,0)
            return (pos[0],new_y)
        elif(move == move.RIGHT):
            new_x = min(pos[0]+1,self.size[0]-1)
            return (new_x,pos[1])
        elif(move == move.DOWN):
            new_y = min(pos[1]+1,self.size[1]-1)
            return (pos[0],new_y)
        elif(move == move.LEFT):
            new_x = max(pos[0]-1,0)
            return (new_x,pos[1])




def _readFile(boardPath):

    with open(boardPath, newline = '') as line:
        line_reader = csv.reader(line, delimiter=',')
        str = ''
        lines = []
        for line in line_reader:                  # num of lines in line_reader is the number of rows
            curLine = ','.join(line)
            numOfColumns = sum(c.isdigit() for c in curLine)  # num of digits in curLine is the number of columns

            lines.append(','.join(line))

    return '\n'.join(lines)


# code to read in arguments from command line
filePath = ''
secondsToLearn = 0
probability_To_Desired_Direction = 0
constant_reward = 0

if __name__ == "__main__":
    FilePath = sys.argv[1]
    secondsToLearn = float(sys.argv[2])
    probability_To_Desired_Direction = float(sys.argv[3])
    probability_To_Any_Other_Direction = round(((1.0 - probability_To_Desired_Direction)/2), 3)
    move_weights = [probability_To_Desired_Direction,probability_To_Any_Other_Direction,probability_To_Any_Other_Direction]
    constant_reward = float(sys.argv[4])
    map_str = _readFile(FilePath)
    # m = Map(move_weights = move_weights)
    m = Map(move_weights = move_weights,map_str = map_str)
    Q = QFunc(m,action_cost = constant_reward)
    finish_time = secondsToLearn + time.time()
    pos = m.random_non_terminal()
    while(finish_time > time.time()):
        new_pos = Q.make_move(pos)
        if not new_pos in m.non_terminals:
            pos = m.random_non_terminal()
        else:
            pos = new_pos
    result = Q.get_readable_Q()
    for y in result:
        print(y)

    for row in Q.Q:
        print(row)
