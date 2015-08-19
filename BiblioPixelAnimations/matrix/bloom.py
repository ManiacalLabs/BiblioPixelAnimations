from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors
from bibliopixel.util import genVector

import math

class Bloom(BaseMatrixAnim):

    def __init__(self, led, dir = True):
        super(Bloom, self).__init__(led)
        self._vector = genVector(self._led.width, self._led.height)
        self._dir = dir

    def step(self, amt = 8):
        if self._dir:
            s = 255 - self._step
        else:
            s = self._step

        h = self._led.height
        w = self._led.width

        #this ignores master brightness in the interest of speed
        # buf = [colors.hue_helper(self._vector[y][x], h, s) for y in range(h) for x in range(w)]
        # buf = [i for sub in buf for i in sub]
        # self._led.setBuffer(buf)

        #this respects master brightness but is slower
        for y in range(self._led.height):
           for x in range(self._led.width):
               c = colors.hue_helper(self._vector[y][x], self._led.height, s)
               self._led.set(x, y, c)

        self._step += amt
        if(self._step >= 255):
            self._step = 0
