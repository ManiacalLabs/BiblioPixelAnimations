from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors
import random


class MatrixRain(BaseMatrixAnim):
    def __init__(self, layout, colors=[colors.Green], tail=4, growthRate=4):
        super(MatrixRain, self).__init__(layout)
        self._colors = colors
        self._tail = tail
        self._growthRate = growthRate

    def pre_run(self):
        self._drops = [[] for x in range(self.layout.width)]

    def _drawDrop(self, x, y, color):
        for i in range(self._tail):
            if y - i >= 0 and y - i < self.layout.height:
                level = 255 - ((255 // self._tail) * i)
                self.layout.set(x, y - i, colors.color_scale(color, level))

    def step(self, amt=1):
        self.layout.all_off()

        for i in range(self._growthRate):
            newDrop = random.randint(0, self.layout.width - 1)
            cInt = random.randint(0, len(self._colors) - 1)
            self._drops[newDrop].append((0, self._colors[cInt]))

        for x in range(self.layout.width):
            col = self._drops[x]
            if len(col) > 0:
                removals = []
                for y in range(len(col)):
                    drop = col[y]
                    if drop[0] < self.layout.height:
                        self._drawDrop(x, drop[0], drop[1])
                    if drop[0] - (self._tail - 1) < self.layout.height:
                        drop = (drop[0] + 1, drop[1])
                        self._drops[x][y] = drop
                    else:
                        removals.append(drop)
                for r in removals:
                    self._drops[x].remove(r)

        self._step = 0


class MatrixRainBow(BaseMatrixAnim):

    def __init__(self, layout, tail=4, growthRate=4):
        super(MatrixRainBow, self).__init__(layout)
        self._tail = tail
        self._growthRate = growthRate

    def pre_run(self):
        self._drops = [[] for x in range(self.layout.width)]

    def _drawDrop(self, x, y, color):
        for i in range(self._tail):
            if y - i >= 0 and y - i < self.layout.height:
                level = 255 - ((255 // self._tail) * i)
                self.layout.set(x, y - i, colors.color_scale(color, level))

    def step(self, amt=1):
        self.layout.all_off()

        for i in range(self._growthRate):
            newDrop = random.randint(0, self.layout.width - 1)
            self._drops[newDrop].append(0)

        for x in range(self.layout.width):
            col = self._drops[x]
            if len(col) > 0:
                removals = []
                for y in range(len(col)):
                    drop = col[y]
                    if drop < self.layout.height:
                        self._drawDrop(x, drop, colors.hue2rgb(
                            drop * (255 // self.layout.height)))
                    if drop - (self._tail - 1) < self.layout.height:
                        drop = drop + 1
                        self._drops[x][y] = drop
                    else:
                        removals.append(drop)
                for r in removals:
                    self._drops[x].remove(r)

        self._step = 0
