from bibliopixel import *
from bibliopixel.animation import *

import psutil
from collections import deque
class CPUUsage(BaseMatrixAnim):

    def __init__(self, led, onColor):
        super(CPUUsage, self).__init__(led)
        self._onColor = onColor

        self._usage = deque(iterable=[0]*self.width, maxlen=self.width)

    def step(self, amt = 1):
        self._internalDelay = 500
        self._led.all_off()
        usage = psutil.cpu_percent()
        self._usage.append(int(usage/100.0*self.height))

        for x in range(self.width):
            if self._usage[x] > 0:
                self._led.drawLine(x, self.height, x, self.height-1-self._usage[x], self._onColor)



MANIFEST = [
    {
        "class": CPUUsage,
        "controller": "matrix",
        "desc": "Displays scrolling CPU usage graph.",
        "display": "CPUUsage",
        "id": "CPUUsage",
        "params": [
            {
                "default": [255, 0, 0],
                "help": "", 
                "id": "onColor",
                "label": "Graph Color",
                "type": "color"
            }
        ],
        "type": "animation"
    }
]
