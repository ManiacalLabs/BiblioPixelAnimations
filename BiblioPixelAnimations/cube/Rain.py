from bibliopixel.animation import BaseCubeAnim
import bibliopixel.colors as colors
import random


class RainBow(BaseCubeAnim):

    def __init__(self, layout, tail=4, growthRate=12):
        super(RainBow, self).__init__(layout)
        self._tail = tail
        self._drops = [[[] for z in range(self.z)] for x in range(self.x)]
        self._growthRate = growthRate

    def pre_run(self):
        self._step = 0

    def _drawDrop(self, x, y, z, color):
        for i in range(self._tail):
            if y - i >= 0 and y - i < self.y:
                level = 255 - ((255 // self._tail) * i)
                self.layout.set(x, y - i, z, colors.color_scale(color, level))

    def step(self, amt=1):
        self.layout.all_off()

        for i in range(self._growthRate):
            x = random.randint(0, self.x - 1)
            z = random.randint(0, self.z - 1)
            self._drops[x][z].append(0)

        for x in range(self.x):
            for z in range(self.z):
                col = self._drops[x][z]
                if len(col) > 0:
                    removals = []
                    for y in range(len(col)):
                        drop = col[y]
                        if drop < self.y:
                            self._drawDrop(x, drop, z, colors.hue2rgb(
                                drop * (255 // self.y)))
                        if drop - (self._tail - 1) < self.y:
                            drop = drop + 1
                            self._drops[x][z][y] = drop
                        else:
                            removals.append(drop)
                    for r in removals:
                        self._drops[x][z].remove(r)

        self._step = 0
