from bibliopixel.animation import *

# This one is best run in the region of 5-10 frames a second

class Alternates(BaseStripAnim):

    def __init__(self, led, max_led=-1, color1=(255, 255, 255), color2=(0, 0, 0)):
        super(Alternates, self).__init__(led, 0, -1)
        self._current = 0
        self._minLed = 0
        self._maxLed = max_led
        if self._maxLed < 0 or self._maxLed < self._minLed:
            self._maxLed = self._led.lastIndex
        self._positive = True
        self._color1 = color1
        self._color2 = color2

    def step(self, amt=1):

        while self._current < self._maxLed:
            if self._current % 2 == 0:
                self._led.fill(self._color1 if self._positive else self._color2, self._current, self._current)
            else:
                self._led.fill(self._color2 if self._positive else self._color1, self._current, self._current)
            self._current += amt

        self._current = 0
        self._positive = not self._positive