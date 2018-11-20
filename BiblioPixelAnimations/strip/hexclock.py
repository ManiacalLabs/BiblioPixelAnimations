# Author: Adam Haile
# Inspired by http://whatcolourisit.scn9a.org/

import time
from bibliopixel.animation.strip import Strip
from bibliopixel.colors import COLORS


class HEXClock(Strip):

    def __init__(self, layout, **kwds):
        super().__init__(layout, 0, -1, **kwds)

    def step(self, amt=1):
        t = time.localtime()
        hex = "#{0:0>2}{1:0>2}{2:0>2}".format(t.tm_hour, t.tm_min, t.tm_sec)
        c = COLORS[hex]
        self.layout.fill(c)

        self._step = 0
