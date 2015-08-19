from bibliopixel import LEDStrip
import bibliopixel.colors as colors
from bibliopixel.animation import BaseStripAnim

import math
import time
import random

class Rainbow(BaseStripAnim):
    """Generate rainbow distributed over 256 pixels.
       If you want the full rainbow to fit in the number of pixels you
       are using, use RainbowCycle instead
    """

    def __init__(self, led, start=0, end=-1):
        super(Rainbow, self).__init__(led, start, end)

    def step(self, amt = 1):
        for i in range(self._size):
            h = (i + self._step) % 255
            self._led.set(self._start + i, colors.hue2rgb_rainbow(h))

        self._step += amt
        overflow = self._step - 256
        if overflow >= 0:
            self._step = overflow

class RainbowCycle(BaseStripAnim):
    """Generate rainbow wheel equally distributed over strip."""

    def __init__(self, led, start=0, end=-1):
        super(RainbowCycle, self).__init__(led, start, end)

    def step(self, amt = 1):
        for i in range(self._size):
            c = colors.hue_helper(i, self._size, self._step)
            self._led.set(self._start + i, c)

        self._step += amt
        overflow = self._step - 256
        if overflow >= 0:
            self._step = overflow

MANIFEST = [
    {
        "class": Rainbow,
        "controller": "strip",
        "desc": "Rainbow animation",
        "display": "Rainbow",
        "id": "Rainbow",
        "params": [
            {
                "default": -1,
                "help": "Ending pixel (-1 for entire strip)",
                "id": "end",
                "label": "End",
                "type": "int"
            },
            {
                "default": 0,
                "help": "Starting pixel",
                "id": "start",
                "label": "Start",
                "type": "int"
            }
        ],
        "type": "animation"
    },
    {
        "class": RainbowCycle,
        "controller": "strip",
        "desc": "More dense rainbow animation",
        "display": "RainbowCycle",
        "id": "RainbowCycle",
        "params": [
            {
                "default": -1,
                "help": "Ending pixel (-1 for entire strip)",
                "id": "end",
                "label": "End",
                "type": "int"
            },
            {
                "default": 0,
                "help": "Starting pixel",
                "id": "start",
                "label": "Start",
                "type": "int"
            }
        ],
        "type": "animation"
    },]
