# Author: Daniel Ternes
# More Info: http://forum.maniacallabs.com/showthread.php?tid=6


class BEClock(BaseStripAnim):

    """Binary Epoch Clock"""

    def __init__(self, led, onColor, offColor, bitWidth, bitSpace, reverse):
        super(BEClock, self).__init__(led, 0, 0)
        self._onColor = onColor
        self._offColor = offColor
        self._bitWidth = bitWidth
        self._bitSpace = bitSpace
        self._reverse = reverse

    def step(self, amt=1):
        z = calendar.timegm(time.gmtime(time.time()))

        if self._reverse:
            for i in range(32):
                if (z & (1 << i)) > 0:
                    self._led.fill(self._onColor, (self._bitSpace + self._bitWidth) * (
                        31 - i), ((self._bitSpace + self._bitWidth) * (31 - i)) + self._bitWidth)
                else:
                    self._led.fill(self._offColor, (self._bitSpace + self._bitWidth) * (
                        31 - i), ((self._bitSpace + self._bitWidth) * (31 - i)) + self._bitWidth)
        else:
            for i in range(32):
                if (z & (1 << i)) > 0:
                    self._led.fill(self._onColor, (self._bitSpace + self._bitWidth) * i, ((self._bitS​pace + self._bitWidth) * i) + self._bitWidth)
                else:
                    self._led.fill(self._offColor, (self._bitSpace + self._bitWidth) * i, ((self._bit​Space + self._bitWidth) * i) + self._bitWidth)

        self._step = 0
