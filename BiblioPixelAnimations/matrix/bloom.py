from bibliopixel.animation.matrix import Matrix
from bibliopixel.util.util import genVector


class Bloom(Matrix):

    def __init__(self, layout, dir=True, **kwds):
        super().__init__(layout, **kwds)
        self._vector = genVector(self.width, self.height)
        self._dir = dir

    def pre_run(self):
        self._step = 0

    def step(self, amt=8):
        if self._dir:
            s = 255 - self._step
        else:
            s = self._step

        # this respects master brightness but is slower
        for y in range(self.height):
            for x in range(self.width):
                index = self._vector[y][x] * 255 / self.height + s
                self.layout.set(x, y, self.palette(index))

        self._step += amt
        if(self._step >= 255):
            self._step = 0
