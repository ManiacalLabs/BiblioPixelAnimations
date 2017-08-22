from bibliopixel.animation import BaseStripAnim
from bibliopixel import colors as bp_colors


class SaberBlade(BaseStripAnim):
    def __init__(self, layout, colors=[bp_colors.Red], speed=1):
        super().__init__(layout)
        self._colors = colors
        self.speed = speed

    def pre_run(self):
        self._step = 0
        self.blade_pos = 0
        self.blade_color = 0

    def step(self, amt=1):
        self.layout.all_off()

        self.layout.fill(self._colors[self.blade_color], 0, self.blade_pos)
        self.blade_pos += self.speed

        if self.speed > 0 and self.blade_pos + self.speed > self._size:
            self.speed *= -1
        elif self.speed < 0 and self.blade_pos <= 0:
            self.blade_pos = 0
            self.blade_color += 1
            if self.blade_color >= len(self._colors):
                self.blade_color = 0
            self.speed *= -1
