from bibliopixel.animation import BaseStripAnim
from bibliopixel import colors
import random


class FireFlies(BaseStripAnim):
    """Stobe Light Effect."""
    COLOR_DEFAULTS = ('colors', [colors.Red]),

    def __init__(self, layout, width=1, count=1, start=0, end=-1, **kwds):
        super().__init__(layout, start, end, **kwds)
        self._width = width
        self._count = count

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        amt = 1  # anything other than 1 would be just plain silly
        if self._step > self.layout.numLEDs:
            self._step = 0

        self.layout.all_off()

        for i in range(self._count):
            pixel = random.randint(0, self.layout.numLEDs - 1)
            color = random.choice(self.palette)

            for i in range(self._width):
                if pixel + i < self.layout.numLEDs:
                    self.layout.set(pixel + i, color)

        self._step += amt
