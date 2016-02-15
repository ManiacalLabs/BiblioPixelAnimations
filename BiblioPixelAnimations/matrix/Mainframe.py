from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors
from bibliopixel.util import genVector

import math
import os


class Mainframe(BaseMatrixAnim):

    def __init__(self, led, scroll = True, color = colors.Red, bgcolor = colors.Off):
        super(Mainframe, self).__init__(led)
        self.color = color
        self.bgcolor = bgcolor
        self.scroll = scroll
        self.rand_bytes_rows = (self.height / 8) + 1
        self.__genBytes()

    def __genBytes(self):
        self.bytes = [[x for x in bytearray(os.urandom(self.width))]
                      for y in range(self.rand_bytes_rows)]

    def __getBit(self, x, y):
        b = self.bytes[y / 8][x]
        return bool(b & (1 << (y % 8)))

    def step(self, amt=8):
        if self.scroll:
            new_bytes = [i for i in bytearray(os.urandom(self.rand_bytes_rows))]
            for y in range(self.rand_bytes_rows):
                self.bytes[y].pop(0)
                self.bytes[y].append(new_bytes[y])
        else:
            self.__genBytes()

        for y in range(self.height):
            for x in range(self.width):
                self._led.set(self.width - x - 1, y, self.color if self.__getBit(x, y) else self.bgcolor)


# MANIFEST = [
#     {
#         "class": Bloom,
#         "controller": "matrix",
#         "desc": "Rainbow blooming animation.",
#         "display": "Bloom",
#         "id": "Bloom",
#         "params": [
#             {
#                 "default": True,
#                 "help": "On for bloom in, off for bloom out.",
#                 "id": "dir",
#                 "label": "Direction",
#                 "type": "bool"
#             }
#         ],
#         "type": "animation"
#     }
# ]
