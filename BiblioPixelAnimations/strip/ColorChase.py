from bibliopixel.animation import BaseStripAnim


class ColorChase(BaseStripAnim):
    """Chase one pixel down the strip."""

    def __init__(self, layout, color=[255, 0, 0], width=1, start=0, end=-1):
        super(ColorChase, self).__init__(layout, start, end)
        self._color = color
        self._width = width

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        self.layout.all_off()  # because I am lazy

        for i in range(self._width):
            self.layout.set(self._start + self._step + i, self._color)

        self._step += amt
        overflow = (self._start + self._step) - self._end
        if overflow >= 0:
            self._step = overflow
