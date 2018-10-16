from bibliopixel.animation import BaseStripAnim
import bibliopixel.colors as colors


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
        color = self._get_color()
        self.layout.set(self._last, color)

        for i in range(self._tail):
            c2 = colors.color_scale(color, 255 - (self._fadeAmt * i))
            self.layout.set(self._last - i, c2)
            self.layout.set(self._last + i, c2)

        if self._start + self._step >= self._end:
            self._direction = -self._direction
        elif self._step <= 0:
            self._direction = -self._direction

        self._step += self._direction * amt

    def _get_color(self):
        return self.palette(0)


class LarsonRainbow(LarsonScanner):
    """Larson scanner (i.e. Cylon Eye or K.I.T.T.) but Rainbow."""

    def _get_color(self):
        return self.palette(self._step)
