import bibliopixel.colors as colors
from bibliopixel.animation import BaseStripAnim


class LarsonScanner(BaseStripAnim):
    """Larson scanner (i.e. Cylon Eye or K.I.T.T.)."""
    COLOR_DEFAULTS = ('color', colors.Red),

    def __init__(self, layout, tail=2, start=0, end=-1, **kwds):
        super().__init__(layout, start, end, **kwds)

        self._tail = tail + 1  # makes tail math later easier
        if self._tail >= self._size // 2:
            self._tail = (self._size // 2) - 1

        if self._tail == 0:
            self._tail = 1
        self._fadeAmt = 256 // self._tail

    def pre_run(self):
        self._direction = -1
        self._last = 0
        self._step = 0

    def step(self, amt=1):
        self.layout.all_off()

        self._last = self._start + self._step
        color = self.palette.get(0)
        self.layout.set(self._last, color)

        for i in range(self._tail):
            self.layout.set(self._last - i, colors.color_scale(color, 255 - (self._fadeAmt * i)))
            self.layout.set(self._last + i, colors.color_scale(color, 255 - (self._fadeAmt * i)))

        if self._start + self._step >= self._end:
            self._direction = -self._direction
        elif self._step <= 0:
            self._direction = -self._direction

        self._step += self._direction * amt


class LarsonRainbow(LarsonScanner):
    """Larson scanner (i.e. Cylon Eye or K.I.T.T.) but Rainbow."""

    def __init__(self, layout, tail=2, start=0, end=-1):
        super().__init__(layout, colors.Off, tail, start, end)

    def step(self, amt=1):
        self._color = colors.hue_helper(0, self._size, self._step)

        super().step(amt)
