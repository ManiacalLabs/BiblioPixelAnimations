from bibliopixel.animation import BaseCircleAnim
import random


class FireFlies(BaseCircleAnim):

    def __init__(self, led, colors, count=10):
        super(FireFlies, self).__init__(led)
        self._colors = colors
        self._color_count = len(colors)
        self._count = count

    def step(self, amt=1):
        amt = 1  # anything other than 1 would be just plain silly
        if self._step > self._led.numLEDs:
            self._step = 0

        self._led.all_off()

        for i in range(self._count):
            pixel = random.randint(0, self._led.numLEDs - 1)
            color = self._colors[random.randint(0, self._color_count - 1)]
            self._led._set_base(pixel, color)

        self._step += amt
