from bibliopixel.animation import BaseCircleAnim
from bibliopixel import colors


class PinWheel(BaseCircleAnim):
    COLOR_DEFAULTS = ('colors', [colors.Red, colors.Green, colors.Blue]),

    def __init__(self, layout, **kwds):
        super().__init__(layout, **kwds)
        self.sepDegrees = 360.0 / len(self.palette)

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        self.layout.all_off()
        for r in range(0, self.ringCount):
            for c, color in enumerate(self.palette):
                self.layout.fillRing(r, color, startAngle=(
                    self.sepDegrees * c) + self._step, endAngle=(self.sepDegrees * c) + self.sepDegrees + self._step)

        self._step += amt
        self._step %= 360
