from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors
from bibliopixel import log
import time


class GradientClock(BaseMatrixAnim):
    def __init__(self, layout):
        super(GradientClock, self).__init__(layout)

        self.cdim = self.layout.width
        self.half = self.cdim // 2
        self.odd = (self.half * 2) < self.cdim

        self.hue = colors.hue2rgb

    def step(self, amt=1):
        self.layout.all_off()
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
            self.layout.drawLine(x, 0, x, self.layout.height - 1, colors.hue2rgb(grad[x]))

        self._step = 0
