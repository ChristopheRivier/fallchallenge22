
import sys #exclude
import math #exclude
pond_owner = 0.5
pond_scrap = 1
pond_en = -1
pond_chemin = 0.9
pond_dist = 0.8
pond_autour = 0.6
pond_moi = 1.1
pond_unit_enemy = 0.5
can_i_build = False
nb_matter_to_build = 27
debug = True #exclude
debug_map = True

def distance(x,y, x1,y1):
    return math.sqrt((x-x1)**2+(y-y1)**2)
def deb(str):
    if debug:
        print(str, file=sys.stderr, flush=True)
class Game:
    def print_map(self, truc):
        if debug_map:
            for i in range(self.height):
                line=""
                for j in range(self.width):
                    line = f"{line} {self.map[i][j][truc]:03}"
                print(line, file=sys.stderr, flush=True)
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
        self.nb_of_round = self.nb_of_round + 1

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
        ret = -1
        if self.cell_attaquable(brick):
            if brick['owner']==0:
                ret += brick['units']*pond_owner + pond_en
            else:
                ret += brick['scrap_amount'] * pond_scrap
        elif brick['owner']==1 and brick['recycler']==0:
            ret = 0
        return ret

    def move_robot(self, robot, element):
        def is_move(b):
            return b and self.map[b['x']][b['y']]['scrap_amount']>0 and self.map[b['x']][b['y']]['recycler']==0
        def calc_ponderation(b):
            if is_move(b):
                nb_unit_en = self.get_truc(b['x'],b['y'],'units') if self.get_truc(b['x'],b['y'],'owner')==0 else 0
                return (self.map[b['x']][b['y']][element]*pond_chemin + 
                        distance(b['x'],b['y'],target_x,target_y)*pond_dist +
                        self.get_truc(b['x'],b['y'],'case_autour')*pond_autour +
                        self.get_truc(b['x'],b['y'],'owner')*pond_moi +
                        nb_unit_en * -pond_unit_enemy 
                        )
            else:
                return None
        # find best move
        robot_units = robot['units'] # self.get_truc(robot['x'],robot['y'],'units')
        tuple_move = set()
        for num_robot in range(robot_units):
            n = self.getNorth(robot['x'], robot['y'])
            s = self.getSouth(robot['x'], robot['y'])
            w = self.getWest(robot['x'], robot['y'])
            e = self.getEast(robot['x'], robot['y'])
            
            target_x=self.center_x
            target_y=self.center_y

            p_n = calc_ponderation(n)
            p_s = calc_ponderation(s)
            p_w = calc_ponderation(w)
            p_e = calc_ponderation(e)
            x,y=-1,-1
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
            unit_needed = 0
            if x!=-1 and self.map[x][y][element]==0:
                if element == 'chemin':
                    # need to recalculate position
                    if self.map[x][y]['units']<robot_units:
                        self.map[x][y][element]=None
                        self.map[x][y]['owner']=2
                        tuple_xy = list()
                        if n:
                            self.map[n['x']][n['y']][element]=None
                            tuple_xy.append((n['x'],n['y']))
                        if s:
                            self.map[s['x']][s['y']][element]=None
                            tuple_xy.append((s['x'],s['y']))
                        if e:
                            self.map[e['x']][e['y']][element]=None
                            tuple_xy.append((e['x'],e['y']))
                        if w:
                            self.map[w['x']][w['y']][element]=None
                            tuple_xy.append((w['x'],w['y']))
                        tuple_xy.append((x,y))
                        self.update_chemin(tuple_xy)
                        unit_needed = self.map[x][y]['units']
                    elif self.map[x][y]['units']>=robot_units:
                        unit_needed = robot_units
            if x!=-1:
                # move all units in the new cell.
                if self.get_truc(x,y,'owner')==0 and self.get_truc(x,y,'units')>0 and self.get_truc(x,y,'units')<=robot_units:
                    tuple_move = set()
                    tuple_move.update([(x,y,unit_needed)])
                    break
                tuple_move.update([(x,y,unit_needed)])
        ret=""
        
        need_unit = 0
        nb_not_null = 0
        for xm,ym,ne in tuple_move:
            if ne==0:
                nb_not_null += 1
            need_unit += ne
        nb_units = robot_units
        if need_unit < nb_units:
            nb_units -= need_unit

        if nb_not_null!=0:
            nb_units = int(nb_units/nb_not_null)

        if element == 'chemin':
            for xm,ym,ne in tuple_move:
                if ret:
                    ret = f"{ret};"
                a = nb_units
                if ne:
                    a = ne
                ret = f"{ret}MOVE {a} {robot['y']} {robot['x']} {ym} {xm}"
        else:
            for xm,ym, ne in tuple_move:
                brick = self.map[xm][ym]
                a = nb_units
                if ne:
                    a = ne
                if brick['owner']==1:
                    if brick['units']<a:
                        brick['units'] = a-brick['units']
                        brick['owner'] = 0
                    else:
                        brick['units'] = brick['units'] - a
                    self.map[robot['x']][robot['y']]['units'] -= a
                else:
                    brick['units'] += a
                    self.map[robot['x']][robot['y']]['units'] -= a 

        return ret

    def get_build(self):
        def get_ponderation(el):
            return el['ponderation']
        def get_recycler(el):
            return el['recycler_scrap']
        def ponderation_scrap_amount(brick):
            if brick is None:
                return 0
            ret = 0
            if brick['owner']==0 and brick['units']>0:
                ret += 15
            elif brick['owner']==1 and brick['units']>0:
                ret -= 8
            else:
                ret += brick['scrap_amount']
            return ret
        # find where to create new robot
        lst_pond = list()
        for i in range(self.height):
          for j in range(self.width):
            if self.map[i][j]['owner']==1:
                # calcul a ponderation for the each cell.
                pond = 0
                p_scrap = 0
                if self.getNorth(i,j) is not None:
                    pond += self.ponderation(self.getNorth(i,j))
                    p_scrap += ponderation_scrap_amount(self.getNorth(i,j))
                if self.getSouth(i,j) is not None:
                    pond += self.ponderation(self.getSouth(i,j))
                    p_scrap += ponderation_scrap_amount(self.getSouth(i,j))
                if self.getEast(i,j) is not None:
                    pond += self.ponderation(self.getEast(i,j))
                    p_scrap += ponderation_scrap_amount(self.getEast(i,j))
                if self.getWest(i,j) is not None:
                    pond += self.ponderation(self.getWest(i,j))
                    p_scrap += ponderation_scrap_amount(self.getWest(i,j))
                a = {}
                a['x']=i
                a['y']=j
                a['ponderation']=pond
                if self.get_truc(i,j,'units')==0 and self.get_truc(i,j,'recycler')==0 and self.get_truc(i,j,'scrap_amount')>3:
                    a['recycler_scrap']=p_scrap
                else:
                    a['recycler_scrap']=0
                lst_pond.append(a)
        lst_pond.sort(key=get_recycler,reverse=True)
        # do we have the middle of the map
        ret = ""
        ff = 0
        if lst_pond[ff]['recycler_scrap']>nb_matter_to_build and can_i_build:
            ret = f"BUILD {lst_pond[ff]['y']} {lst_pond[ff]['x']}"
            self.my_matter-=10
            ff = 0
            lst_pond.pop(0)
        lst_pond.sort(key=get_ponderation,reverse=True)
        while self.my_matter>=10:
            sep="" if ret == "" else ";"
            ret = f"{ret}{sep}SPAWN 1 {lst_pond[ff]['y']} {lst_pond[ff]['x']}"
            ff += 1
            self.my_matter-=10

        return ret

    def get_nb_case_interessante(self, brick) -> int:
        ret = 0
        if brick and self.cell_attaquable(brick):
            ret+=1
        return ret
    def get_nb_case_interessante_en(self, brick)-> int:
        ret = 0
        if brick and self.cell_attaquable_en(brick):
            ret+=1
        return ret
    def get_truc(self, x, y, truc):
        return self.map[x][y][truc]

    def add_truc(self, x, y, truc, val):
        if truc not in self.map[x][y] or self.map[x][y][truc] is None:
            self.map[x][y][truc] = val

    def cell_attaquable(self, brick):
        return brick['owner']!=1 and brick['recycler']==0 and brick['scrap_amount']>0
    def cell_attaquable_en(self, brick):
        return brick['owner']!=0 and brick['recycler']==0 and brick['scrap_amount']>0


    def calc_map(self):
        """ Calcul de distance entre la zone qui m'appartient et la zone vide ou adversaire 
            ajout information dans la brick
            nb de case vide ou appartenant a l'adversaire
            calcul du chemin le plus court
        """
        self.my_point=0
        self.en_point=0
        self.to_take=0
        self.nb_my_recycler = 0
        tuple_xy = set()
        for i in range(self.height):
          for j in range(self.width):
            nb_case_interessante=0
            nb_case_interessante_en=0
            scrap = 0
            if self.getNorth(i,j):
                b=self.getNorth(i,j)
                nb_case_interessante += self.get_nb_case_interessante(b)
                nb_case_interessante_en += self.get_nb_case_interessante_en(b)
                scrap += self.get_truc(b['x'],b['y'],'scrap_amount')
            if self.getSouth(i,j):
                b=self.getSouth(i,j)
                nb_case_interessante += self.get_nb_case_interessante(b)
                nb_case_interessante_en += self.get_nb_case_interessante_en(b)
                scrap += self.get_truc(b['x'],b['y'],'scrap_amount')
            if self.getEast(i,j):
                b=self.getEast(i,j)
                nb_case_interessante += self.get_nb_case_interessante(b)
                nb_case_interessante_en += self.get_nb_case_interessante_en(b)
                scrap += self.get_truc(b['x'],b['y'],'scrap_amount')
            if self.getWest(i,j) :
                b=self.getWest(i,j)
                nb_case_interessante += self.get_nb_case_interessante(b)
                nb_case_interessante_en += self.get_nb_case_interessante_en(b)
                scrap += self.get_truc(b['x'],b['y'],'scrap_amount')
            self.map[i][j]['case_autour']=nb_case_interessante
            self.map[i][j]['recycler_scrap']=scrap
            if self.cell_attaquable(self.map[i][j]):
                self.map[i][j]['chemin']=0
            elif self.map[i][j]['recycler']==1 or self.map[i][j]['scrap_amount']==0:
                self.map[i][j]['chemin']=100
            elif nb_case_interessante>0:
                self.map[i][j]['chemin']=1
            else:
                tuple_xy.update([(i,j)])
            if self.cell_attaquable_en(self.map[i][j]):
                self.map[i][j]['chemin_en']=0
            elif self.map[i][j]['recycler']==1 or self.map[i][j]['scrap_amount']==0:
                self.map[i][j]['chemin_en']=100
            elif nb_case_interessante_en>0:
                self.map[i][j]['chemin_en']=1
            else:
                tuple_xy.update([(i,j)])

            if self.get_truc(i,j,'owner')==0:
                self.en_point+=1
            elif self.get_truc(i,j,'owner') in (1,2):
                self.my_point+=1
                if self.get_truc(i,j,'recycler')==1:
                    self.nb_my_recycler+=1
            elif self.get_truc(i,j,'scrap_amount')>0:
                self.to_take+=1
        self.update_chemin(tuple_xy)

    def update_chemin(self, tuple_xy, recurs=10):
        def is_move(b):
            return b and b['scrap_amount']>0 and b['recycler']==0
        def get_chemin(element,brick,chem):
            if(is_move(brick) and element in brick):
                cc = brick[element]
                if cc:
                    chem = cc+1 if chem is None or chem>cc else chem
            return chem

        autre_list = set()
        for i,j in tuple_xy:
            chemin=None
            chemin_en=None
            if self.getNorth(i,j):
                chemin = get_chemin('chemin',self.getNorth(i,j), chemin)
                chemin_en = get_chemin('chemin_en',self.getNorth(i,j), chemin_en)
            if self.getSouth(i,j):
                chemin = get_chemin('chemin', self.getSouth(i,j), chemin)
                chemin_en = get_chemin('chemin_en', self.getSouth(i,j), chemin_en)
            if self.getEast(i,j):
                chemin = get_chemin('chemin', self.getEast(i,j), chemin)
                chemin_en = get_chemin('chemin_en', self.getEast(i,j), chemin_en)
            if self.getWest(i,j) :
                chemin = get_chemin('chemin', self.getWest(i,j), chemin)
                chemin_en = get_chemin('chemin_en', self.getWest(i,j), chemin_en)
            if chemin:
                self.add_truc(i, j, 'chemin', chemin)
            else:
                autre_list.update([(i,j)])
            if chemin_en:
                self.add_truc(i, j, 'chemin_en', chemin_en)
            else:
                autre_list.update([(i,j)])
        recurs -= 1
        if autre_list and recurs>0:
            self.update_chemin(autre_list, recurs)
        else:
            for i,j in tuple_xy:
                self.add_truc(i, j, 'chemin', 10)
                self.add_truc(i, j, 'chemin_en', 10)

        
    def calcul_action(self):
        actions = ""
        global pond_owner
        global pond_scrap
        global pond_en
        global pond_chemin
        global pond_dist
        global pond_autour
        global pond_moi
        global pond_unit_enemy
        global can_i_build
        global nb_matter_to_build

        # calcul deplacement ennemy
        self.calc_map()

        condition=""
        if self.to_take> self.en_point and self.to_take>self.my_point:
            condition="one"
            pond_owner = 0.4
            pond_scrap = 0.2
            pond_en = 0.5
            pond_chemin = 1.7
            if self.nb_of_round<(self.width+1/2):
                pond_dist = 0.6
            else:
                pond_dist=0
            pond_autour = 0.2
            pond_moi = 2
            pond_unit_enemy = 0.1
            if self.nb_my_recycler<(len(self.my_robot)/4):
                can_i_build = True
            else:
                can_i_build = False
            nb_matter_to_build = 27
        elif self.en_point > self.my_point and len(self.en_robot)>len(self.my_robot) and False:
            condition="two"
            pond_owner = 1.2
            pond_scrap = 0.1
            pond_en = 0.5
            pond_chemin = 1.1
            pond_dist = 0
            pond_autour = 0.1
            pond_moi = 1.1
            pond_unit_enemy = 0.5
            can_i_build = False
            nb_matter_to_build = 26
        elif self.en_point>self.my_point:
            condition="three"
            pond_owner = 1
            pond_scrap = 0.1
            pond_en = 2
            pond_chemin = 1.4 
            pond_dist = 0
            pond_autour = 0.3
            pond_moi = 1.2
            pond_unit_enemy = 2
            can_i_build = False
            nb_matter_to_build = 28
        elif self.en_point < self.my_point:
            condition="four"
            pond_owner = 0.7
            pond_scrap = 0
            pond_en = 2
            pond_chemin = 1.2
            pond_dist = 0
            pond_autour = 0
            pond_moi = 10
            pond_unit_enemy = 2
            can_i_build = True
            nb_matter_to_build = 30
        if condition:
            sep = "" if actions =="" else ";"
            actions = f"MESSAGE {condition}"
        if self.width<12 and self.nb_of_round<(self.width/2):
            # during first round increase number of robot before recycler
            can_i_build=False
        
        # spawn before move
        if self.my_matter>=10:
            sep = "" if actions =="" else ";"
            actions = f"{self.get_build()}{sep}{actions}"

        self.print_map('units')
        for r in self.en_robot:
            sep="" if actions == "" else ";"
            self.move_robot(r, 'chemin_en')
        
        # clean chemin
        self.print_map('units')
        for i in range(self.height):
            for j in range(self.width):
                self.map[i][j]['chemin']=None
                self.map[i][j]['chemin_en']=None

        # calc again with the move of ennemy
        self.calc_map()

        self.print_map('units')

        for r in self.my_robot:
            sep="" if actions == "" else ";"
            if self.get_truc(r['x'],r['y'],'owner')==1:
                r['units'] = self.get_truc(r['x'],r['y'],'units')
                move = self.move_robot(r, 'chemin')
                if move:
                    actions = f"{actions}{sep}{move}"
        if actions=="":
            actions = "WAIT"
        print(actions)

