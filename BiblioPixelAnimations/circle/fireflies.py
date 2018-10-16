from bibliopixel.animation import BaseCircleAnim
from bibliopixel import colors
import random


class FireFlies(BaseCircleAnim):
    COLOR_DEFAULTS = ('colors', [colors.Red, colors.Green, colors.Blue]),

    def __init__(self, layout, count=10, **kwds):
        super().__init__(layout, **kwds)
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
            self.layout._set_base(pixel, color)

        self._step += amt
