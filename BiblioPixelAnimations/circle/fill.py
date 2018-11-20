from bibliopixel.animation.circle import Circle
from bibliopixel.colors import COLORS


class CircleFill(Circle):
    COLOR_DEFAULTS = ('colors', [COLORS.Red]),

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        self.layout.all_off()
        for r, c in enumerate(self.palette):
            self.layout.fillRing(r, c, startAngle=0, endAngle=self._step)
        self._step += amt
        self._step %= 360


class CircleFillRainbow(Circle):

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        self.layout.all_off()
        c = self.palette.get(self._step)
        self.layout.fillRing(0, c, startAngle=0, endAngle=self._step)
        self._step += amt
        self._step %= 360
