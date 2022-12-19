import sys
import math

debug = True
debug_entry = False
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def print_entry(str):
    if debug_entry:
        print(str, file=sys.stderr, flush=True)
def deb(str):
    if debug:
        print(str, file=sys.stderr, flush=True)

from game import Game

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
            a['x'], a['y'] = i, j
            print_entry(f"{a['scrap_amount']} {a['owner']} {a['units']} {a['recycler']} {a['can_build']} {a['can_spawn']} {a['in_range_of_recycler']}")
            if a['owner']==1 and a['units']>0:
                # it is my robot
                my_robot.append({ 'x': i, 'y': j, 'units': a['units']})
            elif a['owner']==0 and a['units']>0:
                en_robot.append({ 'x': i, 'y': j, 'units': a['units']})
            line.append(a)
        my_map.append(line)
    
    game = Game(width,height,my_map,my_robot,en_robot,my_matter,opp_matter)

    game.calcul_action()

