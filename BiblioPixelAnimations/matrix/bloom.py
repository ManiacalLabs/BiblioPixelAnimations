from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors
from bibliopixel.util import genVector


class Bloom(BaseMatrixAnim):

    def __init__(self, layout, dir=True):
        super(Bloom, self).__init__(layout)
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
                c = colors.hue_helper(self._vector[y][x], self.layout.height, s)
                self.layout.set(x, y, c)

        self._step += amt
        if(self._step >= 255):
            self._step = 0
