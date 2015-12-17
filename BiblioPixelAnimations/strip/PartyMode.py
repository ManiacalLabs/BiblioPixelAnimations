from bibliopixel.animation import BaseStripAnim

class PartyMode(BaseStripAnim):
    """Stobe Light Effect."""

    def __init__(self, led, colors, start=0, end=-1):
        super(PartyMode, self).__init__(led, start, end)
        self._colors = colors
        self._color_count = len(colors)

    def step(self, amt = 1):
        amt = 1 #anything other than 1 would be just plain silly
        if self._step > (self._color_count * 2) - 1:
            self._step = 0

        if self._step % 2 == 0:
            self._led.fill(self._colors[self._step / 2], self._start, self._end)
        else:
            self._led.all_off()

        self._step += amt


import bibliopixel.colors as colors
rainbow = [colors.Red, colors.Orange, colors.Yellow, colors.Green, colors.Blue, colors.Purple]
MANIFEST = [
    {
        "class": PartyMode,
        "controller": "strip",
        "desc": None,
        "display": "PartyMode",
        "id": "PartyMode",
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
            # }
        ],
        "type": "animation"
    }
]
