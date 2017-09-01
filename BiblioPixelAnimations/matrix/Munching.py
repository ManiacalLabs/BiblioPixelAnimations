from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors
import random
import math


class Munching(BaseMatrixAnim):
    def __init__(self, layout, t=0, comparator=None):
        super().__init__(layout)
        self.t_start = t
        self.t = 0

    def pre_run(self):
        if self.t_start is None:
            self.t = random.randrange(32)
        else:
            self.t = self.t_start

    def step(self, amt=1):
        self.layout.all_off()
        for y in range(self.height):
            for x in range(self.width):
                if (x ^ y > self.t):
                    self.layout.set(x, y, colors.Red)
        self.t += amt


class Demo(BaseMatrixAnim):
    def __init__(self, layout):
        super().__init__(layout)

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        self.layout.all_off()
        for y in range(self.height):
            for x in range(self.width):
                # h = x + (x * y) + self._step # :)
                # h = x * self._step + (x * y) # :)
                # h = x * y * self._step + self._step # :)
                # h = x * y - math.log(self._step + 1) + self._step
                # h = math.cos(0.5 * x) * y + self._step # :)
                # h = math.cos(x * y) * y + self._step #:)
                # h = math.tan(y) * math.cos(x) + self._step
                # h = math.sin(y) + x * self._step # :)
                # h = math.sin(x) + y * self._step # :)
                # h = math.sin(x * y) + y * x + self._step # :)
                # h = x * x - y * y + self._step # :) !
                # h = (x * y - y * y) + self._step # :)
                # h = (x * y - y * y) % (self._step + 1) # :)
                # h = (y * y + x * x) + self._step # :)
                # h = x * y * 2 - y * y * 2 + self._step
                # h = (x / (y + 1)) + (y * y) + self._step
                h = ((x * x) / 2 * (y + 1)) + self._step
                c = colors.hue2rgb_360(abs(int(h)) % 360)
                self.layout.set(x, y, c)
        self._step += amt
