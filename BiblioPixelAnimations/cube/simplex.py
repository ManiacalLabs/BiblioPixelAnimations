from bibliopixel.animation import BaseCubeAnim
from bibliopixel import colors

from noise import snoise4


class Simplex(BaseCubeAnim):

    def __init__(self, layout, freq=16, octaves=1):
        super(Simplex, self).__init__(layout)
        self._step = 1
        self._freq = float(freq)
        self._octaves = octaves

    def pre_run(self):
        self._step = 0

    def step(self, amt):
        for y in range(self.x):
            for x in range(self.y):
                for z in range(self.z):
                    v = int(snoise4(x / self._freq, y / self._freq, z / self._freq,
                                    self._step / self._freq, octaves=self._octaves) * 127.0 + 128.0)
                    c = colors.hue2rgb(v)
                    self.layout.set(x, y, z, c)

        self._step += amt
