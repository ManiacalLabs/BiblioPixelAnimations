import time
from bibliopixel.animation.strip import Strip


class RGBClock(Strip):
    """RGB Clock done with RGB LED strip(s)"""

    def __init__(self, layout, hStart=0, hEnd=0, mStart=1, mEnd=1, sStart=2,
                 sEnd=2, **kwds):
        super().__init__(layout, 0, -1, **kwds)
        if hEnd < hStart:
            hEnd = hStart + 1
        if mEnd < mStart:
            mEnd = mStart + 1
        if sEnd < sStart:
            sEnd = sStart + 1
        self._hStart = hStart
        self._hEnd = hEnd
        self._mStart = mStart
        self._mEnd = mEnd
        self._sStart = sStart
        self._sEnd = sEnd

    def step(self, amt=1):
        t = time.localtime()

        r, g, b = self.palette(t.tm_hour * (256 // 24))
        self.layout.fillRGB(r, g, b, self._hStart, self._hEnd)

        r, g, b = self.palette(t.tm_min * (256 // 60))
        self.layout.fillRGB(r, g, b, self._mStart, self._mEnd)

        r, g, b = self.palette(t.tm_sec * (256 // 60))
        self.layout.fillRGB(r, g, b, self._sStart, self._sEnd)
