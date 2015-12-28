from Img import pload


def deduplicate(moves):
    setmoves = set([(mx, my) for mx, my in moves])
    return [[mx, my] for mx, my in setmoves]


def inworld(x, y):
    return 0 <= x < 8 and 0 <= y < 8


def clear(p, x, y):
    return inworld(x, y) and not p[x][y]


def enemy(p, x, y, c):
    return inworld(x, y) and p[x][y] and p[x][y].c != c


def get_jumper_moves(ps, p, jdx, jdy):
    moves = []
    for dx in [-jdx, jdx]:
        for dy in [-jdy, jdy]:
            x = p.x + dx
            y = p.y + dy
            if clear(ps, x, y) or enemy(ps, x, y, p.c) and [x, y] not in moves:
                moves.append([x, y])
    return moves


def get_exact_jumper_moves(ps, p, jumps):
    moves = []
    for dx, dy in jumps:
        x = p.x + dx
        y = p.y + dy
        if clear(ps, x, y) or enemy(ps, x, y, p.c) and [x, y] not in moves:
            moves.append([x, y])
    return moves


def get_all_jumper_moves(ps, p, d1, d2):
    return get_jumper_moves(ps, p, d1, d2) + get_jumper_moves(ps, p, d2, d1)


def get_rider_moves(ps, p, dirs, maxi=7, mode=None):
    moves = []
    for dx, dy in dirs:
        x = p.x + dx
        y = p.y + dy
        n = 0
        while clear(ps, x, y):
            if mode not in ["CAPTURE", "CANNON"]:
                moves.append([x, y])
            x += dx
            y += dy
            n += 1
            if n == maxi:
                break
        if enemy(ps, x, y, p.c) and n != maxi and mode not in ["MOVE", "CANNON"]:
            moves.append([x, y])
        if mode == "CANNON" and inworld(x, y):
            x += dx
            y += dy
            n += 1
            while clear(ps, x, y):
                x += dx
                y += dy
                n += 1
                if n == maxi:
                    break
            if enemy(ps, x, y, p.c) and n != maxi:
                moves.append([x, y])
    return moves


def get_all_rider_moves(ps, p, d1, d2, maxi=7, mode=None):
    return deduplicate(get_rider_moves(ps, p,
                                       [[d1, d2], [d2, d1], [-d1, d2], [-d2, d1], [d1, -d2], [d2, -d1], [-d1, -d2],
                                        [-d2, -d1]], maxi, mode))


class Piece(object):
    imgs = None
    royal = False
    value = 0
    symbol = "Pc"
    desc = "A Piece"

    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.c = c

    def get_img(self):
        return self.imgs[self.c]

    def get_moves(self, p):
        return []

    def place(self, x, y):
        self.x = x
        self.y = y


class Pawn(Piece):
    imgs = pload("Pawn")
    value = 1
    symbol = "Pn"
    desc = "Pawn"

    def get_moves(self, p):
        moves = []
        dy = 1 if self.c else -1
        if clear(p, self.x, self.y + dy):
            moves.append([self.x, self.y + dy])
            if self.y == (1 if self.c else 6):
                if clear(p, self.x, self.y + dy * 2):
                    moves.append([self.x, self.y + dy * 2])
        for dx in [-1, 1]:
            if enemy(p, self.x + dx, self.y + dy, self.c):
                moves.append([self.x + dx, self.y + dy])
        return moves


class Rook(Piece):
    value = 5
    imgs = pload("Rook")
    symbol = "R"
    desc = "Rook"

    def get_moves(self, p):
        return get_all_rider_moves(p, self, 0, 1)


class Knight(Piece):
    imgs = pload("Knight")
    value = 3
    symbol = "N"
    desc = "Knight"

    def get_moves(self, p):
        return get_all_jumper_moves(p, self, 1, 2)


class Bishop(Piece):
    imgs = pload("Bishop")
    value = 3
    symbol = "B"
    desc = "Bishop"

    def get_moves(self, p):
        return get_all_rider_moves(p, self, 1, 1)


class Queen(Piece):
    imgs = pload("Queen")
    value = 9
    symbol = "Q"
    desc = "Queen"

    def get_moves(self, p):
        return get_all_rider_moves(p,self,1,1)+get_all_rider_moves(p,self,0,1)


class King(Piece):
    imgs = pload("King")
    royal = True
    symbol = "K"
    desc = "King"

    def get_moves(self, p):
        return get_all_jumper_moves(p, self, 1, 1) + get_all_jumper_moves(p, self, 0, 1)


class Man(Piece):
    imgs = pload("Man")
    value = 3
    symbol = "Mn"
    desc = "Commoner: Non-royal King"

    def get_moves(self, p):
        return get_all_jumper_moves(p, self, 1, 1) + get_all_jumper_moves(p, self, 0, 1)


class Princess(Piece):
    imgs = pload("Princess")
    value = 8
    symbol = "Ps"
    desc = "Princess: Bishop+Knight"

    def get_moves(self, p):
        return get_all_rider_moves(p, self, 1, 1) + get_all_jumper_moves(p, self, 1, 2)


class Marshal(Piece):
    imgs = pload("Marshal")
    value = 9
    symbol = "Ms"
    desc = "Marshal: Rook+Knight"

    def get_moves(self, p):
        return get_all_rider_moves(p, self, 0, 1) + get_all_jumper_moves(p, self, 1, 2)


class Antibody(Piece):
    imgs = pload("Antibody")
    value = 1
    symbol = "Ab"
    desc = "Antibody: Moves 1 space in the direction of its arms."

    def get_moves(self, p):
        dy = 1 if self.c else -1
        return get_exact_jumper_moves(p, self, [[0, -dy], [1, dy], [-1, dy]])


class Amazon(Piece):
    imgs = pload("Amazon")
    value = 12
    symbol = "Az"
    desc = "Amazon: Queen+Knight"

    def get_moves(self, p):
        return get_all_rider_moves(p,self,1,1)+get_all_rider_moves(p,self,0,1)+get_all_jumper_moves(p, self, 1, 2)


class ShortRook(Piece):
    imgs = pload("ShortRook")
    value = 3
    symbol = "Sr"
    desc = "Short Rook: Moves 4 spaces rookwise"

    def get_moves(self, p):
        return get_rider_moves(p, self, [[0, 1], [0, -1], [1, 0], [-1, 0]], 4)


class MiniRook(Piece):
    imgs = pload("MiniRook")
    value = 2
    symbol = "Mr"
    desc = "Mini Rook: Moves 2 spaces rookwise"

    def get_moves(self, p):
        return get_rider_moves(p, self, [[0, 1], [0, -1], [1, 0], [-1, 0]], 2)


class Circle(Piece):
    imgs = pload("Circle")
    value = 6
    symbol = "Cc"
    desc = "Circle: Knight+Dabbaba"

    def get_moves(self, p):
        return get_all_jumper_moves(p, self, 1, 2) + get_all_jumper_moves(p, self, 0, 2)


class Square(Piece):
    imgs = pload("Square")
    value = 7
    symbol = "Sq"
    desc = "Square: Knight+Afil+Dabbaba"

    def get_moves(self, p):
        return get_all_jumper_moves(p, self, 1, 2) + get_all_jumper_moves(p, self, 0, 2) \
               + get_all_jumper_moves(p, self, 2, 2)


class Rookling(Piece):
    imgs = pload("Rookling")
    symbol = "Rl"
    value = 3
    desc = "Rookling: Moves 2 spaces rookwise and can jump."

    def get_moves(self, p):
        return get_all_jumper_moves(p, self, 0, 1) + get_all_jumper_moves(p, self, 0, 2)


class NightRider(Piece):
    imgs = pload("NightRider")
    symbol = "Nr"
    value = 5
    desc = "Nightrider: Moves repeatedly like a knight"

    def get_moves(self, p):
        return get_all_rider_moves(p, self, 1,2)


class BishopX(Piece):
    imgs = pload("BishopX")
    symbol = "BX"
    value = 5.5
    desc = "Bishop X: Bishop that can move 1 space orthogonally."

    def get_moves(self, p):
        return get_all_rider_moves(p, self, 1, 1) + get_all_jumper_moves(p, self, 0, 1)


class RookX(Piece):
    imgs = pload("RookX")
    symbol = "RX"
    value = 6.5
    desc = "Rook X: Rook that can move 1 space diagonally"

    def get_moves(self, p):
        return get_all_rider_moves(p, self, 0, 1) + get_all_jumper_moves(p, self, 1, 1)


from Piece2 import *

pieces = [Rook, RookX, ShortRook, Rookling, MiniRook, Knight, NightRider, Bishop, BishopX, Queen, Marshal, Princess,
          Amazon, King, Man, Antibody, Circle, Square, Window, SquareX, Ghost, Crab, ShortBishop, WideGuard,
          NarrowGuard, Mimic, Star, Star2, Cannon,KnCross]
