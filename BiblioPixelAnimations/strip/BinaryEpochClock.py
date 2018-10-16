# Author: Daniel Ternes
# More Info: http://forum.maniacallabs.com/showthread.php?tid=6


from bibliopixel.animation import BaseStripAnim
from bibliopixel import colors
import time
import calendar


class BEClock(BaseStripAnim):
    COLOR_DEFAULTS = ('offColor', colors.Off), ('onColor', colors.Red)

    """Binary Epoch Clock"""

    def __init__(self, layout, bitWidth=1, bitSpace=1, reverse=False, **kwds):
        super().__init__(layout, 0, 0, **kwds)
        self._bitWidth = bitWidth - 1
        self._bitSpace = bitSpace + 1
        self._reverse = reverse

    def step(self, amt=1):
        z = calendar.timegm(time.gmtime(time.time()))

        for i in range(32):
            color = self.palette((z & (1 << i)) > 0)
            if self._reverse:
                i = 31 - i

            start = (self._bitSpace + self._bitWidth) * i
            self.layout.fill(color, start, start + self._bitWidth)

        self._step = 0
