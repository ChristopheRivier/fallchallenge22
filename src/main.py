import sys
import math

debug = True
debug_entry = False
pond_owner = -10
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def print_entry(str):
    if debug_entry:
        print(str, file=sys.stderr, flush=True)
def deb(str):
    if debug:
        print(str, file=sys.stderr, flush=True)



class Game:
    def __init__(self, w, h, m, r, r_e):
        self.width = w
        self.height = h
        self.my_robot = r
        self.en_robot = r_e
        self.map = m

    def get_pos_n(self, robot):
        return (robot['x'],robot['y']-1)

    def get_pos_s(self, robot):
        return (robot['x'],robot['y']+1)

    def get_pos_w(self, robot):
        return (robot['x']-1,robot['y'])

    def get_pos_e(self, robot):
        return (robot['x']+1,robot['y'])

    def getNorth(self, robot):
        if robot['y']>0:
            return self.map[robot['x']][robot['y']-1]
        return None
    def getSouth(self, robot):
        if robot['y']<self.width-1:
            return self.map[robot['x']][robot['y']+1]
        return None
    def getWest(self, robot):
        if robot['x']>0:
            return self.map[robot['x']-1][robot['y']]
        return None
    def getEast(self, robot):
        if robot['x']<self.height-1:
            return self.map[robot['x']+1][robot['y']]
        return None

    def ponderation(self, brick):
        if brick is None or brick['scrap_amount']==0:
            return -1000
        ret = brick['owner']*pond_owner
        return ret

    def move_for_one_robot(self, robot):
        # find best move
        deb(f"north {robot}")
        n = self.getNorth(robot)
        deb(f"s {robot}")

        s = self.getSouth(robot)
        w = self.getWest(robot)
        e = self.getEast(robot)

        p_n = self.ponderation(n)
        p_s = self.ponderation(s)
        p_w = self.ponderation(w)
        p_e = self.ponderation(e)

        if p_n >= p_s and p_n >= p_w and p_n >= p_e:
            return self.get_pos_n(robot)
        if p_s >= p_n and p_s>=p_w and p_s>= p_e:
            return self.get_pos_s(robot)
        if p_e>=p_s and p_e>=p_n and p_e>=p_w:
            return self.get_pos_e(robot)
        if p_w>=p_e and p_w>=p_s and p_w>=p_n:
            return self.get_pos_w(robot)

    def calcul_action(self):
        r = self.my_robot[0]
        x, y = self.move_for_one_robot(r)

        print(f"MOVE 1 {r['y']} {r['x']} {y} {x}")


width, height = [int(i) for i in input().split()]
print_entry(f"{width} {height}")

# game loop
while True:
    my_robot = list()
    en_robot = list()
    my_matter, opp_matter = [int(i) for i in input().split()]
    print_entry( f"{my_matter} {opp_matter}")
    my_map = list()
    for i in range(height):
        line = list()
        for j in range(width):
            # owner: 1 = me, 0 = foe, -1 = neutral
            a={}
            a['scrap_amount'], a['owner'], a['units'], a['recycler'], a['can_build'], a['can_spawn'], a['in_range_of_recycler'] = [int(k) for k in input().split()]

            print_entry(f"{a['scrap_amount']} {a['owner']} {a['units']} {a['recycler']} {a['can_build']} {a['can_spawn']} {a['in_range_of_recycler']}")
            if a['owner']==1 and a['units']>0:
                # it is my robot
                my_robot.append({ 'x': i, 'y': j, 'units': a['units']})
            elif a['owner']==0 and a['units']>0:
                en_robot.append({ 'x': i, 'y': j, 'units': a['units']})
            line.append(a)
        my_map.append(line)
    
    game = Game(width,height,my_map,my_robot,en_robot)

    game.calcul_action()
    #print(my_map, file=sys.stderr, flush=True)
    #print(my_map[0][0], file=sys.stderr, flush=True)
    #for i in my_robot:
    #    print(i, file=sys.stderr, flush=True)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

