import bibliopixel.colors as colors
from bibliopixel.animation import BaseStripAnim


class LarsonScanner(BaseStripAnim):
    """Larson scanner (i.e. Cylon Eye or K.I.T.T.)."""

    def __init__(self, layout, color=colors.Red, tail=2, start=0, end=-1):
        super(LarsonScanner, self).__init__(layout, start, end)
        self._color = color

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
        self.layout.set(self._last, self._color)

        for i in range(self._tail):
            self.layout.set(self._last - i, colors.color_scale(self._color, 255 - (self._fadeAmt * i)))
            self.layout.set(self._last + i, colors.color_scale(self._color, 255 - (self._fadeAmt * i)))

        if self._start + self._step >= self._end:
            self._direction = -self._direction
        elif self._step <= 0:
            self._direction = -self._direction

        self._step += self._direction * amt


class LarsonRainbow(LarsonScanner):
    """Larson scanner (i.e. Cylon Eye or K.I.T.T.) but Rainbow."""

    def __init__(self, layout, tail=2, start=0, end=-1):
        super(LarsonRainbow, self).__init__(layout, colors.Off, tail, start, end)

    def step(self, amt=1):
        self._color = colors.hue_helper(0, self._size, self._step)

        super(LarsonRainbow, self).step(amt)
