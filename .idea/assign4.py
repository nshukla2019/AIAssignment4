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

    # TODO
    def lookup_best_Q(self,pos):
        return max(self.Q[pos[1]][pos[0]])

    # TODO
    def update_Q(self,pos,move):
        self.Q[pos[1]][pos[0]][int(move)] += 0 #use update rule

class Map():
    def __init__(self, size):
        self.size = size
        self.max_fill = [0.5,1.0]
        self.min_fill = [-1.0,-0.5]
        self.fill_weights = [95,2.5,2.5]
        self.move_weights = [90,5,5]
        self.map = self.make_map()

    def map_fill(self):
        max_val = round(random.uniform(self.max_fill[0],self.max_fill[1]),2)
        min_val = round(random.uniform(self.min_fill[0],self.min_fill[1]),2)
        choices = [0,max_val,min_val]
        return random.choices(choices,weights = self.fill_weights,k=1)[0]

    def random_pos(self):
        return (random.randint(0,self.size[0]-1),random.randint(0,self.size[1]-1))

    # checking whether file has terminal states
    def make_map(self):
        has_terminals = (False,False) # high,low
        map = []
        for y in range(self.size[1]):
            map.append([])
            for x in range(self.size[0]):
                place = self.map_fill();
                has_terminals = (has_terminals[0] or place > 0,has_terminals[1] or place < 0)
                map[y].append(place)
        if (not has_terminals[0]) and (not has_terminals[1]):
            terminal_high = self.random_pos()
            terminal_low = self.random_pos()
            while terminal_low == terminal_high:
                terminal_low = self.random_pos()
            map[terminal_high[1]][terminal_high[0]] = round(random.uniform(self.max_fill[0],self.max_fill[1]),2)
            map[terminal_low[1]][terminal_low[0]] = round(random.uniform(self.min_fill[0],self.min_fill[1]),2)
        elif not has_terminals[0]:
            terminal_high = self.random_pos()
            map[terminal_high[1]][terminal_high[0]] = round(random.uniform(self.max_fill[0],self.max_fill[1]),2)
        elif not has_terminals[1]:
            terminal_low = self.random_pos()
            map[terminal_low[1]][terminal_low[0]] = round(random.uniform(self.min_fill[0],self.min_fill[1]),2)
        return map

    def map_to_string(self):
        return '\n'.join([','.join([str(x) for x in self.map[y]]) for y in range(self.size[1])])

    def map_to_file(self,filepath):
        file = open(filepath,'w')
        file.write(map_to_string(self.map))
        file.close()

    def move_deflection(self,move,direction_right):
        if direction_right:
            return Move(Min((int(move)+1),len(self.moves)))
        else:
            return Move(Max((int(move)-1),0))

    def get_move_transition(self,pos,move):
        choices = [0,1,-1]
        deflect = random.choices(choices,weights = self.move_weights,k=1)[0]
        if(deflect == 1):
            move = self.move_deflection(move,True)
        elif(defelct == -1):
            move = self.move_deflection(move,False)
        if(move == move.UP):
            new_y = Max(pos[1]-1,0)
            return (pos[0],new_y)
        elif(move == move.RIGHT):
            new_x = Min(pos[0]+1,self.size[0]-1)
            return (new_x,pos[1])
        elif(move == move.DOWN):
            new_y = Min(pos[1]+1,self.size[1]-1)
            return (pos[0],new_y)
        elif(move == move.LEFT):
            new_x = Max(pos[0]-1,0)
            return (new_x,pos[1])


m = Map((6,5))
print(m.map_to_string())
Q = QFunc(m)
print(Q.lookup_Q((0,0),Move.UP))


# code to read in arguments from command line
filePath = ''
secondsToLearn = 0
probability_To_Desired_Direction = 0
constant_reward = 0

if __name__ == "__main__":
    FilePath = sys.argv[1]
    secondsToLearn = sys.argv[2]
    secondprobability_To_Desired_DirectionsToLearn = sys.argv[3]
    probability_To_Any_Other_Direction = round(((1.0 - PROBABILITY_TO_DESIRED_DIRECTION)/2), 1)
    constant_reward = sys.argv[4]