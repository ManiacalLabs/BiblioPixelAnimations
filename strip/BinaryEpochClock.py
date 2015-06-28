# Author: Daniel Ternes
# More Info: http://forum.maniacallabs.com/showthread.php?tid=6

from bibliopixel.animation import *
import calendar

class BEClock(BaseStripAnim):

    """Binary Epoch Clock"""

    def __init__(self, led, onColor, offColor, bitWidth, bitSpace, reverse):
        super(BEClock, self).__init__(led, 0, 0)
        self._onColor = onColor
        self._offColor = offColor
        self._bitWidth = bitWidth-1
        self._bitSpace = bitSpace+1
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
                    self._led.fill(self._onColor, (self._bitSpace + self._bitWidth) * i, ((self._bitSpace + self._bitWidth) * i) + self._bitWidth)
                else:
                    self._led.fill(self._offColor, (self._bitSpace + self._bitWidth) * i, ((self._bitSpace + self._bitWidth) * i) + self._bitWidth)

        self._step = 0
		
MANIFEST = [
        {
            "id":"BEClock",
            "class":BEClock,
            "type": "animation",
            "display": "Binary Epoch Clock",
            "controller": "strip",
            "desc": "Turn a string of LEDs into a giant Binary Epoch clock",
            "params": [{
                "id": "onColor",
                "label": "On Color",
                "type": "color",
                "default": (0,255,0),
                "help":"Color representing a 'on' LED (binary '1')."
            },{
                "id": "offColor",
                "label": "Off Color",
                "type": "color",
                "default": (255,0,0),
                "help":"Color representing a 'off' LED (binary '0')."
            },{
                "id": "bitWidth",
                "label": "Bit Width",
                "type": "int",
                "min": 1,
                "default": 1,
                "help":"How many pixels are used to per 'light'."
            },{
                "id": "bitSpace",
                "label": "Bit Space",
                "type": "int",
                "min": 0,
                "default": 0,
                "help":"How many empty pixels are between each 'light'."
            },{
                "id": "reverse",
                "label": "Reverse Order",
                "type": "bool",
                "default": False,
                "help":"Reverse the order of the clock on the strip."
            },]
        },
]
