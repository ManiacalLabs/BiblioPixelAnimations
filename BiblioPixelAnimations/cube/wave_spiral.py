from bibliopixel.animation.cube import BaseCubeAnim
import bibliopixel.colors as colors


def spiralOrder(matrix):
    return matrix and list(matrix.pop(0)) + spiralOrder(list(zip(*matrix))[::-1])


class WaveSpiral(BaseCubeAnim):

    def __init__(self, layout, offset=1, dir=True):
        super(WaveSpiral, self).__init__(layout)
        self.offset = offset
        self._dir = dir
        self.spiral_len = self.x * self.y
        self.matrix = []

        for x in range(self.x):
            col = []
            for y in range(self.y):
                col.append((x, y))
            self.matrix.append(col)

        self.spiral = spiralOrder(self.matrix)

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        if self._dir:
            s = 255 - self._step
        else:
            s = self._step

        offset_total = 0
        for z in range(self.z):
            for i in range(self.spiral_len):
                c = colors.hue_helper(i, self.spiral_len, s + offset_total)
                x, y = self.spiral[i]
                self.layout.set(x, y, z, c)
            offset_total += self.offset

        self._step += amt
        if(self._step >= 255):
            self._step = 0
