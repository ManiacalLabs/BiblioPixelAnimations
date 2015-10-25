from bibliopixel.animation import BaseStripAnim
import bibliopixel.colors as colors

class LarsonScanner(BaseStripAnim):
    """Larson scanner (i.e. Cylon Eye or K.I.T.T.)."""

    def __init__(self, led, color, tail=2, start=0, end=-1):
        super(LarsonScanner, self).__init__(led, start, end)
        self._color = color

        self._tail = tail + 1  # makes tail math later easier
        if self._tail >= self._size / 2:
            self._tail = (self._size / 2) - 1

        self._direction = -1
        self._last = 0
        self._fadeAmt = 256 / self._tail

    def step(self, amt = 1):
        self._led.all_off()

        self._last = self._start + self._step
        self._led.set(self._last, self._color)

        for i in range(self._tail):
            self._led.set(self._last - i, colors.color_scale(self._color, 255 - (self._fadeAmt * i)))
            self._led.set(self._last + i, colors.color_scale(self._color, 255 - (self._fadeAmt * i)))

        if self._start + self._step >= self._end:
            self._direction = -self._direction
        elif self._step <= 0:
            self._direction = -self._direction

        self._step += self._direction * amt

class LarsonRainbow(LarsonScanner):
    """Larson scanner (i.e. Cylon Eye or K.I.T.T.) but Rainbow."""

    def __init__(self, led, tail=2, start=0, end=-1):
        super(LarsonRainbow, self).__init__(
            led, colors.Off, tail, start, end)

    def step(self, amt = 1):
        self._color = colors.hue_helper(0, self._size, self._step)

        super(LarsonRainbow, self).step(amt)



# MANIFEST = [
#     {
#         "class": LarsonRainbow,
#         "controller": "strip",
#         "desc": None,
#         "display": "LarsonRainbow",
#         "id": "LarsonRainbow",
#         "params": [
#             {
#                 "default": -1,
#                 "help": "",
#                 "id": "end",
#                 "label": "",
#                 "type": "int"
#             },
#             {
#                 "default": 0,
#                 "help": "",
#                 "id": "start",
#                 "label": "",
#                 "type": "int"
#             },
#             {
#                 "default": 2,
#                 "help": "",
#                 "id": "tail",
#                 "label": "",
#                 "type": "int"
#             }
#         ],
#         "type": "animation"
#     },
#     {
#         "class": LarsonScanner,
#         "controller": "strip",
#         "desc": None,
#         "display": "LarsonScanner",
#         "id": "LarsonScanner",
#         "params": [
#             {
#                 "default": -1,
#                 "help": "",
#                 "id": "end",
#                 "label": "",
#                 "type": "int"
#             },
#             {
#                 "default": 0,
#                 "help": "",
#                 "id": "start",
#                 "label": "",
#                 "type": "int"
#             },
#             {
#                 "default": 2,
#                 "help": "",
#                 "id": "tail",
#                 "label": "",
#                 "type": "int"
#             },
#             {
#                 "default": None,
#                 "help": "",
#                 "id": "color",
#                 "label": "",
#                 "type": ""
#             }
#         ],
#         "type": "animation"
#     }
# ]
