from bibliopixel.animation import BaseStripAnim

class ColorChase(BaseStripAnim):
    """Chase one pixel down the strip."""

    def __init__(self, led, color, width=1, start=0, end=-1):
        super(ColorChase, self).__init__(led, start, end)
        self._color = color
        self._width = width

    def step(self, amt = 1):
        self._led.all_off() #because I am lazy

        for i in range(self._width):
            self._led.set(self._start + self._step + i, self._color)

        self._step += amt
        overflow = (self._start + self._step) - self._end
        if overflow >= 0:
            self._step = overflow



MANIFEST = [
    {
        "class": ColorChase,
        "controller": "strip",
        "desc": "Chase a pixel (or pixels) of one color down the strip.",
        "display": "ColorChase",
        "id": "ColorChase",
        "params": [
            {
                "default": -1,
                "help": "",
                "id": "end",
                "label": "End Pixel",
                "type": "int"
            },
            {
                "default": 0,
                "help": "",
                "id": "start",
                "label": "Start Pixel",
                "type": "int"
            },
            {
                "default": 1,
                "help": "Width of lit section",
                "id": "width",
                "label": "Width",
                "type": "int"
            },
            {
                "default": None,
                "help": "",
                "id": "color",
                "label": "Color",
                "type": "color"
            }
        ],
        "type": "animation"
    }
]
