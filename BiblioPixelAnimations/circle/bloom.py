from bibliopixel.animation import BaseCircleAnim


class CircleBloom(BaseCircleAnim):

    def __init__(self, layout, spread=1, **kwds):
        super().__init__(layout, **kwds)
        self.spread = spread

    def pre_run(self):
        self._step = 0

    def step(self, amt=8):
        for i in range(self.ringCount):
            length = int(self.ringCount * self.spread)
            c = self.palette(i * 255 / length + self._step)
            self.layout.fillRing(i, c)

        self._step += amt
