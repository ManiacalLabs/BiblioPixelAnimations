from bibliopixel.animation.strip import Strip
from bibliopixel.colors import COLORS
from bibliopixel.util import deprecated
import math


class Wave(Strip):
    """Sine wave animation."""
    COLOR_DEFAULTS = ('color', COLORS.Red),

    def __init__(self, layout, cycles=2, start=0, end=-1, **kwds):
        super().__init__(layout, start, end, **kwds)
        self.cycles = cycles

    def step(self, amt=1):
        for i in range(self._size):
            y = math.sin(
                math.pi *
                float(self.cycles) *
                float(self._step * i) /
                float(self._size))

            if y >= 0.0:
                # Peaks of sine wave are white
                y = 1.0 - y  # Translate Y to 0.0 (top) to 1.0 (center)
                r, g, b = self.palette(0)
                c2 = (int(255 - float(255 - r) * y),
                      int(255 - float(255 - g) * y),
                      int(255 - float(255 - b) * y))
            else:
                # Troughs of sine wave are black
                y += 1.0  # Translate Y to 0.0 (bottom) to 1.0 (center)
                r, g, b = self.palette(0)
                c2 = (int(float(r) * y),
                      int(float(g) * y),
                      int(float(b) * y))
            self.layout.set(self._start + i, c2)

        self._step += amt

    if deprecated.allowed():
        @property
        def _cycles(self):
            return self.cycles

        @_cycles.setter
        def _cycles(self, cycles):
            self.cycles = cycles


class WaveMove(Wave):
    """Sine wave animation."""
    _moveStep = 0

    def step(self, amt=1):
        for i in range(self._size):
            y = math.sin((math.pi * float(self.cycles) * float(i) / float(self._size)) + self._moveStep)

            if y >= 0.0:
                # Peaks of sine wave are white
                y = 1.0 - y  # Translate Y to 0.0 (top) to 1.0 (center)
                r, g, b = self.palette(0)
                c2 = (int(255 - float(255 - r) * y), int(255 - float(255 - g) * y), int(255 - float(255 - b) * y))
            else:
                # Troughs of sine wave are black
                y += 1.0  # Translate Y to 0.0 (bottom) to 1.0 (center)
                r, g, b = self.palette(0)
                c2 = (int(float(r) * y),
                      int(float(g) * y),
                      int(float(b) * y))
            self.layout.set(self._start + i, c2)

        self._moveStep += amt
        self._moveStep += 1
        if(self._moveStep >= self._size):
            self._moveStep = 0
