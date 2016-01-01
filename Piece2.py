from Piece import Piece, get_all_jumper_moves, get_exact_jumper_moves, get_rider_moves, get_jumper_moves, clear, \
    inworld, get_all_rider_moves
from Img import pload


class Ghost(Piece):
    imgs = pload("Ghost")
    symbol = "Gh"
    value = 0.5
    desc = "Ghost: Can move anywhere, but not capture."

    def get_moves(self, p):
        moves = []
        for x in range(8):
            for y in range(8):
                if clear(p, x, y):
                    moves.append([x, y])
        return moves


class Crab(Piece):
    imgs = pload("Crab")
    symbol = "Cr"
    value = 1.5
    desc = "Crab: Narrow Knight forwards, Wide Knight backwards."

    def get_moves(self, p):
        if self.c:
            return get_exact_jumper_moves(p, self, [[1, 2], [-1, 2], [2, -1], [-2, -1]])
        else:
            return get_exact_jumper_moves(p, self, [[1, -2], [-1, -2], [2, 1], [-2, 1]])


class ShortBishop(Piece):
    imgs = pload("ShortBishop")
    symbol = "SB"
    value = 2
    desc = "Short Bishop: Moves up to 4 spaces diagonally"

    def get_moves(self, p):
        return get_all_rider_moves(p, self, 1, 1, 4)


class WideGuard(Piece):
    imgs = pload("WideGuard")
    value = 3.5
    desc = "Wide Guard: Moves like a rook, but can only move 1 space vertically."
    symbol = "Wg"

    def get_moves(self, p):
        return get_rider_moves(p, self, [[1, 0], [-1, 0]]) + get_jumper_moves(p, self, 0, 1)


class NarrowGuard(Piece):
    imgs = pload("NarrowGuard")
    value = 3.5
    desc = "Narrow Guard: Moves like a rook, but can only move 1 space horizontally."
    symbol = "Ng"

    def get_moves(self, p):
        return get_rider_moves(p, self, [[0, 1], [0, -1]]) + get_jumper_moves(p, self, 1, 0)


class Mimic(Piece):
    imgs = pload("Mimic")
    value = 4
    desc = "Mimic: Can move like any piece next to it"
    symbol = "Mi"
    used = False

    def get_moves(self, p):
        moves = []
        for dx, dy in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            tx = self.x + dx
            ty = self.y + dy
            if inworld(tx, ty) and p[tx][ty]:
                mp = p[tx][ty]
                if mp.symbol != "Mi":
                    mp.x = self.x
                    mp.y = self.y
                    moves.extend(mp.get_moves(p))
                    mp.x = tx
                    mp.y = ty
        return moves


class Window(Piece):
    imgs = pload("Window")
    value = 8.5
    symbol = "Wd"
    desc = "Window: Knight+Afil+Dabbaba+Wazir"

    def get_moves(self, p):
        return get_all_jumper_moves(p, self, 1, 2) + get_all_jumper_moves(p, self, 0, 2) + \
               get_all_jumper_moves(p, self, 2, 2) + get_all_jumper_moves(p, self, 0, 1)


class SquareX(Piece):
    imgs = pload("SquareX")
    value = 10
    symbol = "SqX"
    desc = "SquareX: Knight+Afil+Dabbaba+King"

    def get_moves(self, p):
        return get_all_jumper_moves(p, self, 1, 2) + get_all_jumper_moves(p, self, 0, 2) + \
               get_all_jumper_moves(p, self, 2, 2) + get_all_jumper_moves(p, self, 0, 1) + \
               get_all_jumper_moves(p, self, 1, 1)


class Star(Piece):
    imgs = pload("Star")
    value = 4
    symbol = "St"
    desc = "Star: Moves like Rook, Captures like Bishop"

    def get_moves(self, p):
        return get_all_rider_moves(p, self, 1, 1, mode="CAPTURE") + get_all_rider_moves(p, self, 0,1, mode="MOVE")
class Star2(Piece):
    imgs = pload("Star2")
    value = 4
    symbol = "St2"
    desc = "Star 2: Moves like Bishop, Captures like Rook"

    def get_moves(self, p):
        return get_all_rider_moves(p, self, 0, 1, mode="CAPTURE") + get_all_rider_moves(p, self, 1,1, mode="MOVE")


class Cannon(Piece):
    imgs = pload("Cannon")
    value = 5
    symbol = "Cn"
    desc = "Cannon: Moves like Rook, Captures by jumping exactly one piece."

    def get_moves(self, p):
        return get_all_rider_moves(p, self, 0, 1, mode="MOVE") + get_all_rider_moves(p, self, 0, 1, mode="CANNON")
class KnCross(Piece):
    imgs=pload("Cross")
    value = 4
    symbol = "KnC"
    desc = "Knight's Cross: Wazir+sideways Nightrider"

    def get_moves(self, p):
        return get_rider_moves(p,self,[[2,1],[-2,1],[2,-1],[-2,-1]])+get_all_jumper_moves(p,self,0,1)

class Ferz(Piece):
    imgs=pload("Ferz")
    value=1.5
    symbol = "F"
    desc = "Ferz: 1-step Bishop"

    def get_moves(self, p):
        return get_all_jumper_moves(p,self,1,1)

class Wazir(Piece):
    imgs = pload("Wazir")
    value = 1
    symbol = "W"
    desc = "Wazir: 1-step Rook"

    def get_moves(self, p):
        return get_all_jumper_moves(p,self,0,1)

class Elephant(Piece):
    imgs=pload("Elephant")
    value=2.5
    symbol = "E"
    desc = "Elephant: Afil+Ferz"

    def get_moves(self, p):
        return get_all_jumper_moves(p,self,1,1)+get_all_jumper_moves(p,self,2,2)
class Sheep(Piece):
    imgs = pload("Sheep")
    value=4
    symbol = "Sh"
    desc = "Sheep: Bishop+Afilrider (BAA)"
    def get_moves(self, p):
        return get_all_rider_moves(p,self,1,1)+get_all_rider_moves(p,self,2,2)