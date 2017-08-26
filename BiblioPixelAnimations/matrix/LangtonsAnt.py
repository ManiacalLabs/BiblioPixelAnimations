from bibliopixel.animation import BaseMatrixAnim
from bibliopixel import colors
import random


class LangtonsAntBase(BaseMatrixAnim):

    def __init__(self, layout, antColor=colors.Green, pathColor=colors.Red):
        super().__init__(layout)
        self.antColor = tuple(antColor)
        self.pathColor = tuple(pathColor)
        self.offColor = colors.Off
        self.curColor = self.offColor

    def pre_run(self):
        self.x = random.randrange(self.width)
        self.y = random.randrange(self.height)
        self.d = random.randrange(4)

    def _rollValue(self, val, step, min, max):
        val += step
        if val < min:
            diff = min - val
            val = max - diff + 1
        elif val > max:
            diff = val - max
            val = min + diff - 1
        return val

    def _changeDelta(self, delta):
        self.d = self._rollValue(self.d, delta, 0, 3)

    def _moveAnt(self):
        if self.d == 0:
            self.y = self._rollValue(self.y, 1, 0, self.height - 1)
        elif self.d == 1:
            self.x = self._rollValue(self.x, 1, 0, self.width - 1)
        elif self.d == 2:
            self.y = self._rollValue(self.y, -1, 0, self.height - 1)
        elif self.d == 3:
            self.x = self._rollValue(self.x, -1, 0, self.width - 1)

        self.curColor = self.layout.get(self.x, self.y)
        self._postMove()


class LangtonsAnt(LangtonsAntBase):
    def _postMove(self):
        self.layout.set(self.x, self.y, self.antColor)

    def step(self, amt=1):
        if self.curColor == self.pathColor:
            self.layout.set(self.x, self.y, self.offColor)
            self._changeDelta(-1)
            self._moveAnt()
        else:
            self.layout.set(self.x, self.y, self.pathColor)
            self._changeDelta(1)
            self._moveAnt()


class LangtonsAntRainbow(LangtonsAntBase):
    DEFAULT_COLORS = [colors.Red, colors.Orange, colors.Yellow,
                      colors.Green, colors.Blue, colors.Violet]

    def __init__(self, layout, antColor=colors.White, colors=None):
        super().__init__(layout, antColor)
        self.colors = colors or self.DEFAULT_COLORS
        self.curColorIndex = -1

    def _postMove(self):
        if self.curColor == self.offColor:
            i = 0
        else:
            i = self.colors.index(self.curColor)
            i += 1
            i %= len(self.colors)

        self.curColor = self.colors[i]
        self.curColorIndex = i
        self.layout.set(self.x, self.y, self.antColor)

    def step(self, amt=1):
        self.layout.set(self.x, self.y, self.curColor)
        if self.curColorIndex % 2 == 0:
            self._changeDelta(-1)
            self._moveAnt()
        else:
            self._changeDelta(1)
            self._moveAnt()
