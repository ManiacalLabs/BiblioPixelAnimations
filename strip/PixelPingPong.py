# ## PixelPingPong ##
# This animation runs 1 or many pixels from one end of a strip to the other.
#
# ### Usage ###
# Alternates has 3 optional properties
#
# * max_led - int the number of pixels you want used
# * color - (int, int, int) the color you want the pixels to be
# * additional_pixels - int the number of pixels you want to ping pong
#
# In code:
#
# 	from PixelPingPong import PixelPingPong
# 	...
# 	anim = PixelPingPong(led, max_led=30, color=(0, 0, 255), additional_pixels=5)
#
# Best run in the region of 5-200 FPS

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