#  ## WhiteTwinkle ##
# This Bibliopixel animation randomly picks leds and slowly brightens them to a max brightness
# then dims them to off.
#
# Author: Bob Steinbeiser, based on work by Mark Kriegsman at:
#    https://gist.github.com/kriegsman/99082f66a726bdff7776
#
#  ## Usage ##
#
#  max_led -    The max number of pixels you want used ('None' for all leds)
#  speed   -    How fast the leds bighten then dim (best in range 2-40)
#  density -    The density (or number) of twinkling leds
#  max_bright - The maximum brightness, some leds twinkle better if they ramp to less than full
#                 brightness (19 - 255). Lower brightness also speeds up the twinkle rate.

from bibliopixel.animation import BaseStripAnim
import random


class WhiteTwinkle(BaseStripAnim):
    """ Random white twinkling leds """

    def __init__(self, layout, max_led=None, density=80, speed=2, max_bright=255):

        super(WhiteTwinkle, self).__init__(layout, 0, -1)
        self._current = 0
        self._minLed = 0
        self._maxLed = max_led
        if self._maxLed is None or self._maxLed < self._minLed:
            self._maxLed = self.layout.numLEDs - 1
        self.density = density
        self.speed = speed
        self.max_bright = max_bright

        # If max_bright is even then leds won't ever dim, make it odd
        if (self.max_bright & 1 == 0):
            self.max_bright -= 1

        # If the speed is odd then the leds won't ever brighten, make it even
        if self.speed & 1:
            self.speed += 1

        # Make sure speed, density & max_bright are in sane ranges
        self.speed = min(self.speed, 100)
        self.speed = max(self.speed, 2)
        self.density = min(self.density, 100)
        self.density = max(self.density, 2)
        self.max_bright = min(self.max_bright, 255)
        self.max_bright = max(self.max_bright, 5)

    def pre_run(self):
        self._step = 0

    def qadd8(self, color, inc):
        # increment the color brightness to a max of max_bright (that becomes odd)
        r = min(color[0] + inc, self.max_bright)
        g = min(color[1] + inc, self.max_bright)
        b = min(color[2] + inc, self.max_bright)
        return (r, g, b)

    def qsub8(self, color, dec):
        # decrement the color brightness to a min of 0 (that becomes even)
        r = max(color[0] - dec, 0)
        g = max(color[1] - dec, 0)
        b = max(color[2] - dec, 0)
        return (r, g, b)

    def pick_led(self, inc):
        # Pick a random led, if it's off bump it up an even number so it gets brighter
        idx = random.randrange(0, self.layout.numLEDs)
        this_led = self.layout.get(idx)
        r = this_led[0]

        if random.randrange(0, self._maxLed) < self.density:
            if r == 0:
                r += inc
                self.layout.set(idx, (2, 2, 2))

    def step(self, amt=1):
        # The direction of fade is determined by the red value of the led color
        self.pick_led(self.speed)

        for i in range(self._maxLed):

            this_led = self.layout.get(i)
            r = this_led[0]

            if r == 0:    # skip the black pixels
                continue

            # if red is odd darken it, if its even brighten it
            if int(r) & 1:
                self.layout.set(i, self.qsub8(this_led, self.speed))
            else:
                self.layout.set(i, self.qadd8(this_led, self.speed))

        self._step += amt
