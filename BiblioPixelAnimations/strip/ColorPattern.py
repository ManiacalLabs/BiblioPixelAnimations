from bibliopixel.animation.strip import Strip
from bibliopixel.colors import COLORS


class ColorPattern(Strip):
    """Fill the dots progressively along the strip with alternating colors."""
    COLOR_DEFAULTS = ('colors', [COLORS.Red, COLORS.Green, COLORS.Blue]),

    def __init__(self, layout, width=1, dir=True, **kwds):
        super().__init__(layout, **kwds)
        self._width = width
        self._total_width = self._width * len(self.palette)
        self._dir = dir

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        for i in range(self._size):
            cIndex = ((i + self._step) % self._total_width) / self._width
            self.layout.set(i, self.palette(cIndex))
        self._step += amt * (1 if self._dir else -1)
