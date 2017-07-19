from bibliopixel.animation import BaseCircleAnim
from bibliopixel import colors


class Swirl(BaseCircleAnim):

    def __init__(self, layout, angle=12):
        super(Swirl, self).__init__(layout)
        self.angle = angle

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        for a in range(0, 360, self.angle):
            c = colors.hue_helper360(a, 360, self._step)
            for i in range(self.ringCount):
                self.layout.set(i, a, c)

        self._step += amt
