
import sys #exclude
import math #exclude
pond_owner = 1
pond_scrap = 1
pond_units = 2
pond_chemin = 1
pond_dist = 0.5
debug = True #exclude

def distance(x,y, x1,y1):
    return math.sqrt((x-x1)**2+(y-y1)**2)
def deb(str):
    if debug:
        print(str, file=sys.stderr, flush=True)
class Game:
    def __init__(self, w, h):    
        self.width = w
        self.height = h
        self.nb_of_round = 0
        self.center_x = int(self.height/2)
        self.center_y = int(self.width/2)

    def init_round(self, m, r, r_e,matter,op_matt):
        self.my_robot = r
        self.en_robot = r_e
        self.map = m
        self.my_matter = matter
        self.opp_matter = op_matt
        self.nb_of_round += 1

    def get_pos_n(self, robot):
        return (robot['x'],robot['y']-1)

    def get_pos_s(self, robot):
        return (robot['x'],robot['y']+1)

    def get_pos_w(self, robot):
        return (robot['x']-1,robot['y'])

    def get_pos_e(self, robot):
        return (robot['x']+1,robot['y'])

    def getNorth(self, x, y):
        if y>0:
            return self.map[x][y-1]
        return None
    def getSouth(self, x, y):
        if y<self.width-1:
            return self.map[x][y+1]
        return None
    def getWest(self, x, y):
        if x>0:
            return self.map[x-1][y]
        return None
    def getEast(self, x, y):
        if x<self.height-1:
            return self.map[x+1][y]
        return None

    def ponderation(self, brick):
        if brick is None or brick['scrap_amount']==0:
            return -1
        ret = 0
        if self.cell_attaquable(brick):
            if brick['owner']==0:
                ret += brick['units']*pond_owner
            else:
                ret += brick['scrap_amount'] * pond_scrap
        return ret

    def move_robot(self, robot):
        # find best move
        tuple_move = set()
        for num_robot in range(robot['units']):
            n = self.getNorth(robot['x'], robot['y'])
            s = self.getSouth(robot['x'], robot['y'])
            w = self.getWest(robot['x'], robot['y'])
            e = self.getEast(robot['x'], robot['y'])

            if self.nb_of_round<20:
                target_x=self.center_x
                target_y=self.center_y
            else:
                target_x=robot['x']
                target_y=robot['y']

            p_n = self.map[n['x']][n['y']]['chemin']*pond_chemin + distance(n['x'],n['y'],target_x,target_y)*pond_dist if n else None
            p_s = self.map[s['x']][s['y']]['chemin']*pond_chemin + distance(s['x'],s['y'],target_x,target_y)*pond_dist if s else None
            p_w = self.map[w['x']][w['y']]['chemin']*pond_chemin + distance(w['x'],w['y'],target_x,target_y)*pond_dist if w else None
            p_e = self.map[e['x']][e['y']]['chemin']*pond_chemin + distance(e['x'],e['y'],target_x,target_y)*pond_dist if e else None
            if (p_n is not None and (p_s is None or p_n <= p_s ) and
                                    (p_w is None or p_n <= p_w ) and 
                                    (p_e is None or p_n<= p_e)):
                x,y = self.get_pos_n(robot)
            if (p_s is not None and (p_n is None or p_s <= p_n) and
                                    (p_w is None or p_s<=p_w) and 
                                    (p_e is None or p_s<= p_e)):
                x,y = self.get_pos_s(robot)
            if (p_e is not None and (p_s is None or p_e<=p_s) and
                                    (p_n is None or p_e<=p_n) and 
                                    (p_w is None or p_e<=p_w)):
                x,y = self.get_pos_e(robot)
            if (p_w is not None and (p_e is None or p_w<=p_e) and
                                    (p_s is None or p_w<=p_s) and 
                                    (p_n is None or p_w<=p_n)):
                x,y = self.get_pos_w(robot)
            # need to store where I go to
            if self.map[x][y]['chemin']==0:
                # need to recalculate position
                self.map[x][y]['chemin']=None

                self.map[x][y]['owner']=2
                tuple_xy = list()
                if n:
                    self.map[n['x']][n['y']]['chemin']=None
                    tuple_xy.append((n['x'],n['y']))
                if s:
                    self.map[s['x']][s['y']]['chemin']=None
                    tuple_xy.append((s['x'],s['y']))
                if e:
                    self.map[e['x']][e['y']]['chemin']=None
                    tuple_xy.append((e['x'],e['y']))
                if w:
                    self.map[w['x']][w['y']]['chemin']=None
                    tuple_xy.append((w['x'],w['y']))
                tuple_xy.append((x,y))
                self.update_chemin(tuple_xy)
            tuple_move.update([(x,y)])
        ret=""
        nb_units = robot['units']
        nb_units = int(nb_units/len(tuple_move))

        for x,y in tuple_move:
            if ret:
                ret = f"{ret};"
            ret = f"MOVE {nb_units} {robot['y']} {robot['x']} {y} {x}"
        return ret

    def get_build(self):
        def get_ponderation(el):
            return el['ponderation']
        # do we have the middle of the map
        find = False
        ret = ""
        for x in range(self.height):
            brick = self.map[x][self.center_y]
            if brick['owner']==1 and brick['units']==0 and brick['recycler']==0:
                find=True
                break
        if find:
            ret += f"BUILD {self.center_y} {x};"
        # find where to create new robot
        lst_pond = list()
        for i in range(self.height):
          for j in range(self.width):
            if self.map[i][j]['owner']==1:
                # calcul a ponderation for the each cell.
                pond = 0
                if self.getNorth(i,j) is not None:
                    pond += self.ponderation(self.getNorth(i,j))
                if self.getSouth(i,j) is not None:
                    pond += self.ponderation(self.getSouth(i,j))
                if self.getEast(i,j) is not None:
                    pond += self.ponderation(self.getEast(i,j))
                if self.getWest(i,j) is not None:
                    pond += self.ponderation(self.getWest(i,j))
                a = {}
                a['x']=i
                a['y']=j
                a['ponderation']=pond
                lst_pond.append(a)
        lst_pond.sort(key=get_ponderation,reverse=True)
        ff = 0
        while self.my_matter>=10:
            ret = f"{ret}SPAWN 1 {lst_pond[ff]['y']} {lst_pond[ff]['x']};"
            ff += 1
            self.my_matter-=10

        return ret

    def get_nb_case_interessante(self, brick) -> int:
        ret = 0
        if brick and self.cell_attaquable(brick):
            ret+=1
        return ret

    def cell_attaquable(self, brick):
        return brick['owner']!=1 and brick['recycler']==0 and brick['scrap_amount']>0

    def calc_map(self):
        """ Calcul de distance entre la zone qui m'appartient et la zone vide ou adversaire 
            ajout information dans la brick
            nb de case vide ou appartenant a l'adversaire
            calcul du chemin le plus court
        """
        tuple_xy = list()
        for i in range(self.height):
          for j in range(self.width):
            nb_case_interessante=0
            if self.getNorth(i,j):
                nb_case_interessante += self.get_nb_case_interessante(self.getNorth(i,j))
            if self.getSouth(i,j):
                nb_case_interessante += self.get_nb_case_interessante(self.getSouth(i,j))
            if self.getEast(i,j):
                nb_case_interessante += self.get_nb_case_interessante(self.getEast(i,j))
            if self.getWest(i,j) :
                nb_case_interessante += self.get_nb_case_interessante(self.getWest(i,j))
            self.map[i][j]['case_autour']=nb_case_interessante
            if self.cell_attaquable(self.map[i][j]):
                self.map[i][j]['chemin']=0
            elif self.map[i][j]['recycler']==1 or self.map[i][j]['scrap_amount']==0:
                self.map[i][j]['chemin']=100
            elif nb_case_interessante>0:
                self.map[i][j]['chemin']=1
            else:
                tuple_xy.append((i,j))
        self.update_chemin(tuple_xy)

    def update_chemin(self, tuple_xy):
        autre_list = list()
        for i,j in tuple_xy:
            chemin=None
            if self.getNorth(i,j):
                if('chemin' in self.getNorth(i,j)):
                    cc = self.getNorth(i,j)['chemin']
                    chemin = cc+1 if chemin is None or chemin>cc else chemin
            if self.getSouth(i,j):
                if('chemin' in self.getSouth(i,j)):
                    cc = self.getSouth(i,j)['chemin']
                    chemin = cc+1 if chemin is None or chemin>cc else chemin
            if self.getEast(i,j):
                if('chemin' in self.getEast(i,j)):
                    cc = self.getEast(i,j)['chemin']
                    chemin = cc+1 if chemin is None or chemin>cc else chemin
            if self.getWest(i,j) :
                if('chemin' in self.getWest(i,j)):
                    cc = self.getWest(i,j)['chemin']
                    chemin = cc+1 if chemin is None or chemin>cc else chemin
            if chemin:
                self.map[i][j]['chemin']=chemin
            else:
                autre_list.append((i,j))
        if autre_list:
            self.update_chemin(autre_list)

        
    def calcul_action(self):
        actions = ""
        self.calc_map()
        for r in self.my_robot:
            sep="" if actions == "" else ";"
            actions = f"{actions}{sep}{self.move_robot(r)}"
        if actions=="":
            actions = "WAIT"
        if self.my_matter>=10:
            actions = f"{self.get_build()}{actions}"
        print(actions)

