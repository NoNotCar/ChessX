from Img import pload


def inworld(x, y):
    return 0 <= x < 8 and 0 <= y < 8


def clear(p, x, y):
    return inworld(x, y) and not p[x][y]


def piece(p, x, y, c):
    return inworld(x, y) and p[x][y]


def get_jumper_moves(ps, p, jdx, jdy):
    moves = []
    for dx in [-jdx, jdx]:
        for dy in [-jdy, jdy]:
            x = p.x + dx
            y = p.y + dy
            if clear(ps, x, y) or piece(ps, x, y, p.c) and [x, y] not in moves:
                moves.append([x, y])
    return moves


def get_exact_jumper_moves(ps, p, jumps):
    moves = []
    for dx, dy in jumps:
        x = p.x + dx
        y = p.y + dy
        if clear(ps, x, y) or piece(ps, x, y, p.c) and [x, y] not in moves:
            moves.append([x, y])
    return moves


def get_all_jumper_moves(ps, p, d1, d2):
    return get_jumper_moves(ps, p, d1, d2) + get_jumper_moves(ps, p, d2, d1)


def get_rider_moves(ps, p, dirs, maxi=7, mini=0, mode=None):
    moves = []
    for dx, dy in dirs:
        x = p.x + dx
        y = p.y + dy
        n = 0
        while clear(ps, x, y):
            if mode not in ["CAPTURE", "CANNON"] and n >= mini:
                moves.append([x, y])
            x += dx
            y += dy
            n += 1
            if n == maxi:
                break
        if piece(ps, x, y, p.c) and n != maxi and n >= mini and mode not in ["MOVE", "CANNON"]:
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
            if piece(ps, x, y, p.c) and n != maxi:
                moves.append([x, y])
    return moves


def get_all_rider_moves(ps, p, d1, d2, maxi=7, mini=0, mode=None):
    return get_rider_moves(ps, p,
                           [[d1, d2], [d2, d1], [-d1, d2], [-d2, d1], [d1, -d2], [d2, -d1], [-d1, -d2], [-d2, -d1]]
                           , maxi, mini, mode)


class Piece(object):
    royal = False
    value = 0
    symbol = "Pc"
    desc = "A Piece"

    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.c = c
        self.__class__.set_imgs()

    @classmethod
    def set_imgs(cls):
        cls.imgs = pload(cls.__name__) if cls.__name__!="Piece" else None
    def get_img(self):
        return self.imgs[self.c]

    def get_moves(self, p):
        return []

    def place(self, x, y):
        self.x = x
        self.y = y

    def onmove(self, p):
        pass


class Pawn(Piece):
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
            if piece(p, self.x + dx, self.y + dy, self.c):
                moves.append([self.x + dx, self.y + dy])
        return moves

    def onmove(self, p):
        if self.c:
            if self.y == 7:
                p[self.x][self.y] = Queen(self.x, self.y, 1)
        else:
            if self.y == 0:
                p[self.x][self.y] = Queen(self.x, self.y, 0)


class Rook(Piece):
    value = 5
    symbol = "R"
    desc = "Rook"

    def get_moves(self, p):
        return get_all_rider_moves(p, self, 0, 1)


class Knight(Piece):
    value = 3
    symbol = "N"
    desc = "Knight"

    def get_moves(self, p):
        return get_all_jumper_moves(p, self, 1, 2)


class Bishop(Piece):
    value = 3
    symbol = "B"
    desc = "Bishop"

    def get_moves(self, p):
        return get_all_rider_moves(p, self, 1, 1)


class Queen(Piece):
    value = 9
    symbol = "Q"
    desc = "Queen"

    def get_moves(self, p):
        return get_all_rider_moves(p, self, 1, 1) + get_all_rider_moves(p, self, 0, 1)


class King(Piece):
    royal = True
    symbol = "K"
    desc = "King"

    def get_moves(self, p):
        return get_all_jumper_moves(p, self, 1, 1) + get_all_jumper_moves(p, self, 0, 1)


class Man(Piece):
    value = 3
    symbol = "Mn"
    desc = "Commoner: Non-royal King"

    def get_moves(self, p):
        return get_all_jumper_moves(p, self, 1, 1) + get_all_jumper_moves(p, self, 0, 1)


class Princess(Piece):
    value = 8
    symbol = "Ps"
    desc = "Princess: Bishop+Knight"

    def get_moves(self, p):
        return get_all_rider_moves(p, self, 1, 1) + get_all_jumper_moves(p, self, 1, 2)


class Marshal(Piece):
    value = 9
    symbol = "Ms"
    desc = "Marshal: Rook+Knight"

    def get_moves(self, p):
        return get_all_rider_moves(p, self, 0, 1) + get_all_jumper_moves(p, self, 1, 2)


class Antibody(Piece):
    value = 1
    symbol = "Ab"
    desc = "Antibody: Moves 1 space in the direction of its arms."

    def get_moves(self, p):
        dy = 1 if self.c else -1
        return get_exact_jumper_moves(p, self, [[0, -dy], [1, dy], [-1, dy]])


class Amazon(Piece):
    value = 12
    symbol = "Az"
    desc = "Amazon: Queen+Knight"

    def get_moves(self, p):
        return get_all_rider_moves(p, self, 1, 1) + get_all_rider_moves(p, self, 0, 1) + get_all_jumper_moves(p, self,
                                                                                                              1, 2)


class ShortRook(Piece):
    value = 3
    symbol = "Sr"
    desc = "Short Rook: Moves 4 spaces rookwise"

    def get_moves(self, p):
        return get_rider_moves(p, self, [[0, 1], [0, -1], [1, 0], [-1, 0]], 4)


class MiniRook(Piece):
    value = 2
    symbol = "Mr"
    desc = "Mini Rook: Moves 2 spaces rookwise"

    def get_moves(self, p):
        return get_rider_moves(p, self, [[0, 1], [0, -1], [1, 0], [-1, 0]], 2)


class Circle(Piece):
    value = 6
    symbol = "Cc"
    desc = "Circle: Knight+Dabbaba"

    def get_moves(self, p):
        return get_all_jumper_moves(p, self, 1, 2) + get_all_jumper_moves(p, self, 0, 2)


class Square(Piece):
    value = 7
    symbol = "Sq"
    desc = "Square: Knight+Alfil+Dabbaba"

    def get_moves(self, p):
        return get_all_jumper_moves(p, self, 1, 2) + get_all_jumper_moves(p, self, 0, 2) \
               + get_all_jumper_moves(p, self, 2, 2)


class Rookling(Piece):
    symbol = "Rl"
    value = 3
    desc = "Rookling: Moves 2 spaces rookwise and can jump."

    def get_moves(self, p):
        return get_all_jumper_moves(p, self, 0, 1) + get_all_jumper_moves(p, self, 0, 2)


class NightRider(Piece):
    symbol = "Nr"
    value = 5
    desc = "Nightrider: Moves repeatedly like a knight"

    def get_moves(self, p):
        return get_all_rider_moves(p, self, 1, 2)


class BishopX(Piece):
    symbol = "BX"
    value = 5.5
    desc = "Bishop X: Bishop that can move 1 space orthogonally."

    def get_moves(self, p):
        return get_all_rider_moves(p, self, 1, 1) + get_all_jumper_moves(p, self, 0, 1)


class RookX(Piece):
    symbol = "RX"
    value = 6.5
    desc = "Rook X: Rook that can move 1 space diagonally"

    def get_moves(self, p):
        return get_all_rider_moves(p, self, 0, 1) + get_all_jumper_moves(p, self, 1, 1)

class Null(Piece):
    symbol = "No"
    value = 0
    desc = "An Empty Square"



from Piece2 import *

pieces = [Rook, RookX, ShortRook, Rookling, RooklingX, MiniRook, Knight, NightRider, Bishop, BishopX, Queen, Marshal,
          Princess, Amazon, King, Man, Antibody, Circle, Square, Window, SquareX, Ghost, Crab, ShortBishop, WideGuard,
          NarrowGuard, Mimic, Star, Star2, Cannon, KnCross, Ferz, Wazir, Elephant, Sheep, Penguin, Dabbaba, Bede, Null]
for p in pieces:
    p.set_imgs()
