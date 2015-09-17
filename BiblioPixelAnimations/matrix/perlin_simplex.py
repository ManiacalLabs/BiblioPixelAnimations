from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors

from noise import pnoise3, snoise3

class PerlinSimplex(BaseMatrixAnim):

    def __init__(self, led, freq=16, octaves=1, type=True):
        super(PerlinSimplex, self).__init__(led)
        self._step = 1
        self._freq = float(freq)
        self._octaves = octaves
        if type:
            self.func = snoise3
        else:
            self.func = pnoise3

    def step(self, amt):
        octaves = 1
        freq = 16.0
        data = []
        for y in range(self.height):
            for x in range(self.width):
                v = int(self.func(x / self._freq, y / self._freq, self._step / self._freq, octaves=self._octaves) * 127.0 + 128.0)
                c = colors.hue2rgb_rainbow(v)
                self._led.set(x,y, c)

        self._step += amt


MANIFEST = [
    {
        "class": PerlinSimplex,
        "controller": "matrix",
        "desc": "Perlin / Simplex noise generator",
        "display": "Perlin / Simplex",
        "id": "PerlinSimplex",
        "params": [
            {
                "default": 16,
                "help": "Relative distance between high/low points",
                "id": "freq",
                "label": "Spread",
                "type": "int",
                "min": 1,
                "max": 64
            },{
                "default": 1,
                "help": "High values runs more passes on the noise generation, resulting in higher complexity.",
                "id": "octaves",
                "label": "Complexity",
                "type": "int",
                "min": 1,
                "max": 8
            },{
                "default": True,
                "help": "On for Simplex, Off for Perlin",
                "id": "type",
                "label": "Perlin / Simplex",
                "type": "bool"
            }
        ],
        "type": "animation"
    }
]
