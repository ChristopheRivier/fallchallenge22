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



def test_game2():
    
    #game = init_data("src/sample1.txt", 13,6,80,70)
    game = init_data("src/test_data/test_spawn", 14,7,10,29)
    
    game.calcul_action()


def test_bloc():
    
    #game = init_data("src/sample1.txt", 13,6,80,70)
    game = init_data("src/test_data/blocage", 16,8,16,16)
    game.nb_of_round=32
    game.calcul_action()

def test_stay():
    game = init_data("src/test_data/stay", 23,11,15,40)
    game.nb_of_round=32
    game.calcul_action()


def test_gain():
    game = init_data("src/test_data/test_", 15,7,10,10)
    game.nb_of_round=5
    game.calcul_action()


def test_move():
    game = init_data("src/test_data/test_move", 21,10,29,10)
    game.nb_of_round=10
    game.calcul_action()


def test_chemin():
    game = init_data("src/test_data/test_chemin", 18,9,18,10)
    game.nb_of_round=42
    game.calcul_action()


def test_spawn2():
    game = init_data("src/test_data/test_spawn2", 15,7,140,23)
    game.nb_of_round=42
    game.calcul_action()
    assert False

def test_deplacement():
    #seed=6772313716882704000

    game = init_data("src/test_data/test_deplacement", 14,7,18,14)
    game.attaque['36'] = {'nb_tour':4, 'round':23, 'units': 2}
    game.nb_of_round=23
    ret = game.get_action()
    assert ret == 'SPAWN 1 6 3;MESSAGE three;MOVE 3 6 3 6 2'


def test_deplacement():
    #seed=2810236576456295000

    game = init_data("src/test_data/test_apparition", 13,6,18,14)
    game.nb_of_round=25
    ret = game.get_action()
    assert 'SPAWN 1 7 3' in ret

