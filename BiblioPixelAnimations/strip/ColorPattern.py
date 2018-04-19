from bibliopixel.animation import BaseStripAnim
from bibliopixel import colors


class ColorPattern(BaseStripAnim):
    """Fill the dots progressively along the strip with alternating colors."""

    def __init__(self, layout, colors=[colors.Red, colors.Green, colors.Blue],
                 width=1, dir=True):
        super(ColorPattern, self).__init__(layout)
        self._colors = colors
        self._colorCount = len(colors)
        self._width = width
        self._total_width = self._width * self._colorCount
        self._dir = dir

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        for i in range(self._size):
            cIndex = ((i + self._step) % self._total_width) // self._width
            self.layout.set(i, self._colors[cIndex])
        self._step += amt * (1 if self._dir else -1)
        if self._dir and self._step >= self.layout.numLEDs:
            self._step = 0
        elif not self._dir and self._step < 0:
            self._step = self.layout.numLEDs - 1
