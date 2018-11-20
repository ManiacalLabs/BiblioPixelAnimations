from bibliopixel.animation.strip import Strip


class Rainbow(Strip):
    """Generate rainbow distributed over 256 pixels.
       If you want the full rainbow to fit in the number of pixels you
       are using, use RainbowCycle instead
    """

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        for i in range(self._size):
            h = (i + self._step) % 255
            self.layout.set(self._start + i, self.palette(h))

        self._step += amt
        overflow = self._step - 256
        if overflow >= 0:
            self._step = overflow


class RainbowCycle(Strip):
    """Generate rainbow wheel equally distributed over strip."""

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        for i in range(self._size):
            color = self.palette(i * 255 / self._size + self._step)
            self.layout.set(self._start + i, color)

        self._step += amt
        overflow = self._step - 256
        if overflow >= 0:
            self._step = overflow
