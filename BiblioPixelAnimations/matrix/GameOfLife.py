import random
import copy
from collections import deque
import time
from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors
from bibliopixel import log
from bibliopixel import font
import threading


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
        for y in range(0, self.height):
            self.table.append([])
            for x in range(0, self.width):
                rand = random.randint(0, self._rand_max)
                if rand == 0:
                    self.table[y].append(1)
                else:
                    self.table[y].append(0)

    def liveNeighbours(self, y, x):
        """Returns the number of live neighbours."""
        count = 0
        if y > 0:
            if self.table[y - 1][x]:
                count = count + 1
            if x > 0:
                if self.table[y - 1][x - 1]:
                    count = count + 1
            if self.width > (x + 1):
                if self.table[y - 1][x + 1]:
                    count = count + 1

        if x > 0:
            if self.table[y][x - 1]:
                count = count + 1
        if self.width > (x + 1):
            if self.table[y][x + 1]:
                count = count + 1

        if self.height > (y + 1):
            if self.table[y + 1][x]:
                count = count + 1
            if x > 0:
                if self.table[y + 1][x - 1]:
                    count = count + 1
            if self.width > (x + 1):
                if self.table[y + 1][x + 1]:
                    count = count + 1

        if self.toroidal:
            if y == 0:
                if self.table[self.height - 1][x]:
                    count = count + 1
            if y == self.height - 1:
                if self.table[0][x]:
                    count = count + 1
            if x == 0:
                if self.table[y][self.width - 1]:
                    count = count + 1
            if x == self.width - 1:
                if self.table[y][0]:
                    count = count + 1

        return count

    def turn(self):
        """Turn"""
        nt = copy.deepcopy(self.table)
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

    def __init__(self, layout, color=colors.Red, bg=colors.Off, toroidal=False):
        super(GameOfLife, self).__init__(layout)

        self._color = color
        self._bg = bg

        self.toroidal = toroidal

        self._finishCount = 0

    def pre_run(self):
        self._table = Table(self.layout.height, self.layout.width, 1, None)
        self._table.toroidal = self.toroidal

    def stepTable(self):
        x = 0
        y = 0
        for row in self._table.table:
            for col in row:
                if col == 0:
                    self.layout.set(x, y, self._bg)
                else:
                    self.layout.set(x, y, self._color)
                x = x + 1
            y = y + 1
            x = 0

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


class GameOfLifeRGB(BaseMatrixAnim):

    def __init__(self, layout, toroidal=True):
        super(GameOfLifeRGB, self).__init__(layout)

        self.toroidal = toroidal

    def pre_run(self):
        self._tableR = Table(self.layout.height, self.layout.width, 1, None)
        self._tableR.toroidal = self.toroidal
        time.sleep(0.01)

        self._tableG = Table(self.layout.height, self.layout.width, 1, None)
        self._tableG.toroidal = self.toroidal
        time.sleep(0.01)

        self._tableB = Table(self.layout.height, self.layout.width, 1, None)
        self._tableB.toroidal = self.toroidal

    def stepTables(self):
        x = 0
        y = 0
        for row in range(self._tableR.height):
            for col in range(self._tableR.width):
                r = (self._tableR.table[row][col]) * 255
                g = (self._tableG.table[row][col]) * 255
                b = (self._tableB.table[row][col]) * 255

                c = (r, g, b)
                self.layout.set(x, y, c)

                x = x + 1
            y = y + 1
            x = 0

        self._tableR.turn()
        self._tableG.turn()
        self._tableB.turn()

    def doStableCheck(self, table):
        if table.checkStable():
            table.genNewTable()

    def step(self, amt=1):

        self.stepTables()
        self.doStableCheck(self._tableR)
        self.doStableCheck(self._tableG)
        self.doStableCheck(self._tableB)
        self._step = 0


class GameOfLifeClock(BaseMatrixAnim):

    def __init__(self, layout, font_name='16x8', mil_time=False):
        super(GameOfLifeClock, self).__init__(layout)
        self.font_name = font_name
        self.mil_time = mil_time
        self.scale = 1
        self.steady_time = 2000
        self.history = None
        self.next_history = None
        self.next_thread = None
        self.next_ready = False

        # Find the text size
        while True:
            x, y = font.str_dim('00:00', font=self.font_name,
                                font_scale=self.scale, final_sep=False)
            if x > self.width or y > self.height:
                self.scale -= 1
                break
            self.scale += 1

        # create a time frame while we wait
        self.init_frame = self.create_time_table(int(time.time()))

    def create_time_table(self, t):
        t = time.localtime(t)
        hr = t.tm_hour
        if not self.mil_time:
            hr = hr % 12
        hrs = str(hr).zfill(2)
        mins = str(t.tm_min).zfill(2)
        val = hrs + ":" + mins
        w, h = font.str_dim(val, font=self.font_name,
                            font_scale=self.scale, final_sep=False)
        x = (self.width - w) // 2
        y = (self.height - h) // 2
        old_buf = copy.copy(self.layout.colors)
        self.layout.all_off()
        self.layout.drawText(val, x, y, color=colors.Red,
                             font=self.font_name, font_scale=self.scale)
        table = []
        for y in range(self.height):
            table.append([0] * self.width)
            for x in range(self.width):
                table[y][x] = int(any(self.layout.get(x, y)))
        self.layout.setBuffer(old_buf)
        return table

    def generate_history(self, t, steps):
        history = []
        start = self.create_time_table(t)
        steady_frames = int(self.steady_time // self._sleep)
        steady = steps if steps <= steady_frames else steady_frames
        for _ in range(steady):
            history.append(start)
        gol = Table(self.height, self.width, 1, start)
        for _ in range(steps - steady):
            gol.turn()
            history.append(copy.deepcopy(gol.table))

        return history

    def gen_next(self):
        start = self._msTime()
        t = int(time.time())
        assert self._sleep, "GameOfLifeClock requires a set FPS!"
        self.next_history = self.generate_history(t + 60, 60000 // self._sleep)
        self.next_ready = True
        log.debug("History Generate Time: {}".format(self._msTime() - start))

    def do_gen_next(self):
        if not self.next_thread or not self.next_thread.isAlive():
            self.next_thread = threading.Thread(target=self.gen_next)
            self.next_thread.start()

    def swap_history(self):
        self.history = self.next_history
        self.next_ready = False
        self.do_gen_next()

    def display_frame(self, frame):
        for y in range(self.height):
            for x in range(self.width):
                c = colors.Red if frame[y][x] else colors.Black
                self.layout.set(x, y, c)

    def step(self, amt=1):
        if not self.history and not self.next_ready:
            self.display_frame(self.init_frame)
            if self._sleep:
                self.do_gen_next()
        else:
            if not self.history:
                self.swap_history()
            if len(self.history) > 1:
                self.display_frame(self.history.pop(-1))
            else:
                self.display_frame(self.history[0])
                if self.next_ready:
                    self.swap_history()
