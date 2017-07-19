from bibliopixel.animation import BaseStripAnim


class ColorWipe(BaseStripAnim):
    """Fill the dots progressively along the strip."""

    def __init__(self, layout, color=[255, 0, 0], start=0, end=-1):
        super(ColorWipe, self).__init__(layout, start, end)
        self._color = color

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        if self._step == 0:
            self.layout.all_off()
        for i in range(amt):
            self.layout.set(self._start + self._step - i, self._color)

        self._step += amt
        overflow = (self._start + self._step) - self._end
        if overflow >= 0:
            self._step = overflow
