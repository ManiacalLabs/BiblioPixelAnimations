# Author: Daniel Ternes
# More Info: http://forum.maniacallabs.com/showthread.php?tid=6


from bibliopixel.animation import BaseStripAnim
from bibliopixel import colors
import time
import calendar


class BEClock(BaseStripAnim):

    """Binary Epoch Clock"""

    def __init__(self, layout, onColor=colors.Red, offColor=colors.Off,
                 bitWidth=1, bitSpace=1, reverse=False):
        super(BEClock, self).__init__(layout, 0, 0)
        self._onColor = onColor
        self._offColor = offColor
        self._bitWidth = bitWidth - 1
        self._bitSpace = bitSpace + 1
        self._reverse = reverse

    def step(self, amt=1):
        z = calendar.timegm(time.gmtime(time.time()))

        if self._reverse:
            for i in range(32):
                if (z & (1 << i)) > 0:
                    self.layout.fill(self._onColor, (self._bitSpace + self._bitWidth) * (
                        31 - i), ((self._bitSpace + self._bitWidth) * (31 - i)) + self._bitWidth)
                else:
                    self.layout.fill(self._offColor, (self._bitSpace + self._bitWidth) * (
                        31 - i), ((self._bitSpace + self._bitWidth) * (31 - i)) + self._bitWidth)
        else:
            for i in range(32):
                if (z & (1 << i)) > 0:
                    self.layout.fill(self._onColor, (self._bitSpace + self._bitWidth) * i, ((self._bitSpace + self._bitWidth) * i) + self._bitWidth)
                else:
                    self.layout.fill(self._offColor, (self._bitSpace + self._bitWidth) * i, ((self._bitSpace + self._bitWidth) * i) + self._bitWidth)

        self._step = 0
