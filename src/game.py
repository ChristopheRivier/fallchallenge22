
pond_owner = 1
pond_units = 2

class Game:
    def __init__(self, w, h, m, r, r_e,matter,op_matt):
        self.width = w
        self.height = h
        self.my_robot = r
        self.en_robot = r_e
        self.map = m
        self.my_matter = matter
        self.opp_matter = op_matt

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
            return -1000
        ret = 0
        if brick['owner']!=1:
            ret = brick['scrap_amount'] * pond_owner
        return ret

    def ponderation_robot(self, brick, robot):
        ret = self.ponderation(brick)
        if brick and brick['owner']!=1:
            ret += (robot['units'] - brick['units'])*pond_units
        return ret

    def move_robot(self, robot):
        # find best move
        n = self.getNorth(robot['x'], robot['y'])
        s = self.getSouth(robot['x'], robot['y'])
        w = self.getWest(robot['x'], robot['y'])
        e = self.getEast(robot['x'], robot['y'])

        p_n = self.ponderation_robot(n,robot)
        p_s = self.ponderation_robot(s,robot)
        p_w = self.ponderation_robot(w,robot)
        p_e = self.ponderation_robot(e,robot)

        if p_n >= p_s and p_n >= p_w and p_n >= p_e:
            x,y = self.get_pos_n(robot)
        if p_s >= p_n and p_s>=p_w and p_s>= p_e:
            x,y = self.get_pos_s(robot)
        if p_e>=p_s and p_e>=p_n and p_e>=p_w:
            x,y = self.get_pos_e(robot)
        if p_w>=p_e and p_w>=p_s and p_w>=p_n:
            x,y = self.get_pos_w(robot)
        return f"MOVE {robot['units']} {robot['y']} {robot['x']} {y} {x}"

    def get_build(self):
        # find where to create new robot
        max_pond = -1
        buildx,buildy=-1,-1
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
                if max_pond<pond:
                    max_pond = pond
                    buildx = i
                    buildy = j
        return f"SPAWN 1 {buildy} {buildx};"

    def calcul_action(self):
        actions = ""
        for r in self.my_robot:
            sep="" if actions == "" else ";"
            actions = f"{actions}{sep}{self.move_robot(r)}"
        if actions=="":
            actions = "WAIT"
        if self.my_matter>10:
            actions = f"{self.get_build()}{actions}"
        print(actions)

