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
    def boardvalue(self,side):
        dbv=self.get_delta_board_value(1-side)
        if dbv=="CHECKMATE":
            return -1000
        return sum(p.value for p in self.gen_ps(side))-sum(p.value for p in self.gen_ps(1-side))-self.get_delta_board_value(1-side)
    def basic_board_value(self,side):
        return sum(p.value for p in self.gen_ps(side))-sum(p.value for p in self.gen_ps(1-side))
    def developement_value(self,side):
        ek=[p for p in self.gen_ps(1-side) if p.royal][0]
        return sum([self.dist(p,ek) for p in self.gen_ps(side)])
    def dist(self,p1,p2):
        return abs(p1.x-p2.x)+abs(p1.y-p2.y)
    def get_best_moves(self,side):
        moves=[]
        for row in self.p:
            for p in row:
                if p and p.c==side:
                    for mx,my in p.get_moves(self.p):
                        bco=copy.deepcopy(self)
                        bco.move_p(bco.get_p(p.x,p.y),mx,my,True)
                        if bco.ischeck(1-side) and bco.is_mate(1-side):
                            return [[p,mx,my]]
                        if not bco.ischeck(side):
                            moves.append([p,mx,my,bco.boardvalue(side),bco.developement_value(side)])
        bv=max([m[3] for m in moves])
        bvs=[m[:3]+[m[4]] for m in moves if m[3]==bv]
        bd=min([m[3] for m in bvs])
        return [m[:3] for m in bvs if m[3]==bd]
    def get_delta_board_value(self,side):
        sbv=self.basic_board_value(side)
        moves=[]
        for row in self.p:
            for p in row:
                if p and p.c==side:
                    for mx,my in p.get_moves(self.p):
                        if self.p[mx][my]:
                            bco=copy.deepcopy(self)
                            bco.move_p(bco.get_p(p.x,p.y),mx,my,True)
                            if bco.ischeck(1-side) and bco.is_mate(1-side):
                                return "CHECKMATE"
                            if not bco.ischeck(side):
                                moves.append([p,mx,my,bco.basic_board_value(side)])
                        else:
                            bco=copy.deepcopy(self)
                            bco.move_p(bco.get_p(p.x,p.y),mx,my,True)
                            if bco.ischeck(1-side) and bco.is_mate(1-side):
                                return "CHECKMATE"
        if not moves:
            return 0
        bv=max([m[3] for m in moves])
        return bv-sbv
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

