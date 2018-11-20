from bibliopixel.animation.circle import Circle
from bibliopixel.colors import COLORS


class ArcRotate(Circle):
    COLOR_DEFAULTS = ('colors', [COLORS.Red, COLORS.Green, COLORS.Blue]),

    def __init__(self, layout, arc=180, outerRing=-1, outterRing=None, **kwds):
        super().__init__(layout, **kwds)
        if outterRing is not None:
            # Legacy misspelling
            outerRing = outterRing
        if outerRing < 0 or outerRing > self.layout.lastRing:
            outerRing = self.layout.lastRing
        self.outerRing = outerRing
        self.arcCount = len(self.palette)
        self.arc = arc / 2

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        self.layout.all_off()
        ci = 0
        for r in range(self.outerRing, self.outerRing - self.arcCount, -1):
            c = self.palette(ci)
            ci += 1
            self.layout.fillRing(r, c, startAngle=self._step - self.arc, endAngle=self._step + self.arc)
        self._step += amt
        self._step %= 360
