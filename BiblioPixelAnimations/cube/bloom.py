from bibliopixel.animation.cube import BaseCubeAnim
import bibliopixel.colors as colors
import math


def genCubeVector(x, y, z, x_mult=1, y_mult=1, z_mult=1):
    """Generates a map of vector lengths from the center point to each coordinate

    x - width of matrix to generate
    y - height of matrix to generate
    z - depth of matrix to generate
    x_mult - value to scale x-axis by
    y_mult - value to scale y-axis by
    z_mult - value to scale z-axis by
    """
    cX = (x - 1) / 2.0
    cY = (y - 1) / 2.0
    cZ = (z - 1) / 2.0

    def vect(_x, _y, _z):
        return int(math.sqrt(math.pow(_x - cX, 2 * x_mult) +
                             math.pow(_y - cY, 2 * y_mult) +
                             math.pow(_z - cZ, 2 * z_mult)))

    return [[[vect(_x, _y, _z) for _z in range(z)] for _y in range(y)] for _x in range(x)]


class CubeBloom(BaseCubeAnim):

    def __init__(self, layout, dir=True):
        super(CubeBloom, self).__init__(layout)
        self._vector = genCubeVector(self.x, self.y, self.z)
        self._dir = dir

    def pre_run(self):
        self._step = 0

    def step(self, amt=8):
        if self._dir:
            s = 255 - self._step
        else:
            s = self._step

        # this respects master brightness but is slower
        for z in range(self.z):
            for y in range(self.y):
                for x in range(self.x):
                    c = colors.hue_helper(self._vector[x][y][z], self.y, s)
                    self.layout.set(x, y, z, c)

        self._step += amt
        if(self._step >= 255):
            self._step = 0
