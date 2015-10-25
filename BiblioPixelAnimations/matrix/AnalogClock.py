from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors
from bibliopixel.util import pointOnCircle
import time, math

class AnalogClock(BaseMatrixAnim):
    def __init__(self, led):
        super(AnalogClock, self).__init__(led)
        self._centerX = (self._led.width - 1) / 2
        self._centerY = (self._led.height - 1) / 2

    def step(self, amt = 1):
        self._led.all_off()
        t = time.localtime()
        hrs = t.tm_hour % 12
        min = t.tm_min
        sec = t.tm_sec

        p_hrs = pointOnCircle(self._centerX, self._centerY, int(self._centerX *0.7), hrs * 30)
        p_min = pointOnCircle(self._centerX, self._centerY, self._centerX, min * 6)
        p_sec = pointOnCircle(self._centerX, self._centerY, self._centerX, sec * 6)

        self._led.drawLine(self._centerX, self._centerY, p_hrs[0], p_hrs[1], (255, 0, 0))
        self._led.drawLine(self._centerX, self._centerY, p_min[0], p_min[1], (0, 255, 0))
        self._led.drawLine(self._centerX, self._centerY, p_sec[0], p_sec[1], (0, 0, 255))

        self._step = 0

class RGBAnalogClock(BaseMatrixAnim):

    def __init__(self, led):
        super(RGBAnalogClock, self).__init__(led)
        self._centerX = (self._led.width - 1) / 2
        self._centerY = (self._led.height - 1) / 2

    def step(self, amt = 1):
        self._led.all_off()
        t = time.localtime()
        hrs = t.tm_hour % 12
        min = t.tm_min
        sec = t.tm_sec

        p_hrs = pointOnCircle(self._centerX, self._centerY, int(self._centerX * 0.7), hrs * 30)
        p_min = pointOnCircle(self._centerX, self._centerY, self._centerX, min * 6)
        p_sec = pointOnCircle(self._centerX, self._centerY, self._centerX, sec * 6)

        c_hrs = colors.hue2rgb_rainbow(t.tm_hour * (256/24))

        c_min = colors.hue2rgb_rainbow(min * (256/60))

        c_sec = colors.hue2rgb_rainbow(sec * (256/60))

        self._led.drawLine(self._centerX, self._centerY, p_hrs[0], p_hrs[1], c_hrs)
        self._led.drawLine(self._centerX, self._centerY, p_min[0], p_min[1], c_min)
        self._led.drawLine(self._centerX, self._centerY, p_sec[0], p_sec[1], c_sec)

        self._step = 0



MANIFEST = [
    {
        "class": AnalogClock,
        "controller": "matrix",
        "desc": "Displays analog clock with red, green, and blue hands.", 
        "display": "AnalogClock",
        "id": "AnalogClock",
        "params": [],
        "type": "animation"
    },
    {
        "class": RGBAnalogClock,
        "controller": "matrix",
        "desc": "Displays analog clock with hand colors based on their angle converted to a hue value.",
        "display": "RGBAnalogClock",
        "id": "RGBAnalogClock",
        "params": [],
        "type": "animation"
    }
]
