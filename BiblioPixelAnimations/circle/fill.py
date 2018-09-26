from bibliopixel.animation import BaseCircleAnim
from bibliopixel.util.colors import COLORS, palettes


class CircleFill(BaseCircleAnim):

    def __init__(self, layout, colors=[COLORS.Red]):
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

    def __init__(self, layout, palette=palettes.get('three_sixty')):
        super().__init__(layout)
        self.palette = palette

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        self.layout.all_off()
        c = self.palette.get(self._step)
        self.layout.fillRing(0, c, startAngle=0, endAngle=self._step)
        self._step += amt
        self._step %= 360
