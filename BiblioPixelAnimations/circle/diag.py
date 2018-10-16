from bibliopixel.animation import BaseCircleAnim
from bibliopixel.util.colors import palettes


class Diag(BaseCircleAnim):
    COLOR_DEFAULTS = ('palette', palettes.get('three_sixty')),

    def __init__(self, layout, turns=1, angle=6, direction=False, **kwds):
        super().__init__(layout, **kwds)
        self.turns = turns
        self.angle = angle
        self.slice = 360 / self.ringCount * self.turns
        self.direction = direction

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        for a in range(0, 360, self.angle):
            c = self.palette.get(self._step)
            for i in range(self.ringCount):
                ap = a + (self.slice * i)
                self.layout.set(i, ap, c)

        self._step += amt if self.direction else (amt * -1)
