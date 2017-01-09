from bibliopixel.animation import BaseCircleAnim
from bibliopixel import colors


class Swirl(BaseCircleAnim):

    def __init__(self, led, angle=12):
        super(Swirl, self).__init__(led)
        self.angle = angle

    def step(self, amt=1):
        for a in range(0, 360, self.angle):
            c = colors.hue_helper360(a, 360, self._step)
            for i in range(self.ringCount):
                self._led.set(i, a, c)

        self._step += amt


MANIFEST = [
    {
        "class": Swirl,
        "controller": "circle",
        "desc": None,
        "display": "Swirl",
        "id": "Swirl",
        "params": [
            {
                "default": 12,
                "help": "Degrees change per frame",
                "id": "angle",
                "label": "Angle Change",
                "type": "int"
            }
        ],
        "type": "animation"
    }
]
