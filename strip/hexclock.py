# Author: Adam Haile
# Inspired by http://whatcolourisit.scn9a.org/

import time
from bibliopixel.animation import *
import bibliopixel.colors as colors
import bibliopixel.log as log


class HEXClock(BaseStripAnim):

    def __init__(self, led):
        super(HEXClock, self).__init__(led, 0, -1)

    def step(self, amt=1):
        t = time.localtime()
        hex = "#{0:0>2}{1:0>2}{2:0>2}".format(t.tm_hour, t.tm_min, t.tm_sec)
        c = colors.hex2rgb(hex)
        self._led.fill(c)

        self._step = 0



MANIFEST = [
    {
        "class": HEXClock, 
        "controller": "strip", 
        "desc": None, 
        "display": "HEXClock", 
        "id": "HEXClock", 
        "params": [], 
        "type": "animation"
    }
]