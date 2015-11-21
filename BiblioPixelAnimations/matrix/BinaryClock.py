#Scalable Binary (BCD) Clock
#By: Dan (www.maniacallabs.com)

from bibliopixel import LEDMatrix
from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors

import math
import time
import random

class MatrixBinaryClock(BaseMatrixAnim):

    def __init__(self, led, onColor, offColor, origX, origY, lightSize, colSpacing):
        super(MatrixBinaryClock, self).__init__(led)
        self._onColor = onColor
        self._offColor = offColor
        self._origX = origX
        self._origY = origY
        self._lightSize = lightSize
        self._colSpacing = colSpacing
        if self._lightSize < 1:
            self._lightSize = 1

    def step(self, amt = 1):
        self._led.all_off()

        a = "" + time.ctime()
        tIndex = [11,12,14,15,17,18]
        colSize = [2,4,3,4,3,4]

        for x in range (6):
            b = bin(128+int(a[tIndex[x]]))
            for i in range (colSize[x]):
                self._led.fillRect(
                    self._origX+(x)+(self._lightSize-1)*x+self._colSpacing*x,
                    ((4-colSize[x])+i+self._origY)*self._lightSize,
                    self._lightSize, self._lightSize,
                    self._offColor if b[6+(4-colSize[x])+i] == '0' else self._onColor)

        self._step = 0


MANIFEST = [
    {
        "class": MatrixBinaryClock,
        "controller": "matrix",
        "desc": "Display a BCD Binary clock",
        "display": "MatrixBinaryClock",
        "id": "MatrixBinaryClock",
        "params": [
            {
                "default": [(255,0,0)],
                "help": "Color of On lights",
                "id": "onColor",
                "label": "onColor",
                "type": "color"
            },
            {
                "default": [(0,0,255)],
                "help": "Color of Off lights",
                "id": "offColor",
                "label": "offColor",
                "type": "color"
            },
            {
                "default": 0,
                "help": "Origin (top left) X coordinate",
                "id": "origX",
                "label": "Origin X",
                "type": "int"
            },
            {
                "default": 0,
                "help": "Origin (top left) Y coordinate",
                "id": "origY",
                "label": "Origin Y",
                "type": "int"
            },
            {
                "default": 1,
                "help": "Size of the clock Lights (1=1 pixel, 2=2x2, 3=3x3, etc...)",
                "id": "lightSize",
                "label": "Light Size",
                "type": "int"
            },
            {
                "default": 0,
                "help": "Number of pixels between each column",
                "id": "colSpacing",
                "label": "Column Spacing",
                "type": "int"
            }
        ],
        "type": "animation"
    }
]
