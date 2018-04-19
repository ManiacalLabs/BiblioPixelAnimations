from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors
import os


class Mainframe(BaseMatrixAnim):

    def __init__(self, layout, scroll=True, color=colors.Red, bgcolor=colors.Off):
        super(Mainframe, self).__init__(layout)
        self.color = color
        self.bgcolor = bgcolor
        self.scroll = scroll
        self.rand_bytes_rows = (self.height // 8) + 1
        self.__genBytes()

    def __genBytes(self):
        self.bytes = [[x for x in bytearray(os.urandom(self.width))]
                      for y in range(self.rand_bytes_rows)]

    def __getBit(self, x, y):
        b = self.bytes[y // 8][x]
        return bool(b & (1 << (y % 8)))

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
                self.layout.set(self.width - x - 1, y,
                                self.color if self.__getBit(x, y) else self.bgcolor)
