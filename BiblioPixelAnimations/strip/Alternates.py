# ## Alternates ##
# This animation alternates colours on every other pixel and then animates them flipping between the default
# colours White and Off.
#
# ## Usage ###
# Alternates has 3 optional properties
#
# * max_led - int the number of pixels you want used
# * color1 - (int, int, int) the color you want the odd pixels to be
# * color2 - (int, int, int) the color you want the even pixels to be
#
# In code:
#
# 	from Alternates import Alternates
# 	...
# 	anim = Alternates(led, max_led=10, color1=(255, 0, 0), color2=(0, 0, 255))
#
# Best run in the region of 5-10 FPS


from bibliopixel.animation import BaseStripAnim


class Alternates(BaseStripAnim):

    def __init__(self, layout, max_led=-1, color1=(255, 255, 255), color2=(0, 0, 0)):
        super(Alternates, self).__init__(layout, 0, -1)
        self._current = 0
        self._minLed = 0
        self._maxLed = max_led
        if self._maxLed < 0 or self._maxLed < self._minLed:
            self._maxLed = self.layout.numLEDs - 1
        self._positive = True
        self._color1 = color1
        self._color2 = color2

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):

        while self._current < self._maxLed:
            if self._current % 2 == 0:
                self.layout.fill(
                    self._color1 if self._positive else self._color2, self._current, self._current)
            else:
                self.layout.fill(
                    self._color2 if self._positive else self._color1, self._current, self._current)
            self._current += amt

        self._current = self._minLed
        self._positive = not self._positive
