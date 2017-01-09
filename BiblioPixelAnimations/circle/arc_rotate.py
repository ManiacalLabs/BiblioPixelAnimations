from bibliopixel.animation import BaseCircleAnim
from bibliopixel import colors


class ArcRotate(BaseCircleAnim):

    def __init__(self, led, colors, arc=180, outterRing=-1):
        super(ArcRotate, self).__init__(led)
        if outterRing < 0 or outterRing > self._led.lastRing:
            outterRing = self._led.lastRing
        self.outterRing = outterRing
        self.colors = colors
        self.arcCount = len(self.colors)
        self.arc = arc / 2

    def step(self, amt=1):
        self._led.all_off()
        ci = 0
        for r in range(self.outterRing, self.outterRing - self.arcCount, -1):
            c = self.colors[ci]
            ci += 1
            self._led.fillRing(r, c, startAngle=self._step -
                               self.arc, endAngle=self._step + self.arc)
        self._step += amt
        self._step %= 360


rainbow = [colors.Red, colors.Orange, colors.Yellow,
           colors.Green, colors.Blue, colors.Purple]

MANIFEST = [
    {
        "class": ArcRotate,
        "controller": "circle",
        "desc": None,
        "display": "ArcRotate",
        "id": "ArcRotate",
        "params": [
            {
                "default": rainbow,
                "help": "",
                "id": "colors",
                "label": "Colors",
                "type": "multi",
                "controls": {
                    "help": None,
                    "label": "Color",
                    "type": "color"
                }
            },
            {
                "default": 180,
                "help": "Arc Angle to light up",
                "id": "arc",
                "label": "Arc Angle",
                "type": "int",
                "min": 1,
                "max": 359
            }
        ],
        "type": "animation"
    }
]
