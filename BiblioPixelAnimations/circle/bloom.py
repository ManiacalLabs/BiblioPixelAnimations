from bibliopixel.animation import BaseCircleAnim
from bibliopixel import colors


class CircleBloom(BaseCircleAnim):

    def __init__(self, led, spread=1):
        super(CircleBloom, self).__init__(led)
        self.spread = spread

    def step(self, amt=8):
        for i in range(self.ringCount):
            c = colors.hue_helper(
                i, int(self.ringCount * self.spread), self._step)
            self._led.fillRing(i, c)

        self._step += amt
        if(self._step >= 255):
            self._step = 0


MANIFEST = [
    {
        "class": CircleBloom,
        "controller": "circle",
        "desc": None,
        "display": "Bloom",
        "id": "CircleBloom",
        "params": [
            {
                "default": 1,
                "help": "",
                "id": "spread",
                "label": "Spread",
                "type": "int",
                "min": 1,
                "max": 32
            }
        ],
        "type": "animation"
    }
]
