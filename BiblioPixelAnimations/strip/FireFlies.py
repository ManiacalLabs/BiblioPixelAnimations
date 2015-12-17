from bibliopixel.animation import BaseStripAnim
import random

class FireFlies(BaseStripAnim):
    """Stobe Light Effect."""
    def __init__(self, led, colors, width = 1, count = 1, start=0, end=-1):
        super(FireFlies, self).__init__(led, start, end)
        self._colors = colors
        self._color_count = len(colors)
        self._width = width
        self._count = count

    def step(self, amt = 1):
        amt = 1 #anything other than 1 would be just plain silly
        if self._step > self._led.numLEDs:
            self._step = 0

        self._led.all_off();

        for i in range(self._count):
            pixel = random.randint(0, self._led.numLEDs - 1)
            color = self._colors[random.randint(0, self._color_count - 1)]

            for i in range(self._width):
                if pixel + i < self._led.numLEDs:
                    self._led.set(pixel + i, color)

        self._step += amt


import bibliopixel.colors as colors
rainbow = [colors.Red, colors.Orange, colors.Yellow, colors.Green, colors.Blue, colors.Purple]
MANIFEST = [
    {
        "class": FireFlies,
        "controller": "strip",
        "desc": None,
        "display": "FireFlies",
        "id": "FireFlies",
        "params": [
            {
                "default": rainbow,
                "help": "Colors for pixels",
                "id": "colors",
                "label": "Colors",
                "type": "multi",
                "controls": {
                    "default": rainbow,
                    "help": None,
                    "label": "Color",
                    "type": "color"
                }
            },
            {
                "default": 30,
                "help": "",
                "id": "count",
                "label": "Pixels Per Frame",
                "type": "int"
            },
            # {
            #     "default": -1,
            #     "help": "",
            #     "id": "end",
            #     "label": "",
            #     "type": "int"
            # },
            # {
            #     "default": 0,
            #     "help": "",
            #     "id": "start",
            #     "label": "",
            #     "type": "int"
            # },
            {
                "default": 1,
                "help": "Width of each random pixel",
                "id": "width",
                "label": "Width",
                "type": "int"
            }
        ],
        "type": "animation"
    }
]
