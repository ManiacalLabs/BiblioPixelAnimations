from bibliopixel.animation import BaseMatrixAnim
from bibliopixel import colors
import random


class LangtonsAnt(BaseMatrixAnim):

    def __init__(self, layout, antColor=colors.Green, pathColor=colors.Red):
        super(LangtonsAnt, self).__init__(layout)
        self.antColor = tuple(antColor)
        self.pathColor = tuple(pathColor)
        self.offColor = colors.Off
        self.curColor = self.offColor

    def preRun(self):
        self.x = random.randrange(self.width)
        self.y = random.randrange(self.height)
        self.d = random.randrange(4)

    def __rollValue(self, val, step, min, max):
        val += step
        if val < min:
            diff = min - val
            val = max - diff + 1
        elif val > max:
            diff = val - max
            val = min + diff - 1
        return val

    def __changeDir(self, dir):
        if dir:
            dir = 1
        else:
            dir = -1
        self.d = self.__rollValue(self.d, dir, 0, 3)

    def __moveAnt(self):
        if self.d == 0:
            self.y = self.__rollValue(self.y, 1, 0, self.height - 1)
        elif self.d == 1:
            self.x = self.__rollValue(self.x, 1, 0, self.width - 1)
        elif self.d == 2:
            self.y = self.__rollValue(self.y, -1, 0, self.height - 1)
        elif self.d == 3:
            self.x = self.__rollValue(self.x, -1, 0, self.width - 1)

        self.curColor = self.layout.get(self.x, self.y)
        self.layout.set(self.x, self.y, self.antColor)

    def step(self, amt=1):
        if self.curColor == self.pathColor:
            self.layout.set(self.x, self.y, self.offColor)
            self.__changeDir(False)
            self.__moveAnt()
        else:
            self.layout.set(self.x, self.y, self.pathColor)
            self.__changeDir(True)
            self.__moveAnt()


class LangtonsAntRainbow(BaseMatrixAnim):

    def __init__(self, layout, antColor=colors.White):
        super(LangtonsAntRainbow, self).__init__(layout)
        self.color_cycle = [colors.Red, colors.Orange,
                            colors.Yellow, colors.Green,
                            colors.Blue, colors.Violet]
        self.antColor = tuple(antColor)
        self.offColor = colors.Off
        self.curColor = self.offColor
        self.curColorIndex = -1

    def preRun(self):
        self.x = random.randrange(self.width)
        self.y = random.randrange(self.height)
        self.d = random.randrange(4)

    def __rollValue(self, val, step, min, max):
        val += step
        if val < min:
            diff = min - val
            val = max - diff + 1
        elif val > max:
            diff = val - max
            val = min + diff - 1
        return val

    def __changeDir(self, dir):
        if dir:
            dir = 1
        else:
            dir = -1
        self.d = self.__rollValue(self.d, dir, 0, 3)

    def __moveAnt(self):
        if self.d == 0:
            self.y = self.__rollValue(self.y, 1, 0, self.height - 1)
        elif self.d == 1:
            self.x = self.__rollValue(self.x, 1, 0, self.width - 1)
        elif self.d == 2:
            self.y = self.__rollValue(self.y, -1, 0, self.height - 1)
        elif self.d == 3:
            self.x = self.__rollValue(self.x, -1, 0, self.width - 1)

        self.curColor = self.layout.get(self.x, self.y)
        if self.curColor == self.offColor:
            i = 0
        else:
            i = self.color_cycle.index(self.curColor)
            i += 1
            i %= len(self.color_cycle)

        self.curColor = self.color_cycle[i]
        self.curColorIndex = i
        self.layout.set(self.x, self.y, self.antColor)

    def step(self, amt=1):
        self.layout.set(self.x, self.y, self.curColor)
        if self.curColorIndex % 2 == 0:
            self.__changeDir(False)
            self.__moveAnt()
        else:
            self.__changeDir(True)
            self.__moveAnt()
