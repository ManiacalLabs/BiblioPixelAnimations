from bibliopixel.animation import BaseCircleAnim
from bibliopixel import colors


class CircleBloom(BaseCircleAnim):

    def __init__(self, layout, spread=1):
        super(CircleBloom, self).__init__(layout)
        self.spread = spread

    def pre_run(self):
        self._step = 0

    def step(self, amt=8):
        for i in range(self.ringCount):
            c = colors.hue_helper(
                i, int(self.ringCount * self.spread), self._step)
            self.layout.fillRing(i, c)

        self._step += amt
        if(self._step >= 255):
            self._step = 0
