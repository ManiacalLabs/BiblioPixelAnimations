import random
import time
import copy
from collections import deque

from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors

class Table:

    def __init__(self, height, width, rand_max, table=None):
        self.toroidal = True
        self._rand_max = rand_max
        if table:
            self.table = table
            self.height = len(table)
            self.width = len(table[0])
        else:
            self.height = height
            self.width = width
            self.genNewTable()

        self._oldStates = deque()
        for i in range(3):
            self._oldStates.append([])

    def genNewTable(self):
        self.table = []

        random.seed(time.time())
        for y in range(0,self.height):
            self.table.append([])
            for x in range(0,self.width):
                rand = random.randint(0,self._rand_max)
                if rand == 0:
                    self.table[y].append(1)
                else:
                    self.table[y].append(0)

    def liveNeighbours(self, y, x):
        """Returns the number of live neighbours."""
        count = 0
        if y > 0:
            if self.table[y-1][x]:
                count = count + 1
            if x > 0:
                if self.table[y-1][x-1]:
                    count = count + 1
            if self.width > (x + 1):
                if self.table[y-1][x+1]:
                    count = count + 1

        if x > 0:
            if self.table[y][x-1]:
                count = count + 1
        if self.width > (x + 1):
            if self.table[y][x+1]:
                count = count + 1

        if self.height > (y + 1):
            if self.table[y+1][x]:
                count = count + 1
            if x > 0:
                if self.table[y+1][x-1]:
                    count = count + 1
            if self.width > (x + 1):
                if self.table[y+1][x+1]:
                    count = count + 1

        if self.toroidal:
            if y == 0:
                if self.table[self.height-1][x]:
                    count = count + 1
            if y == self.height-1:
                if self.table[0][x]:
                    count = count + 1
            if x == 0:
                if self.table[y][self.width-1]:
                    count = count + 1
            if x == self.width-1:
                if self.table[y][0]:
                    count = count + 1

        return count

    def turn(self):
        """Turn"""
        nt = copy.deepcopy(self.table)
        #nt = list(self.table)
        for y in range(0, self.height):
            for x in range(0, self.width):
                neighbours = self.liveNeighbours(y, x)
                if self.table[y][x] == 0:
                    if neighbours == 3:
                        nt[y][x] = 1
                else:
                    if (neighbours < 2) or (neighbours > 3):
                        nt[y][x] = 0

        self._oldStates.append(self.table)
        if len(self._oldStates) > 3:
            self._oldStates.popleft()

        self.table = nt

    def checkStable(self):
        for t in self._oldStates:
            if self.table == t:
                return True
        return False

class GameOfLife(BaseMatrixAnim):
    def __init__(self, led, color = colors.Red, bg = colors.Off, toroidal = False):
        super(GameOfLife, self).__init__(led)

        self._color = color
        self._bg = bg
        self._table = Table(self._led.height, self._led.width, 1, None)
        self._table.toroidal = toroidal

        self._finishCount = 0

    def stepTable(self):
        x = 0
        y = 0
        for row in self._table.table:
            for col in row:
                if col == 0:
                    self._led.set(x, y, self._bg)
                else:
                    self._led.set(x, y, self._color)
                x = x + 1
            y = y + 1
            x = 0

        self._table.turn()

    def step(self, amt = 1):

        self.stepTable()
        if self._table.checkStable():
            self._finishCount += 1
            if self._finishCount > 10:
                self._table.genNewTable()
                self._finishCount = 0

        self._step = 0

class GameOfLifeRGB(BaseMatrixAnim):
    def __init__(self, led, toroidal = True):
        super(GameOfLifeRGB, self).__init__(led)

        self._tableR = Table(self._led.height, self._led.width, 1, None)
        self._tableR.toroidal = toroidal

        self._tableG = Table(self._led.height, self._led.width, 1, None)
        self._tableG.toroidal = toroidal

        self._tableB = Table(self._led.height, self._led.width, 1, None)
        self._tableB.toroidal = toroidal

    def stepTables(self):
        x = 0
        y = 0
        for row in range(self._tableR.height):
            for col in range(self._tableR.width):
                r = (self._tableR.table[row][col]) * 255
                g = (self._tableG.table[row][col]) * 255
                b = (self._tableB.table[row][col]) * 255

                c = (r, g, b)
                self._led.set(x, y, c)

                x = x + 1
            y = y + 1
            x = 0

        self._tableR.turn()
        self._tableG.turn()
        self._tableB.turn()

    def doStableCheck(self, table):
        if table.checkStable():
            table.genNewTable()

    def step(self, amt = 1):

        self.stepTables()
        self.doStableCheck(self._tableR)
        self.doStableCheck(self._tableG)
        self.doStableCheck(self._tableB)
        self._step = 0


MANIFEST = [
        {
            "id":"GameOfLife",
            "class":GameOfLife,
            "type": "animation",
            "display": "Game of Life",
            "controller": "matrix",
            "desc": "Conway's Game of Life",
            "params": [{
                "id": "color",
                "label": "Color",
                "type": "color",
                "default": (255,0,0),
                "help":"Color of simulation cells."
            },{
                "id": "bg",
                "label": "Background Color",
                "type": "color",
                "default": (0,0,0),
                "help":"Color of simulation background."
            },{
                "id": "toroidal",
                "label": "Toroidal",
                "type": "bool",
                "default": False,
                "help":"Wrap similation around edges like a toroid (donut shape)."
            },]
        },
        {
            "id":"GameOfLifeRGB",
            "class":GameOfLifeRGB,
            "type": "animation",
            "display": "Game of Life RGB",
            "controller": "matrix",
            "desc": "Conway's Game of Life running three separate simulations, one on each color channel.",
            "params": [{
                "id": "toroidal",
                "label": "Toroidal",
                "type": "bool",
                "default": False,
                "help":"Wrap similation around edges like a toroid (donut shape)."
            },]
        }
]
