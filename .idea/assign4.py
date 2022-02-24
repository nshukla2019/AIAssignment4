import random
from enum import IntEnum

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
                if(best_move == 0):
                    readable[y][x] = '^'
                elif(best_move == 1):
                    readable[y][x] = '>'
                elif(best_move == 2):
                    readable[y][x] = '<'
                elif(best_move == 3):
                    readable[y][x] = 'v'
        return readable



class Map():
    def __init__(self, size,moves = [Move.UP,Move.RIGHT,Move.DOWN,Move.LEFT]):
        self.size = size
        self.moves = moves
        self.max_fill = [0.5,1.0]
        self.min_fill = [-1.0,-0.5]
        self.fill_weights = [95,2.5,2.5]
        self.move_weights = [90,5,5]
        self.non_terminals = []
        self.map = self.make_map()

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

    def map_to_string(self):
        return '\n'.join([','.join([str(x) for x in self.map[y]]) for y in range(self.size[1])])

    def map_to_file(self,filepath):
        file = open(filepath,'w')
        file.write(map_to_string(self.map))
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


m = Map((6,5))
print(m.map_to_string())
Q = QFunc(m)

pos = m.random_non_terminal()
for i in range(1000):
    pos = Q.make_move(pos)
    # stop when reach terminal
        # check here if pos is in self.non_terminals
            # if it is not, then we have reached a terminal state
                # pos = m.random_non_terminal() to chose another random start state

    # repeat process at random points

result = Q.get_readable_Q()
for y in result:
    print(y)


# code to read in arguments from command line
filePath = ''
secondsToLearn = 0
probability_To_Desired_Direction = 0
constant_reward = 0

if __name__ == "__main__":
    FilePath = sys.argv[1]
    secondsToLearn = sys.argv[2]
    probability_To_Desired_Direction = sys.argv[3]
    probability_To_Any_Other_Direction = round(((1.0 - probability_To_Desired_Direction)/2), 1)
    constant_reward = sys.argv[4]