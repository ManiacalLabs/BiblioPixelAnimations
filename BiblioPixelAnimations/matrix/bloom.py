from bibliopixel.animation import BaseMatrixAnim
from bibliopixel.util import genVector


class Bloom(BaseMatrixAnim):

    def __init__(self, layout, dir=True):
        super().__init__(layout)
        self._vector = genVector(self.layout.width, self.layout.height)
        self._dir = dir

    def step(self, amt=8):
        if self._dir:
            s = 255 - self._step
        else:
            s = self._step

        # this respects master brightness but is slower
        for y in range(self.layout.height):
            for x in range(self.layout.width):
                index = self._vector[y][x] * 255 / self.layout.height + s
                self.layout.set(x, y, self.palette(index))

        self._step += amt
        if(self._step >= 255):
            self._step = 0
