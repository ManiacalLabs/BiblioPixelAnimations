from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors
from bibliopixel.util import pointOnCircle


class SpiningTriangle(BaseMatrixAnim):
    def __init__(self, led, cx, cy, radius, aa=True):
        super(SpiningTriangle, self).__init__(led)
        self._cx = cx
        self._cy = cy
        self._radius = radius
        self._angles = (0, 120, 240)
        self.aa = aa

    def _stepAngle(self, a, step):
        a += step
        if a >= 360:
            a -= 360
        elif a < 0:
            a += 360
        return a

    def __stepAngles(self, a, step):
        return (self._stepAngle(a[0], step), self._stepAngle(a[1], step), self._stepAngle(a[2], step),)

    def step(self, amt=1):
        self._led.all_off()
        a = pointOnCircle(self._cx, self._cy, self._radius, self._angles[0])
        b = pointOnCircle(self._cx, self._cy, self._radius, self._angles[1])
        c = pointOnCircle(self._cx, self._cy, self._radius, self._angles[2])

        color = colors.hue2rgb_360(self._angles[0])

        self._led.drawLine(a[0], a[1], b[0], b[1], color, aa=self.aa)
        self._led.drawLine(b[0], b[1], c[0], c[1], color, aa=self.aa)
        self._led.drawLine(c[0], c[1], a[0], a[1], color, aa=self.aa)

        self._angles = self.__stepAngles(self._angles, amt)


MANIFEST = [
    {
        "class": SpiningTriangle,
        "controller": "matrix",
        "desc": None,
        "display": "SpiningTriangle",
        "id": "SpiningTriangle",
        "params": [
            {
                "default": None,
                "help": "",
                "id": "radius",
                "label": "Radius",
                "type": "int"
            },
            {
                "default": None,
                "help": "",
                "id": "cy",
                "label": "Y Pos",
                "type": "int"
            },
            {
                "default": None,
                "help": "",
                "id": "cx",
                "label": "X Pos",
                "type": "int"
            },
            {
                "default": True,
                "help": "",
                "id": "aa",
                "label": "AntiAlias",
                "type": "bool"
            }
        ],
        "type": "animation"
    }
]
