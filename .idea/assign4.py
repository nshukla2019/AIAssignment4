import random
from enum import IntEnum

class Move(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class QFunc():
    def __init__(self, map, moves = [Move.UP,Move.RIGHT,Move.DOWN,Move.LEFT]):
        self.map = map
        self.moves = moves
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

class Map():
    def __init__(self, size):
        self.size = size
        self.map = self.make_map()

    def map_fill(self):
        choices = [0,1,-1]
        weights = [95,2.5,2.5]
        return random.choices(choices,weights = weights,k=1)[0]

    def random_pos(self):
        return (random.randint(0,self.size[0]-1),random.randint(0,self.size[1]-1))

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
            map[terminal_high[1]][terminal_high[0]] = 1
            map[terminal_low[1]][terminal_low[0]] = -1
        elif not has_terminals[0]:
            terminal_high = self.random_pos()
            map[terminal_high[1]][terminal_high[0]] = 1
        elif not has_terminals[1]:
            terminal_low = self.random_pos()
            map[terminal_low[1]][terminal_low[0]] = -1
        return map

    def map_to_string(self):
        return '\n'.join([','.join([str(x) for x in self.map[y]]) for y in range(self.size[1])])

    def map_to_file(self,filepath):
        file = open(filepath,'w')
        file.write(map_to_string(self.map))
        file.close()


m = Map((6,5))
print(m.map_to_string())
Q = QFunc(m)
print(Q.lookup_Q((0,0),Move.UP))
