from bibliopixel.animation.cube import BaseCubeAnim
import bibliopixel.colors as colors
from collections import deque
import random
import copy
import time
import itertools


class Table:

    def __init__(self, width, height, depth, rand_max, table=None):
        self.toroidal = True
        self._rand_max = rand_max
        if table:
            self.table = table
            self.depth = len(table)
            self.height = len(table[0])
            self.width = len(table[0][0])
        else:
            self.height = height
            self.width = width
            self.depth = depth
            self.genNewTable()

        self._oldStates = deque()
        for i in range(3):
            self._oldStates.append([])

        self.offsets = list(itertools.product([-1, 0, 1], repeat=3))
        self.offsets.remove((0, 0, 0))  # remove center point

    def genNewTable(self):
        self.table = []

        random.seed(time.time())
        for z in range(self.depth):
            self.table.append([])
            for y in range(0, self.height):
                self.table[z].append([])
                for x in range(0, self.width):
                    rand = random.randint(0, self._rand_max)
                    if rand == 0:
                        self.table[z][y].append(1)
                    else:
                        self.table[z][y].append(0)

    def liveNeighbours(self, z, y, x):
        """Returns the number of live neighbours."""
        count = 0

        for oz, oy, ox in self.offsets:
            cz, cy, cx = z + oz, y + oy, x + ox
            if cz >= self.depth:
                cz = 0
            if cy >= self.height:
                cy = 0
            if cx >= self.width:
                cx = 0
            count += self.table[cz][cy][cx]

        # if self.toroidal:
        #     if y == 0:
        #         if self.table[self.height - 1][x]:
        #             count = count + 1
        #     if y == self.height - 1:
        #         if self.table[0][x]:
        #             count = count + 1
        #     if x == 0:
        #         if self.table[y][self.width - 1]:
        #             count = count + 1
        #     if x == self.width - 1:
        #         if self.table[y][0]:
        #             count = count + 1

        return count

    def turn(self):
        """Turn"""
        r = (4, 5, 5, 5)
        nt = copy.deepcopy(self.table)
        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    neighbours = self.liveNeighbours(z, y, x)
                    if self.table[z][y][x] == 0 and (neighbours > r[0] and neighbours <= r[1]):
                        nt[z][y][x] = 1
                    elif self.table[z][y][x] == 1 and (neighbours > r[2] and neighbours < r[3]):
                        nt[z][y][x] = 0

        self._oldStates.append(self.table)
        if len(self._oldStates) > 3:
            self._oldStates.popleft()

        self.table = nt

    def checkStable(self):
        for t in self._oldStates:
            if self.table == t:
                return True
        return False


class CubeGameOfLife(BaseCubeAnim):

    def __init__(self, layout, color=colors.Red, bg=colors.Off, toroidal=False):
        super().__init__(layout)

        self._color = color
        self._bg = bg
        self._table = Table(self.x, self.y, self.z, 1, None)
        self._table.toroidal = toroidal

        self._finishCount = 0

    def stepTable(self):
        x, y, z = 0, 0, 0
        for t_z in self._table.table:
            for t_y in t_z:
                for t_x in t_y:
                    if t_x == 0:
                        self.layout.set(x, y, z, self._bg)
                    else:
                        self.layout.set(x, y, z, self._color)
                    # print(x, y, z)
                    x = x + 1
                y = y + 1
                x = 0
            z = z + 1
            y = 0

        self._table.turn()

    def step(self, amt=1):

        self.stepTable()
        if self._table.checkStable():
            self._finishCount += 1
            if self._finishCount > 10:
                self._table.genNewTable()
                self._finishCount = 0
                self.animComplete = True

        self._step = 0
