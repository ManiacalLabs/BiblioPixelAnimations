# ## PixelPingPong ##
# This animation runs 1 or many pixels from one end of a strip to the other.
#
# ### Usage ###
# Alternates has 4 optional properties
#
# * max_led - int the number of pixels you want used
# * color - (int, int, int) the color you want the pixels to be
# * additional_pixels - int the number of pixels you want to ping pong
# * fade_delay - int the number of frames for the trailing pixels to fade to black
#
# In code:
#
#   from PixelPingPong import PixelPingPong
#   ...
#   anim = PixelPingPong(led, max_led=30, color=(0, 0, 255), additional_pixels=5, fade_delay=2)
#
# Best run in the region of 5-200 FPS

from bibliopixel.animation import BaseStripAnim


class PixelPingPong(BaseStripAnim):

    def __init__(self, layout, max_led=None, color=(255, 255, 255),
                 total_pixels=1, fade_delay=1):
        super(PixelPingPong, self).__init__(layout, 0, -1)
        self._current = 0
        self._minLed = 0
        self._maxLed = max_led
        if self._maxLed is None or self._maxLed < self._minLed:
            self._maxLed = self.layout.numLEDs - 1
        self._additionalPixels = total_pixels - 1
        self._positive = True
        self._color = color
        self._fade_delay = fade_delay if fade_delay >= 1 else 1
        self._fade_increment = tuple(x / self._fade_delay for x in self._color)

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        # fade last frame's pixels
        for i in range(0, self._maxLed + 1):
            faded_color = tuple(x - self._fade_increment[i] if x > self._fade_increment[i] else 0 for (i, x) in enumerate(self.layout.get(i)))
            self.layout.fill(faded_color, i, i)

        self.layout.fill(
            self._color, self._current, self._current + self._additionalPixels)

        if self._positive:
            self._current += 1
        else:
            self._current -= 1

        if self._current + self._additionalPixels == self._maxLed:
            self._positive = False

        if self._current == self._minLed:
            self._positive = True
