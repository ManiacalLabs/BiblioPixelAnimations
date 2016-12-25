from bibliopixel.animation import BaseCircleAnim


class PinWheel(BaseCircleAnim):

    def __init__(self, led, colors):
        super(PinWheel, self).__init__(led)
        self.colors = colors
        self.blades = len(self.colors)
        self.sepDegrees = 360.0 / self.blades

    def step(self, amt=1):
        self._led.all_off()
        for r in range(0, self.ringCount):
            for c in range(len(self.colors)):
                self._led.fillRing(r, self.colors[c], startAngle=(
                    self.sepDegrees * c) + self._step, endAngle=(self.sepDegrees * c) + self.sepDegrees + self._step)

        self._step += amt
        self._step %= 360
