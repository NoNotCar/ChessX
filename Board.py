import copy
from operator import itemgetter
import pygame
def deduplicate(moves):
    setmoves = set([(mx, my) for mx, my in moves])
    return [[mx, my] for mx, my in setmoves]
class Board(object):
    def __init__(self):
        self.p=[]
        for _ in range(8):
            self.p.append([None]*8)
        self.turn=0
        self.positions=[]
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
                p.onmove(self.p)
                self.positions.append([[p.symbol if p else "" for p in row] for row in self.p])
                return True
            return False
        else:
            self.p[tx][ty]=p
            self.p[p.x][p.y]=None
            p.place(tx,ty)
            p.onmove(self.p)

    def ischeck(self,side):
        royalps=[]
        for row in self.p:
            for p in row:
                if p and p.c==side and p.royal:
                    royalps.append([p.x,p.y])
        for row in self.p:
            for p in row:
                if p and p.c==1-side and [pos for pos in self.get_moves(p)[0] if pos in royalps]:
                    return True
        return False
    def boardvalue(self,side):
        dbv=self.get_delta_board_value(1-side)
        if dbv=="CHECKMATE":
            return -1000
        return sum(p.value for p in self.gen_ps(side))-sum(p.value for p in self.gen_ps(1-side))-dbv
    def basic_board_value(self,side):
        return sum(p.value for p in self.gen_ps(side))-sum(p.value for p in self.gen_ps(1-side))
    def developement_value(self,side):
        ek=[p for p in self.gen_ps(1-side) if p.royal][0]
        return sum([self.dist(p,ek) for p in self.gen_ps(side)])
    def dist(self,p1,p2):
        return abs(p1.x-p2.x)+abs(p1.y-p2.y)
    def get_best_moves(self,side):
        moves=[[],[],[]]
        startvalue=self.basic_board_value(side)
        for row in self.p:
            for p in row:
                if p and p.c==side:
                    pygame.event.pump()
                    for mx,my in self.get_moves(p)[0]:
                        bco=copy.deepcopy(self)
                        bco.move_p(bco.get_p(p.x,p.y),mx,my,True)
                        if bco.ischeck(1-side) and bco.is_mate(1-side):
                            return [[p,mx,my]]
                        if not bco.ischeck(side):
                            bbv=bco.basic_board_value(side)
                            if bco.is_stalemate():
                                moves[2].append([p,mx,my,-500,bco.developement_value(side),bco])
                            else:
                                moves[0 if bbv>startvalue else 1].append([p,mx,my,bbv,bco.developement_value(side),bco])
        for amove in sorted(moves[0],key=itemgetter(3)):
            pygame.event.pump()
            bv=amove[5].boardvalue(side)
            if bv>=amove[3]:
                return [amove[:3]]
            elif startvalue<bv:
                if len(moves)==3:
                    moves=[[]]
                amove[3]=bv
                moves[0].append(amove[:5])
            else:
                amove[3]=bv
                moves[2].append(amove)
        if len(moves)==3:
            for zmove in moves[1]:
                pygame.event.pump()
                bv=zmove[5].boardvalue(side)
                if bv>zmove[3]:
                    return [zmove[:3]]
                elif bv==zmove[3]:
                    if len(moves)==3:
                        moves=[[]]
                    zmove[3]=bv
                    moves[0].append(zmove[:5])
                else:
                    zmove[3]=bv
        if len(moves)==3:
            smoves=moves[2]
            moves=moves[1]
            if not len(moves):
                return [sm[:3] for sm in smoves]
        else:
            moves=moves[0]
        bv=max([m[3] for m in moves])
        bvs=[m[:3]+[m[4]] for m in moves if m[3]==bv]
        bd=min([m[3] for m in bvs])
        return [m[:3] for m in bvs if m[3]==bd]
    def get_delta_board_value(self,side):
        sbv=self.basic_board_value(side)
        moves=[]
        defmoves=self.get_edmoves(1-side)
        for p in self.gen_ps(side):
            for mx,my in self.get_moves(p)[0]:
                if self.p[mx][my]:
                    bco=copy.deepcopy(self)
                    bco.move_p(bco.get_p(p.x,p.y),mx,my,True)
                    if bco.ischeck(1-side) and bco.is_mate(1-side):
                        return "CHECKMATE"
                    if not bco.ischeck(side):
                        if [mx,my] in defmoves:
                            moves.append([p,mx,my,bco.basic_board_value(side)-p.value])
                        else:
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
                    for mx,my in self.get_moves(p)[0]:
                        bco=copy.deepcopy(self)
                        bco.move_p(bco.get_p(p.x,p.y),mx,my,True)
                        if not bco.ischeck(side):
                            return False
        return True
    def is_stalemate(self):
        uniquepos=[]
        doublepos=[]
        for pos in self.positions:
            if pos not in uniquepos:
                uniquepos.append(pos)
            elif pos not in doublepos:
                doublepos.append(pos)
            else:
                return True
        return False

    def get_moves(self,p):
        moves=[]
        defmoves=[]
        for mx,my in deduplicate(p.get_moves(self.p)):
            mp=self.get_p(mx,my)
            if mp and mp.c==p.c:
                defmoves.append([mx,my])
            else:
                moves.append([mx,my])
        return moves,defmoves
    def get_edmoves(self,side):
        edmoves=[]
        for p in self.gen_ps(side):
            edmoves.extend(self.get_moves(p)[1])
        return deduplicate(edmoves)



    def gen_ps(self,side=None):
        for row in self.p:
            for p in row:
                if p and (side is None or p.c==side):
                    yield p

