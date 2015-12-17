from bibliopixel.animation import BaseStripAnim
import bibliopixel.colors as colors

class ColorFade(BaseStripAnim):
    """Fill the dots progressively along the strip."""

    def wave_range(self, start, peak, step):
        main = [i for i in range(start, peak+1, step)]
        return main + [i for i in reversed(main[0:len(main)-1])]

    def __init__(self, led, colors, step = 5, start=0, end=-1):
        super(ColorFade, self).__init__(led, start, end)
        self._colors = colors
        self._levels = self.wave_range(30, 255, step)
        self._level_count = len(self._levels)
        self._color_count = len(colors)

    def step(self, amt = 1):
        if self._step > self._level_count * self._color_count:
            self._step = 0

        c_index = (self._step / self._level_count) % self._color_count
        l_index = (self._step % self._level_count)
        color = self._colors[c_index];
        self._led.fill(colors.color_scale(color, self._levels[l_index]), self._start, self._end)

        self._step += amt


import bibliopixel.colors as colors
rainbow = [colors.Red, colors.Orange, colors.Yellow, colors.Green, colors.Blue, colors.Purple]
MANIFEST = [
    {
        "class": ColorFade,
        "controller": "strip",
        "desc": None,
        "display": "ColorFade",
        "id": "ColorFade",
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
            #     "default": 0,
            #     "help": "",
            #     "id": "start",
            #     "label": "",
            #     "type": "int"
            # },
            # {
            #     "default": -1,
            #     "help": "",
            #     "id": "end",
            #     "label": "",
            #     "type": "int"
            # },
            {
                "default": 5,
                "min": 1,
                "max": 50, 
                "help": "",
                "id": "step",
                "label": "Brightness Step",
                "type": "int"
            }
        ],
        "type": "animation"
    }
]
