from bibliopixel.animation.matrix import Matrix
from bibliopixel.colors.conversions import hue_gradient
from bibliopixel.util import log
import time


class GradientClock(Matrix):
    def __init__(self, layout, **kwds):
        super().__init__(layout, **kwds)

        self.cdim = self.width
        self.half = self.cdim // 2
        self.odd = (self.half * 2) < self.cdim

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

        grad += hue_gradient(h_hrs, h_min, self.half)
        if self.odd:
            grad += [h_min]
        grad += hue_gradient(h_min, h_sec, self.half)

        log.debug('{}:{}:{}'.format(hrs, mins, sec))

        for x in range(self.cdim):
            self.layout.drawLine(x, 0, x, self.height - 1,
                                 self.palette(grad[x]))
