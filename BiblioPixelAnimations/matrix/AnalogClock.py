import time

from bibliopixel.animation import BaseMatrixAnim
from bibliopixel.util import pointOnCircle


class AnalogClock(BaseMatrixAnim):
    def __init__(self, layout, aa=True):
        super().__init__(layout)
        self._centerX = (self.layout.width - 1) // 2
        self._centerY = (self.layout.height - 1) // 2
        self.hand_length = min(self._centerX, self._centerY)
        self.aa = aa

    def step(self, amt=1):
        self.layout.all_off()
        t = time.localtime()
        hrs = t.tm_hour % 12
        mins = t.tm_min
        sec = t.tm_sec

        p_hrs = pointOnCircle(self._centerX, self._centerY, int(self.hand_length * 0.7), hrs * 30)
        p_min = pointOnCircle(self._centerX, self._centerY, self.hand_length, mins * 6)
        p_sec = pointOnCircle(self._centerX, self._centerY, self.hand_length, sec * 6)

        self.layout.drawLine(self._centerX, self._centerY, p_hrs[0], p_hrs[1], (255, 0, 0), aa=self.aa)
        self.layout.drawLine(self._centerX, self._centerY, p_min[0], p_min[1], (0, 255, 0), aa=self.aa)
        self.layout.drawLine(self._centerX, self._centerY, p_sec[0], p_sec[1], (0, 0, 255), aa=self.aa)

        self._step = 0


class RGBAnalogClock(BaseMatrixAnim):

    def __init__(self, layout, aa=True):
        super().__init__(layout)
        self._centerX = (self.layout.width - 1) // 2
        self._centerY = (self.layout.height - 1) // 2
        self.hand_length = min(self._centerX, self._centerY)
        self.aa = aa

    def step(self, amt=1):
        self.layout.all_off()
        t = time.localtime()
        hrs = t.tm_hour % 12
        mins = t.tm_min
        sec = t.tm_sec

        p_hrs = pointOnCircle(self._centerX, self._centerY, int(self.hand_length * 0.7), hrs * 30)
        p_min = pointOnCircle(self._centerX, self._centerY, self.hand_length, mins * 6)
        p_sec = pointOnCircle(self._centerX, self._centerY, self.hand_length, sec * 6)

        c_hrs = self.palette(hrs * (256 // 12))
        c_min = self.palette(mins * (256 // 60))
        c_sec = self.palette(sec * (256 // 60))

        self.layout.drawLine(self._centerX, self._centerY, p_hrs[0], p_hrs[1], c_hrs, aa=self.aa)
        self.layout.drawLine(self._centerX, self._centerY, p_min[0], p_min[1], c_min, aa=self.aa)
        self.layout.drawLine(self._centerX, self._centerY, p_sec[0], p_sec[1], c_sec, aa=self.aa)

        self._step = 0
