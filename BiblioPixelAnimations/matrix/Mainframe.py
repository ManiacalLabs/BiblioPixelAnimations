from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors
import os


class Mainframe(BaseMatrixAnim):
    COLOR_DEFAULTS = ('bgcolor', colors.Off), ('color', colors.Red)

    def __init__(self, layout, scroll=True):
        super().__init__(layout)
        self.scroll = scroll
        self.rand_bytes_rows = (self.height // 8) + 1
        self.__genBytes()

    def __genBytes(self):
        self.bytes = [[x for x in bytearray(os.urandom(self.width))]
                      for y in range(self.rand_bytes_rows)]

    def step(self, amt=8):
        if self.scroll:
            new_bytes = [i for i in bytearray(
                os.urandom(self.rand_bytes_rows))]
            for y in range(self.rand_bytes_rows):
                self.bytes[y].pop(0)
                self.bytes[y].append(new_bytes[y])
        else:
            self.__genBytes()

        for y in range(self.height):
            for x in range(self.width):
                b = self.bytes[y // 8][x]
                bit = bool(b & (1 << (y % 8)))
                color = self.palette(int(bit))
                self.layout.set(self.width - x - 1, y, color)
