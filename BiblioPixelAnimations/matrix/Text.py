from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors

class ScrollText(BaseMatrixAnim):

    def __init__(self, led, text, xPos = 0, yPos = 0, color = colors.White, bgcolor = colors.Off, size = 1):
        super(ScrollText, self).__init__(led)
        self.bgcolor = bgcolor
        self.color = color
        self._text = text
        self.xPos = xPos
        self.yPos = yPos
        self._osize = size
        if size > 0:
            self._dim = 6, 8
        else:
            self._dim = 4, 6
            size = 1
        self._size = size
        self._strW = len(text)*self._dim[0]*size

    def step(self, amt = 1):
        self._led.all_off()
        self._led.drawText(self._text, self.xPos, self.yPos, color = self.color, bg = self.bgcolor, size = self._osize)
        self.xPos -= amt
        if self.xPos + self._strW <= 0:
            self.xPos = self.startX + self.width - 1
            self.animComplete = True

        self._step = 0

class BounceText(BaseMatrixAnim):

    def __init__(self, led, text, xPos = 0, yPos = 0, buffer = 0, color = colors.White, bgcolor = colors.Off, size = 1):
        super(BounceText, self).__init__(led)
        self.color = color
        self.bgcolor = bgcolor
        self._text = text
        self.xPos = xPos
        self.yPos = yPos
        self._osize = size
        if size > 0:
            self._dim = 6, 8
        else:
            self._dim = 4, 6
            size = 1
        self._size = size
        self._strW = len(text)*self._dim[0]*size
        self._dir = -1
        self._buffer = buffer

    def step(self, amt = 1):
        self._led.all_off()
        self._led.drawText(self._text, self.xPos, self.yPos, color = self.color, bg = self.bgcolor, size = self._osize)

        if self._strW < self.width:
            if self.xPos <= 0 + self._buffer and self._dir == -1:
                self._dir = 1
            elif self.xPos + self._strW > self.width - self._buffer  and self._dir == 1:
                self._dir = -1
                self.animComplete = True
        else:
            if self.xPos + self._strW <= self.width - self._buffer  and self._dir == -1:
                self._dir = 1
            elif self.xPos >= 0 + self._buffer and self._dir == 1:
                self._dir = -1
                self.animComplete = True

        self.xPos += amt * self._dir

        self._step = 0



MANIFEST = [
    {
        "class": BounceText,
        "controller": "matrix",
        "desc": None,
        "display": "BounceText",
        "id": "BounceText",
        "params": [
            {
                "default": None,
                "help": "",
                "id": "text",
                "label": "Text",
                "type": "str"
            },
            {
                "default": 1,
                "help": "8x5 Font multipled by this value",
                "id": "size",
                "label": "Text Size",
                "type": "int"
            },
            {
                "default": [
                    0,
                    0,
                    0
                ],
                "help": "",
                "id": "bgcolor",
                "label": "Background Color",
                "type": "color"
            },
            {
                "default": [
                    255,
                    255,
                    255
                ],
                "help": "",
                "id": "color",
                "label": "Text Color",
                "type": "color"
            },
            {
                "default": 0,
                "help": "Distance from edge before bounce.",
                "id": "buffer",
                "label": "Edge Buffer",
                "type": "int"
            },
            {
                "default": 0,
                "help": "",
                "id": "yPos",
                "label": "Y Pos",
                "type": "int"
            },
            {
                "default": 0,
                "help": "",
                "id": "xPos",
                "label": "X Pos",
                "type": "int"
            }

        ],
        "type": "animation"
    },
    {
        "class": ScrollText,
        "controller": "matrix",
        "desc": None,
        "display": "ScrollText",
        "id": "ScrollText",
        "params": [
            {
                "default": None,
                "help": "",
                "id": "text",
                "label": "Text",
                "type": "str"
            },
            {
                "default": 1,
                "help": "8x5 Font multipled by this value",
                "id": "size",
                "label": "Text Size",
                "type": "int"
            },
            {
                "default": [
                    0,
                    0,
                    0
                ],
                "help": "",
                "id": "bgcolor",
                "label": "Background Color",
                "type": "color"
            },
            {
                "default": [
                    255,
                    255,
                    255
                ],
                "help": "",
                "id": "color",
                "label": "Text Color",
                "type": "color"
            },
            {
                "default": 0,
                "help": "",
                "id": "yPos",
                "label": "Y Pos",
                "type": "int"
            },
            {
                "default": 0,
                "help": "",
                "id": "xPos",
                "label": "X Pos",
                "type": "int"
            }
        ],
        "type": "animation"
    }
]
