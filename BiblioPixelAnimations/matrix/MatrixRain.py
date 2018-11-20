from bibliopixel.animation.matrix import Matrix
from bibliopixel.colors.arithmetic import color_scale
import random


class MatrixRain(Matrix):
    COLOR_DEFAULTS = ('palette', 'green'),

    def __init__(self, layout, tail=4, growthRate=4, **kwds):
        super().__init__(layout, **kwds)
        self._tail = tail
        self._growthRate = growthRate

    def pre_run(self):
        self._drops = [[] for x in range(self.width)]

    def _drawDrop(self, x, y, color):
        for i in range(self._tail):
            if y - i >= 0 and y - i < self.height:
                level = 255 - ((255 // self._tail) * i)
                self.layout.set(x, y - i, color_scale(color, level))

    def step(self, amt=1):
        self.layout.all_off()

        for i in range(self._growthRate):
            newDrop = random.randint(0, self.width - 1)
            self._drops[newDrop].append((0, random.choice(self.palette)))

        for x in range(self.width):
            col = self._drops[x]
            if len(col) > 0:
                removals = []
                for y in range(len(col)):
                    drop = col[y]
                    if drop[0] < self.height:
                        self._drawDrop(x, drop[0], drop[1])
                    if drop[0] - (self._tail - 1) < self.height:
                        drop = (drop[0] + 1, drop[1])
                        self._drops[x][y] = drop
                    else:
                        removals.append(drop)
                for r in removals:
                    self._drops[x].remove(r)


class MatrixRainBow(Matrix):

    def __init__(self, layout, tail=4, growthRate=4, **kwds):
        super().__init__(layout, **kwds)
        self._tail = tail
        self._growthRate = growthRate

    def pre_run(self):
        self._drops = [[] for x in range(self.width)]

    def _drawDrop(self, x, y, color):
        for i in range(self._tail):
            if y - i >= 0 and y - i < self.height:
                level = 255 - ((255 // self._tail) * i)
                self.layout.set(x, y - i, color_scale(color, level))

    def step(self, amt=1):
        self.layout.all_off()

        for i in range(self._growthRate):
            newDrop = random.randint(0, self.width - 1)
            self._drops[newDrop].append(0)

        for x in range(self.width):
            col = self._drops[x]
            if len(col) > 0:
                removals = []
                for y in range(len(col)):
                    drop = col[y]
                    if drop < self.height:
                        self._drawDrop(x, drop, self.palette(
                            drop * (255 // self.height)))
                    if drop - (self._tail - 1) < self.height:
                        drop = drop + 1
                        self._drops[x][y] = drop
                    else:
                        removals.append(drop)
                for r in removals:
                    self._drops[x].remove(r)
