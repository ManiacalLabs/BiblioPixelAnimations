from bibliopixel.animation.matrix import Matrix
from noise import pnoise3, snoise3


class PerlinSimplex(Matrix):

    def __init__(self, layout, freq=16, octaves=1, type=True, **kwds):
        super().__init__(layout, **kwds)
        self._step = 1
        self._freq = float(freq)
        self._octaves = octaves
        if type:
            self.func = snoise3
        else:
            self.func = pnoise3

    def step(self, amt):
        for y in range(self.height):
            for x in range(self.width):
                v = int(self.func(x / self._freq, y / self._freq, self._step / self._freq, octaves=self._octaves) * 127.0 + 128.0)
                c = self.palette(v)
                self.layout.set(x, y, c)

        self._step += amt
