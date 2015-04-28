from bibliopixel.animation import *

class PixelPingPong(BaseStripAnim):

    def __init__(self, led, max_led=-1, color=(255, 255, 255), additional_pixels=0):
        super(PixelPingPong, self).__init__(led, 0, -1)
        self._current = 0
        self._minLed = 0
        self._maxLed = max_led
        if self._maxLed < 0 or self._maxLed < self._minLed:
            self._maxLed = self._led.lastIndex
        self._additionalPixels = additional_pixels
        self._positive = True
        self._color = color

    def step(self, amt=1):
        self._led.fill((0, 0, 0), 0, self._maxLed)

        self._led.fill(self._color, self._current, self._current + self._additionalPixels)

        if self._positive:
            self._current += 1
        else:
            self._current -= 1

        if self._current + self._additionalPixels == self._maxLed:
            self._positive = False

        if self._current == self._minLed:
            self._positive = True