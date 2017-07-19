from bibliopixel.animation import BaseCircleAnim
from bibliopixel import colors


class PinWheel(BaseCircleAnim):

    def __init__(self, layout, colors=[colors.Red, colors.Green, colors.Blue]):
        super(PinWheel, self).__init__(layout)
        self.colors = colors
        self.blades = len(self.colors)
        self.sepDegrees = 360.0 / self.blades

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        self.layout.all_off()
        for r in range(0, self.ringCount):
            for c in range(len(self.colors)):
                self.layout.fillRing(r, self.colors[c], startAngle=(
                    self.sepDegrees * c) + self._step, endAngle=(self.sepDegrees * c) + self.sepDegrees + self._step)

        self._step += amt
        self._step %= 360
