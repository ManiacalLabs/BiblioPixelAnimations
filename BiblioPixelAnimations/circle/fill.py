from bibliopixel.animation import BaseCircleAnim
from bibliopixel.util.colors import COLORS


class CircleFill(BaseCircleAnim):
    COLOR_DEFAULTS = ('colors', [COLORS.Red]),

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        self.layout.all_off()
        for r, c in enumerate(self.palette):
            self.layout.fillRing(r, c, startAngle=0, endAngle=self._step)
        self._step += amt
        self._step %= 360


class CircleFillRainbow(BaseCircleAnim):

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        self.layout.all_off()
        c = self.palette.get(self._step)
        self.layout.fillRing(0, c, startAngle=0, endAngle=self._step)
        self._step += amt
        self._step %= 360
