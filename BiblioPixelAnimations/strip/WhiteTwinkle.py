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

import time, random
from bibliopixel.animation import *

class WhiteTwinkle(BaseStripAnim):
    """ Random white twinkling leds """

    def __init__(self, led, max_led=None, density=80, speed=2, max_bright=255):

        super(WhiteTwinkle, self).__init__(led, 0, -1)
        self._current = 0
        self._minLed = 0
        self._maxLed = max_led
        if self._maxLed == None or self._maxLed < self._minLed:
            self._maxLed = self._led.lastIndex
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


    def qadd8 (self, color, inc):
        # increment the color brightness to a max of max_bright (that becomes odd)
        r = min(color[0] + inc, self.max_bright)
        g = min(color[1] + inc, self.max_bright)
        b = min(color[2] + inc, self.max_bright)
        return (r, g, b)

    def qsub8 (self, color, dec):
        # decrement the color brightness to a min of 0 (that becomes even)
        r = max(color[0] - dec, 0)
        g = max(color[1] - dec, 0)
        b = max(color[2] - dec, 0)
        return (r, g, b)

    def pick_led(self, inc):
        # Pick a random led, if it's off bump it up an even number so it gets brighter
        idx =  random.randrange(0,self._led.numLEDs)
        this_led = self._led.get(idx)
        r,g,b = this_led[0], this_led[1], this_led[2]

        if random.randrange(0,self._maxLed) < self.density:
            if r == 0:
                r += inc
                self._led.set(idx, (2,2,2))

    def step(self, amt = 1):
        # The direction of fade is determined by the red value of the led color
        self.pick_led(self.speed)

        for i in range(self._maxLed):

            this_led = self._led.get(i)
            r = this_led[0]

            if r == 0:    # skip the black pixels
                continue;

            # if red is odd darken it, if its even brighten it 
            if r & 1: 
                self._led.set(i, self.qsub8(this_led, self.speed))
            else:
                self._led.set(i, self.qadd8(this_led, self.speed))

            #log.logger.info("Led: {0} - {1}".format(i, self._led.get(i)))

        self._step += amt

MANIFEST = [
    {
        "class": WhiteTwinkle, 
        "controller": "strip", 
        "desc": "Random White Twinkling Leds", 
        "display": "Random White Twinkling Leds", 
        "id": "WhiteTwinkle", 
        "params": [
            {
                "default": None, 
                "help": "Last pixel index to use. Leave empty to use max index.", 
                "id": "max_led", 
                "label": "Last Pixel", 
                "type": "int"
            }, 
            {
                "default": 2, 
                "help": "Fade up/down speed of the twinkle (best in range of 2-20) (100 max)", 
                "id": "speed", 
                "label": "Fade Speed", 
                "type": "int"
            }, 
            {
                "default": 80, 
                "help": "Density (or number) of the twinkling leds (best in range 40-80) (100 max)", 
                "id": "density", 
                "label": "Twinkling LED Density", 
                "type": "int"
            },
            {
                "default": 255, 
                "help": "Some leds twinkle better at less than full brightness. This also speeds up the twinkle rate. (255 max)", 
                "id": "max_bright", 
                "label": "LED Max Brightness", 
                "type": "int"
            }
        ], 
        "type": "animation"
    }
]
