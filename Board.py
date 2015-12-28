import copy
class Board(object):
    def __init__(self):
        self.p=[]
        for _ in range(8):
            self.p.append([None]*8)
        self.turn=0
    def get_p(self,x,y):
        return self.p[x][y]
    def add_p(self,pc,x,y,c):
        self.p[x][y]=pc(x,y,c)
    def move_p(self,p,tx,ty,c=False):
        sx=p.x
        sy=p.y
        if not c:
            bcopy=copy.deepcopy(self)
            bcopy.move_p(bcopy.get_p(sx,sy),tx,ty,True)
            if not bcopy.ischeck(self.turn):
                self.p[tx][ty]=p
                self.p[p.x][p.y]=None
                p.place(tx,ty)
                return True
            return False
        else:
            self.p[tx][ty]=p
            self.p[p.x][p.y]=None
            p.place(tx,ty)

    def ischeck(self,side):
        royalps=[]
        for row in self.p:
            for p in row:
                if p and p.c==side and p.royal:
                    royalps.append([p.x,p.y])
        for row in self.p:
            for p in row:
                if p and p.c==1-side and [pos for pos in p.get_moves(self.p) if pos in royalps]:
                    return True
        return False
    def is_mate(self,side):
        for row in self.p:
            for p in row:
                if p and p.c==side:
                    for mx,my in p.get_moves(self.p):
                        bco=copy.deepcopy(self)
                        bco.move_p(bco.get_p(p.x,p.y),mx,my,True)
                        if not bco.ischeck(side):
                            return False
        return True
    def gen_ps(self,side=None):
        for row in self.p:
            for p in row:
                if p and (side is None or p.c==side):
                    yield p

