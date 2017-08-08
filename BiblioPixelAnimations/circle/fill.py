from bibliopixel.animation import BaseCircleAnim
from bibliopixel import colors


class CircleFill(BaseCircleAnim):

    def __init__(self, layout, colors=[colors.Red]):
        super().__init__(layout)
        self.colors = colors

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        self.layout.all_off()
        for r, c in enumerate(self.colors):
            self.layout.fillRing(r, c, startAngle=0, endAngle=self._step)
        self._step += amt
        self._step %= 360


class CircleFillRainbow(BaseCircleAnim):

    def __init__(self, layout):
        super().__init__(layout)
        self.colors = colors

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        self.layout.all_off()
        c = colors.hue2rgb_360(self._step)
        self.layout.fillRing(0, c, startAngle=0, endAngle=self._step)
        # for r, c in enumerate(self.colors):
        #     self.layout.fillRing(r, c, startAngle=0, endAngle=self._step)
        self._step += amt
        self._step %= 360
