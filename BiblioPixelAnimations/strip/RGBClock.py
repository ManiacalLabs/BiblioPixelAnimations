from bibliopixel.animation import BaseStripAnim
import bibliopixel.colors as colors

import time
class RGBClock(BaseStripAnim):
    """RGB Clock done with RGB LED strip(s)"""

    def __init__(self, led, hStart, hEnd, mStart, mEnd, sStart, sEnd):
        super(RGBClock, self).__init__(led, 0, -1)
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


    def step(self, amt = 1):
        t = time.localtime()

        r, g, b = colors.hue2rgb_rainbow(t.tm_hour * (256/24))
        self._led.fillRGB(r,g,b,self._hStart,self._hEnd)

        r, g, b = colors.hue2rgb_rainbow(t.tm_min * (256/60))
        self._led.fillRGB(r,g,b,self._mStart,self._mEnd)

        r, g, b = colors.hue2rgb_rainbow(t.tm_sec * (256/60))
        self._led.fillRGB(r,g,b,self._sStart,self._sEnd)

        self._step = 0



MANIFEST = [
    {
        "class": RGBClock,
        "controller": "strip",
        "desc": "Color Clock",
        "display": "RGBClock",
        "id": "RGBClock",
        "params": [
            {
                "default": None,
                "help": "",
                "id": "hStart",
                "label": "Hour Start Pixel",
                "type" : "int"
            },
            {
                "default": None,
                "help": "",
                "id": "hEnd",
                "label": "Hour End Pixel",
                "type" : "int"
            },
            {
                "default": None,
                "help": "",
                "id": "mStart",
                "label": "Min Start Pixel",
                "type" : "int"
            },
            {
                "default": None,
                "help": "",
                "id": "mEnd",
                "label": "Minute End Pixel",
                "type" : "int"
            },
            {
                "default": None,
                "help": "",
                "id": "sStart",
                "label": "Sec Start Pixel",
                "type" : "int"
            },
            {
                "default": None,
                "help": "",
                "id": "sEnd",
                "label": "Sec End Pixel", 
                "type" : "int"
            }
        ],
        "type": "animation"
    }
]
