from bibliopixel.colors import COLORS as _COLORS
from bibliopixel.colors.arithmetic import color_scale
from bibliopixel.animation.strip import Strip

import random


class Searchlights(Strip):
    """Three search lights sweeping at different speeds"""
    COLORS = [_COLORS.MediumSeaGreen, _COLORS.MediumPurple,
              _COLORS.MediumVioletRed]
    COLOR_DEFAULTS = ('colors', COLORS),

    def __init__(self, layout, tail=5, start=0, end=-1, **kwds):
        super().__init__(layout, start, end, **kwds)

        self._tail = tail + 1
        if self._tail >= self._size // 2:
            self._tail = (self._size // 2) - 1

    def pre_run(self):
        self._direction = [1, 1, 1]
        self._currentpos = [0, 0, 0]
        self._steps = [1, 1, 1]
        self._fadeAmt = 256 / self._tail

    def step(self, amt=1):
        self._ledcolors = [(0, 0, 0) for i in range(self._size)]
        self.layout.all_off()

        for i in range(0, 3):
            self._currentpos[i] = self._start + self._steps[i]

            color = self.palette(i)

            # average the colors together so they blend
            self._ledcolors[self._currentpos[i]] = list(map(lambda x, y: (x + y) // 2, color, self._ledcolors[self._currentpos[i]]))
            for j in range(1, self._tail):
                if self._currentpos[i] - j >= 0:
                    self._ledcolors[self._currentpos[i] - j] = list(map(lambda x, y: (x + y) // 2, self._ledcolors[self._currentpos[i] - j], color_scale(color, 255 - (self._fadeAmt * j))))
                if self._currentpos[i] + j < self._size:
                    self._ledcolors[self._currentpos[i] + j] = list(map(lambda x, y: (x + y) // 2, self._ledcolors[self._currentpos[i] + j], color_scale(color, 255 - (self._fadeAmt * j))))
            if self._start + self._steps[i] >= self._end:
                self._direction[i] = -1
            elif self._start + self._steps[i] <= 0:
                self._direction[i] = 1

            # advance each searchlight at a slightly different speed
            self._steps[i] += self._direction[i] * amt * int(random.random() > (i * 0.05))

        for i, thiscolor in enumerate(self._ledcolors):
            self.layout.set(i, thiscolor)
