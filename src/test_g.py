import pytest

from game import Game


def init_data(filename, w,h,mat,opp)-> Game:
    my_robot = list()
    en_robot = list()
    width,height = w,h
    my_matter,opp_matter = mat, opp
    my_map = list()
    f = open(filename, "r")
    game = Game(width, height)
    for i in range(height):
        line = list()
        for j in range(width):
            # owner: 1 = me, 0 = foe, -1 = neutral
            a={}
            a['scrap_amount'], a['owner'], a['units'], a['recycler'], a['can_build'], a['can_spawn'], a['in_range_of_recycler'] = [int(k) for k in f.readline().split()]
            a['x'], a['y'] = i, j
            if a['owner']==1 and a['units']>0:
                # it is my robot
                my_robot.append({ 'x': i, 'y': j, 'units': a['units']})
            elif a['owner']==0 and a['units']>0:
                en_robot.append({ 'x': i, 'y': j, 'units': a['units']})
            line.append(a)
        my_map.append(line)

    game.init_round(my_map,my_robot,en_robot,my_matter,opp_matter)
    return game

def test_game():
    
    #game = init_data("src/sample1.txt", 13,6,80,70)
    game = init_data("src/test_data/map_init.txt", 17,8,10,10)
    
    game.calcul_action()



def test_game():
    
    #game = init_data("src/sample1.txt", 13,6,80,70)
    game = init_data("src/test_data/test_spawn", 14,7,10,29)
    
    game.calcul_action()
