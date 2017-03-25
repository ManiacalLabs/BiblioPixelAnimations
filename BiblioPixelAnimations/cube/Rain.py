from bibliopixel.animation import BaseCubeAnim
import bibliopixel.colors as colors
import random


# class MatrixRain(BaseMatrixAnim):
#     # TODO: Upgrade back to use multiple colors when supported by UI
#
#     def __init__(self, led, rain_colors=colors.Green, tail=4, growthRate=4):
#         super(MatrixRain, self).__init__(led)
#         if not isinstance(rain_colors, list):
#             rain_colors = [rain_colors]
#         self._colors = rain_colors
#         self._tail = tail
#         self._drops = [[] for x in range(self._led.width)]
#         self._growthRate = growthRate
#
#     def _drawDrop(self, x, y, color):
#         for i in range(self._tail):
#             if y - i >= 0 and y - i < self._led.height:
#                 level = 255 - ((255 / self._tail) * i)
#                 self._led.set(x, y - i, colors.color_scale(color, level))
#
#     def step(self, amt=1):
#         self._led.all_off()
#
#         for i in range(self._growthRate):
#             newDrop = random.randint(0, self._led.width - 1)
#             cInt = random.randint(0, len(self._colors) - 1)
#             self._drops[newDrop].append((0, self._colors[cInt]))
#
#         for x in range(self._led.width):
#             col = self._drops[x]
#             if len(col) > 0:
#                 removals = []
#                 for y in range(len(col)):
#                     drop = col[y]
#                     if drop[0] < self._led.height:
#                         self._drawDrop(x, drop[0], drop[1])
#                     if drop[0] - (self._tail - 1) < self._led.height:
#                         drop = (drop[0] + 1, drop[1])
#                         self._drops[x][y] = drop
#                     else:
#                         removals.append(drop)
#                 for r in removals:
#                     self._drops[x].remove(r)
#
#         self._step = 0


class RainBow(BaseCubeAnim):

    def __init__(self, led, tail=4, growthRate=12):
        super(RainBow, self).__init__(led)
        self._tail = tail
        self._drops = [[[] for z in range(self.z)] for x in range(self.x)]
        self._growthRate = growthRate

    def _drawDrop(self, x, y, z, color):
        for i in range(self._tail):
            if y - i >= 0 and y - i < self.y:
                level = 255 - ((255 // self._tail) * i)
                self._led.set(x, y - i, z, colors.color_scale(color, level))

    def step(self, amt=1):
        self._led.all_off()

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
