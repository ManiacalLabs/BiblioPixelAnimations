from bibliopixel.animation import BaseCircleAnim
from bibliopixel.util.colors import palettes


class Swirl(BaseCircleAnim):
    COLOR_DEFAULTS = ('palette', palettes.get('three_sixty')),

    def __init__(self, layout, angle=12):
        super().__init__(layout)
        self.angle = angle

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        for a in range(0, 360, self.angle):
            c = self.palette(self._step)
            for i in range(self.ringCount):
                self.layout.set(i, a, c)

        self._step += amt
