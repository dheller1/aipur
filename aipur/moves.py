import enum


class MoveType(enum.Enum):
    DrawSingle = 1
    DrawMultiple = 2
    DrawAllCamels = 3
    Discard = 4


class Move:
    def __init__(self, typ, draw=None, replace=None, discard=None):
        self.typ = typ
        self.draw = draw
        self.replace = replace
        self.discard = discard

    @classmethod
    def draw_single(cls, which):
        return Move(MoveType.DrawSingle, draw=which)

    @classmethod
    def draw_multiple(cls, which, replace):
        return Move(MoveType.DrawMultiple, draw=which, replace=replace)

    @classmethod
    def draw_all_camels(cls):
        return Move(MoveType.DrawAllCamels)

    @classmethod
    def discard(cls, which):
        return Move(MoveType.Discard, discard=which)
