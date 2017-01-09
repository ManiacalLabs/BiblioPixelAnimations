from bibliopixel.animation import BaseCircleAnim
from bibliopixel import colors


class Diag(BaseCircleAnim):

    def __init__(self, led, turns=1, angle=6, direction=False):
        super(Diag, self).__init__(led)
        self.turns = turns
        self.angle = angle
        self.slice = 360 / self.ringCount * self.turns
        self.direction = direction

    def step(self, amt=1):
        for a in range(0, 360, self.angle):
            c = colors.hue_helper360(a, 360, self._step)
            for i in range(self.ringCount):
                ap = a + (self.slice * i)
                self._led.set(i, ap, c)

        self._step += amt if self.direction else (amt * -1)


MANIFEST = [
    {
        "class": Diag,
        "controller": "circle",
        "desc": None,
        "display": "Diagonal Rainbow",
        "id": "Diag",
        "params": [
            {
                "default": 1,
                "help": "Total turns",
                "id": "turns",
                "label": "Turns",
                "type": "int"
            },
            {
                "default": 6,
                "help": "Degrees change per frame",
                "id": "angle",
                "label": "Angle Change",
                "type": "int"
            }
        ],
        "type": "animation"
    }
]
