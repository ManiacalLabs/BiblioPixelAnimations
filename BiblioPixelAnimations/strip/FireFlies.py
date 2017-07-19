from bibliopixel.animation import BaseStripAnim
from bibliopixel import colors
import random


class FireFlies(BaseStripAnim):
    """Stobe Light Effect."""

    def __init__(self, layout, colors=[colors.Red], width=1, count=1, start=0, end=-1):
        super(FireFlies, self).__init__(layout, start, end)
        self._colors = colors
        self._color_count = len(colors)
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
            color = self._colors[random.randint(0, self._color_count - 1)]

            for i in range(self._width):
                if pixel + i < self.layout.numLEDs:
                    self.layout.set(pixel + i, color)

        self._step += amt
