from bibliopixel.animation.circle import Circle
from bibliopixel.colors import COLORS


class PinWheel(Circle):
    COLOR_DEFAULTS = ('colors', [COLORS.Red, COLORS.Green, COLORS.Blue]),

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
