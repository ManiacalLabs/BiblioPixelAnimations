# Author: Adam Haile
# Inspired by http://whatcolourisit.scn9a.org/

import time
from bibliopixel.animation import BaseStripAnim
import bibliopixel.colors as colors


class HEXClock(BaseStripAnim):

    def __init__(self, layout):
        super(HEXClock, self).__init__(layout, 0, -1)

    def step(self, amt=1):
        t = time.localtime()
        hex = "#{0:0>2}{1:0>2}{2:0>2}".format(t.tm_hour, t.tm_min, t.tm_sec)
        c = colors.hex2rgb(hex)
        self.layout.fill(c)

        self._step = 0
