# Scalable Binary (BCD) Clock
# By: Dan (www.maniacallabs.com)

from bibliopixel.animation import BaseMatrixAnim
from bibliopixel import colors
import time


class MatrixBinaryClock(BaseMatrixAnim):

    def __init__(self, layout, onColor=colors.Red, offColor=colors.Blue,
                 origX=0, origY=0, lightSize=1, colSpacing=1):
        super(MatrixBinaryClock, self).__init__(layout)
        self._onColor = onColor
        self._offColor = offColor
        self._origX = origX
        self._origY = origY
        self._lightSize = lightSize
        self._colSpacing = colSpacing
        if self._lightSize < 1:
            self._lightSize = 1

    def step(self, amt=1):
        self.layout.all_off()

        a = "" + time.ctime()
        tIndex = [11, 12, 14, 15, 17, 18]
        colSize = [2, 4, 3, 4, 3, 4]

        for x in range(6):
            b = bin(128 + int(a[tIndex[x]]))
            for i in range(colSize[x]):
                self.layout.fillRect(
                    self._origX + (x) + (self._lightSize - 1) * x + self._colSpacing * x,
                    ((4 - colSize[x]) + i + self._origY) * self._lightSize,
                    self._lightSize, self._lightSize,
                    self._offColor if b[6 + (4 - colSize[x]) + i] == '0' else self._onColor)

        self._step = 0
