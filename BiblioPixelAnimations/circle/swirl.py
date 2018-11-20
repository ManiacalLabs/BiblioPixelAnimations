from bibliopixel.animation.circle import Circle
from bibliopixel.colors import palettes


class Swirl(Circle):
    COLOR_DEFAULTS = ('palette', palettes.get('three_sixty')),

    def __init__(self, layout, angle=12, **kwds):
        super().__init__(layout, **kwds)
        self.angle = angle

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        for a in range(0, 360, self.angle):
            c = self.palette(self._step)
            for i in range(self.ringCount):
                self.layout.set(i, a, c)

        self._step += amt
