from bibliopixel.animation import BaseCircleAnim
from bibliopixel import colors


class ArcRotate(BaseCircleAnim):

    def __init__(self, layout, colors=[colors.Red, colors.Green, colors.Blue], arc=180, outterRing=-1):
        super(ArcRotate, self).__init__(layout)
        if outterRing < 0 or outterRing > self.layout.lastRing:
            outterRing = self.layout.lastRing
        self.outterRing = outterRing
        self.colors = colors
        self.arcCount = len(self.colors)
        self.arc = arc / 2

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        self.layout.all_off()
        ci = 0
        for r in range(self.outterRing, self.outterRing - self.arcCount, -1):
            c = self.colors[ci]
            ci += 1
            self.layout.fillRing(r, c, startAngle=self._step - self.arc, endAngle=self._step + self.arc)
        self._step += amt
        self._step %= 360
