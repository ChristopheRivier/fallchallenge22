import pytest

from game import Game

def test_game():
    my_robot = list()
    en_robot = list()
    width,height = 13,6
    my_matter,opp_matter = 80,70
    my_map = list()
    f = open("src/sample1.txt", "r")

    for i in range(height):
        line = list()
        for j in range(width):
            # owner: 1 = me, 0 = foe, -1 = neutral
            a={}
            a['scrap_amount'], a['owner'], a['units'], a['recycler'], a['can_build'], a['can_spawn'], a['in_range_of_recycler'] = [int(k) for k in f.readline().split()]
            if a['owner']==1 and a['units']>0:
                # it is my robot
                my_robot.append({ 'x': i, 'y': j, 'units': a['units']})
            elif a['owner']==0 and a['units']>0:
                en_robot.append({ 'x': i, 'y': j, 'units': a['units']})
            line.append(a)
        my_map.append(line)

    game = Game(width,height,my_map,my_robot,en_robot,my_matter,opp_matter)
    game.calcul_action()

