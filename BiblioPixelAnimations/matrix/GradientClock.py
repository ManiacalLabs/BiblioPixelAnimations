from __future__ import division
from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors
from bibliopixel.util import pointOnCircle
from bibliopixel import log
import time
import math


class GradientClock(BaseMatrixAnim):
    def __init__(self, led):
        super(GradientClock, self).__init__(led)

        self.cdim = self._led.width
        self.half = self.cdim // 2
        self.odd = (self.half * 2) < self.cdim

        self.hue = colors.hue2rgb_rainbow

    def step(self, amt=1):
        self._led.all_off()
        t = time.localtime()
        hrs = t.tm_hour % 12
        mins = t.tm_min
        sec = t.tm_sec

        h_hrs = hrs * (256 // 12)
        h_min = mins * (256 // 60)
        h_sec = sec * (256 // 60)

        grad = []

        grad += colors.hue_gradient(h_hrs, h_min, self.half)
        if self.odd:
            grad += [h_min]
        grad += colors.hue_gradient(h_min, h_sec, self.half)

        log.debug('{}:{}:{}'.format(hrs, mins, sec))

        for x in range(self.cdim):
            self._led.drawLine(x, 0, x, self._led.height - 1, colors.hue2rgb(grad[x]))

        self._step = 0


MANIFEST = [
    {
        "class": GradientClock,
        "controller": "matrix",
        "desc": "RGB Gradient Clock",
        "display": "GradientClock",
        "id": "GradientClock",
        "params": [],
        "type": "animation"
    }
]
