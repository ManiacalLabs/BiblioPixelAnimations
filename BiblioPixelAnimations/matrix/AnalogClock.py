from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors
from bibliopixel.util import pointOnCircle
import time
import math


class AnalogClock(BaseMatrixAnim):
    def __init__(self, led, aa=True):
        super(AnalogClock, self).__init__(led)
        self._centerX = (self._led.width - 1) / 2
        self._centerY = (self._led.height - 1) / 2
        self.hand_length = self._centerX if self._centerX <= self._centerY else self._centerY
        self.aa = aa

    def step(self, amt=1):
        self._led.all_off()
        t = time.localtime()
        hrs = t.tm_hour % 12
        mins = t.tm_min
        sec = t.tm_sec

        p_hrs = pointOnCircle(self._centerX, self._centerY, int(self.hand_length * 0.7), hrs * 30)
        p_min = pointOnCircle(self._centerX, self._centerY, self.hand_length, mins * 6)
        p_sec = pointOnCircle(self._centerX, self._centerY, self.hand_length, sec * 6)

        self._led.drawLine(self._centerX, self._centerY, p_hrs[0], p_hrs[1], (255, 0, 0), aa=self.aa)
        self._led.drawLine(self._centerX, self._centerY, p_min[0], p_min[1], (0, 255, 0), aa=self.aa)
        self._led.drawLine(self._centerX, self._centerY, p_sec[0], p_sec[1], (0, 0, 255), aa=self.aa)

        self._step = 0


class RGBAnalogClock(BaseMatrixAnim):

    def __init__(self, led, aa=True):
        super(RGBAnalogClock, self).__init__(led)
        self._centerX = (self._led.width - 1) / 2
        self._centerY = (self._led.height - 1) / 2
        self.hand_length = self._centerX if self._centerX <= self._centerY else self._centerY
        self.aa = aa

    def step(self, amt=1):
        self._led.all_off()
        t = time.localtime()
        hrs = t.tm_hour % 12
        mins = t.tm_min
        sec = t.tm_sec

        p_hrs = pointOnCircle(self._centerX, self._centerY, int(self.hand_length * 0.7), hrs * 30)
        p_min = pointOnCircle(self._centerX, self._centerY, self.hand_length, mins * 6)
        p_sec = pointOnCircle(self._centerX, self._centerY, self.hand_length, sec * 6)

        c_hrs = colors.hue2rgb_rainbow(hrs * (256 / 12))

        c_min = colors.hue2rgb_rainbow(mins * (256 / 60))

        c_sec = colors.hue2rgb_rainbow(sec * (256 / 60))

        self._led.drawLine(self._centerX, self._centerY, p_hrs[0], p_hrs[1], c_hrs, aa=self.aa)
        self._led.drawLine(self._centerX, self._centerY, p_min[0], p_min[1], c_min, aa=self.aa)
        self._led.drawLine(self._centerX, self._centerY, p_sec[0], p_sec[1], c_sec, aa=self.aa)

        self._step = 0


MANIFEST = [
    {
        "class": AnalogClock,
        "controller": "matrix",
        "desc": "Displays analog clock with red, green, and blue hands.",
        "display": "AnalogClock",
        "id": "AnalogClock",
        "params": [
            {
                "default": True,
                "help": "",
                "id": "aa",
                "label": "AntiAlias",
                "type": "bool"
            }
        ],
        "type": "animation"
    },
    {
        "class": RGBAnalogClock,
        "controller": "matrix",
        "desc": "Displays analog clock with hand colors based on their angle converted to a hue value.",
        "display": "RGBAnalogClock",
        "id": "RGBAnalogClock",
        "params": [
            {
                "default": True,
                "help": "",
                "id": "aa",
                "label": "AntiAlias",
                "type": "bool"
            }
        ],
        "type": "animation"
    }
]
