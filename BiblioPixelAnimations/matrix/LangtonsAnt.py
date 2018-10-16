from bibliopixel.animation import BaseMatrixAnim
from bibliopixel import colors
import random


class LangtonsAntBase(BaseMatrixAnim):
    COLOR_DEFAULTS = (
        ('offColor', colors.Off),
        ('antColor', colors.Green),
        ('pathColor', colors.Red)
    )

    def __init__(self, layout, **kwds):
        super().__init__(layout, **kwds)
        self.curColor = self.palette.get(0)

    def pre_run(self):
        self.x = random.randrange(self.width)
        self.y = random.randrange(self.height)
        self.d = random.randrange(4)

    def _moveAnt(self, delta):
        def roll(val, step, min, max):
            val += step
            if val < min:
                diff = min - val
                val = max - diff + 1
            elif val > max:
                diff = val - max
                val = min + diff - 1
            return val

        self.d = roll(self.d, delta, 0, 3)
        if self.d == 0:
            self.y = roll(self.y, 1, 0, self.height - 1)
        elif self.d == 1:
            self.x = roll(self.x, 1, 0, self.width - 1)
        elif self.d == 2:
            self.y = roll(self.y, -1, 0, self.height - 1)
        elif self.d == 3:
            self.x = roll(self.x, -1, 0, self.width - 1)

        self.curColor = tuple(int(c) for c in self.layout.get(self.x, self.y))
        self._postMove()


class LangtonsAnt(LangtonsAntBase):
    def _postMove(self):
        self.layout.set(self.x, self.y, self.palette.get(1))

    def step(self, amt=1):
        if self.curColor == self.pathColor:
            self.layout.set(self.x, self.y, self.palette.get(0))
            self._moveAnt(-1)
        else:
            self.layout.set(self.x, self.y, self.palette.get(2))
            self._moveAnt(1)


class LangtonsAntRainbow(LangtonsAntBase):
    DEFAULT_COLORS = [colors.Red, colors.Orange, colors.Yellow,
                      colors.Green, colors.Blue, colors.Violet]

    def __init__(self, layout, colors=None, **kwds):
        super().__init__(layout, **kwds)
        self.colors = colors or self.DEFAULT_COLORS
        self.curColorIndex = -1

    def _postMove(self):
        if self.curColor == self.palette.get(0):
            i = 0
        else:
            i = self.colors.index(self.curColor)
            i += 1
            i %= len(self.colors)

        self.curColor = self.colors[i]
        self.curColorIndex = i
        self.layout.set(self.x, self.y, self.palette.get(1))

    def step(self, amt=1):
        self.layout.set(self.x, self.y, self.curColor)
        if self.curColorIndex % 2 == 0:
            self._moveAnt(-1)
        else:
            self._moveAnt(1)
