from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors

import os


class Mainframe(BaseMatrixAnim):

    def __init__(self, led, scroll=True, color=colors.Red, bgcolor=colors.Off):
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
            new_bytes = [i for i in bytearray(
                os.urandom(self.rand_bytes_rows))]
            for y in range(self.rand_bytes_rows):
                self.bytes[y].pop(0)
                self.bytes[y].append(new_bytes[y])
        else:
            self.__genBytes()

        for y in range(self.height):
            for x in range(self.width):
                self._led.set(self.width - x - 1, y,
                              self.color if self.__getBit(x, y) else self.bgcolor)


MANIFEST = [
    {
        "class": Mainframe,
        "controller": "matrix",
        "desc": "90's Computer Mainframe random blinking lights",
        "display": "Mainframe",
        "id": "Mainframe",
        "params": [
            {
                "default": True,
                "help": "Move and random",
                "id": "scroll",
                "label": "Scroll",
                "type": "bool"
            },
            {
                "default": [
                    0,
                    0,
                    0
                ],
                "help": "",
                "id": "bgcolor",
                "label": "Background",
                "type": "color"
            },
            {
                "default": [
                    255,
                    0,
                    0
                ],
                "help": "Random pixel color",
                "id": "color",
                "label": "Color",
                "type": "color"
            }
        ],
        "type": "animation"
    }
]
