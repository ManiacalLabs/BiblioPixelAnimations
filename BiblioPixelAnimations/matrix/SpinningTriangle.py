from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors
from bibliopixel.util import pointOnCircle


class SpinningTriangle(BaseMatrixAnim):
    def __init__(self, layout, cx=None, cy=None, radius=None, aa=True):
        super(SpinningTriangle, self).__init__(layout)
        self._cx = cx
        self._cy = cy
        self._radius = radius
        self._angles = (0, 120, 240)
        self.aa = aa

        if self._cx is None:
            self._cx = self.width // 2
        if self._cy is None:
            self._cy = self.height // 2
        if self._radius is None:
            self._radius = (self.width // 2) - 2

    def pre_run(self):
        self._step = 0

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
        self.layout.all_off()
        a = pointOnCircle(self._cx, self._cy, self._radius, self._angles[0])
        b = pointOnCircle(self._cx, self._cy, self._radius, self._angles[1])
        c = pointOnCircle(self._cx, self._cy, self._radius, self._angles[2])

        color = colors.hue2rgb_360(self._angles[0])

        self.layout.drawLine(a[0], a[1], b[0], b[1], color, aa=self.aa)
        self.layout.drawLine(b[0], b[1], c[0], c[1], color, aa=self.aa)
        self.layout.drawLine(c[0], c[1], a[0], a[1], color, aa=self.aa)

        self._angles = self.__stepAngles(self._angles, amt)
