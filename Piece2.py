from Piece import Piece, get_all_jumper_moves, get_exact_jumper_moves, get_rider_moves, get_jumper_moves, clear, \
    inworld, get_all_rider_moves
from Img import pload


class Ghost(Piece):
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
    symbol = "Cr"
    value = 1.5
    desc = "Crab: Narrow Knight forwards, Wide Knight backwards."

    def get_moves(self, p):
        if self.c:
            return get_exact_jumper_moves(p, self, [[1, 2], [-1, 2], [2, -1], [-2, -1]])
        else:
            return get_exact_jumper_moves(p, self, [[1, -2], [-1, -2], [2, 1], [-2, 1]])


class ShortBishop(Piece):
    symbol = "SB"
    value = 2
    desc = "Short Bishop: Moves up to 4 spaces diagonally"

    def get_moves(self, p):
        return get_all_rider_moves(p, self, 1, 1, 4)


class WideGuard(Piece):
    value = 3.5
    desc = "Wide Guard: Moves like a rook, but can only move 1 space vertically."
    symbol = "Wg"

    def get_moves(self, p):
        return get_rider_moves(p, self, [[1, 0], [-1, 0]]) + get_jumper_moves(p, self, 0, 1)


class NarrowGuard(Piece):
    value = 3.5
    desc = "Narrow Guard: Moves like a rook, but can only move 1 space horizontally."
    symbol = "Ng"

    def get_moves(self, p):
        return get_rider_moves(p, self, [[0, 1], [0, -1]]) + get_jumper_moves(p, self, 1, 0)


class Mimic(Piece):
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
    value = 8.5
    symbol = "Wd"
    desc = "Window: Knight+Alfil+Dabbaba+Wazir"

    def get_moves(self, p):
        return get_all_jumper_moves(p, self, 1, 2) + get_all_jumper_moves(p, self, 0, 2) + \
               get_all_jumper_moves(p, self, 2, 2) + get_all_jumper_moves(p, self, 0, 1)


class SquareX(Piece):
    value = 10
    symbol = "SqX"
    desc = "SquareX: Knight+Alfil+Dabbaba+King"

    def get_moves(self, p):
        return get_all_jumper_moves(p, self, 1, 2) + get_all_jumper_moves(p, self, 0, 2) + \
               get_all_jumper_moves(p, self, 2, 2) + get_all_jumper_moves(p, self, 0, 1) + \
               get_all_jumper_moves(p, self, 1, 1)


class Star(Piece):
    value = 4
    symbol = "St"
    desc = "Star: Moves like Rook, Captures like Bishop"

    def get_moves(self, p):
        return get_all_rider_moves(p, self, 1, 1, mode="CAPTURE") + get_all_rider_moves(p, self, 0, 1, mode="MOVE")


class Star2(Piece):
    value = 4
    symbol = "St2"
    desc = "Star 2: Moves like Bishop, Captures like Rook"

    def get_moves(self, p):
        return get_all_rider_moves(p, self, 0, 1, mode="CAPTURE") + get_all_rider_moves(p, self, 1, 1, mode="MOVE")


class Cannon(Piece):
    value = 5
    symbol = "Cn"
    desc = "Cannon: Moves like Rook, Captures by jumping exactly one piece."

    def get_moves(self, p):
        return get_all_rider_moves(p, self, 0, 1, mode="MOVE") + get_all_rider_moves(p, self, 0, 1, mode="CANNON")


class KnCross(Piece):
    value = 4
    symbol = "KnC"
    desc = "Knight's Cross: Wazir+sideways Nightrider"

    def get_moves(self, p):
        return get_rider_moves(p, self, [[2, 1], [-2, 1], [2, -1], [-2, -1]]) + get_all_jumper_moves(p, self, 0, 1)


class Ferz(Piece):
    value = 1.5
    symbol = "F"
    desc = "Ferz: 1-step Bishop"

    def get_moves(self, p):
        return get_all_jumper_moves(p, self, 1, 1)


class Wazir(Piece):
    value = 1
    symbol = "W"
    desc = "Wazir: 1-step Rook"

    def get_moves(self, p):
        return get_all_jumper_moves(p, self, 0, 1)


class Elephant(Piece):
    value = 2.5
    symbol = "E"
    desc = "Elephant: Alfil+Ferz"

    def get_moves(self, p):
        return get_all_jumper_moves(p, self, 1, 1) + get_all_jumper_moves(p, self, 2, 2)


class Sheep(Piece):
    value = 4
    symbol = "Sh"
    desc = "Sheep: Bishop+Alfilrider (BAA)"

    def get_moves(self, p):
        return get_all_rider_moves(p, self, 1, 1) + get_all_rider_moves(p, self, 2, 2)


class Penguin(Piece):
    value = 2
    symbol = "Pg"
    desc = "Penguin: Moves 2-3 spaces like a rook"

    def get_moves(self, p):
        return get_all_rider_moves(p, self, 0, 1, 3, 1)


class Dabbaba(Piece):
    value = 1
    symbol = "D"
    desc = "Dabbaba: Jumps 2 spaces orthogonally"

    def get_moves(self, p):
        return get_all_jumper_moves(p, self, 0, 2)


class Bede(Piece):
    value = 5
    symbol = "Be"
    desc = "Bede: Bishop+Dabbaba"

    def get_moves(self, p):
        return get_all_jumper_moves(p, self, 0, 2) + get_all_rider_moves(p, self, 1, 1)


class RooklingX(Piece):
    value = 5
    symbol = "RlX"
    desc = "Rookling X: Can leap up to 3 spaces like a Rook"

    def get_moves(self, p):
        return get_all_jumper_moves(p, self, 0, 1) + get_all_jumper_moves(p, self, 0, 2) + get_all_jumper_moves(p, self,
                                                                                                                0, 3)
