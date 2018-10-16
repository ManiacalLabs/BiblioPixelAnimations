from bibliopixel.animation import BaseStripAnim
from bibliopixel import colors as bp_colors


class SaberBlade(BaseStripAnim):
    COLOR_DEFAULTS = ('colors', [bp_colors.Red])

    def __init__(self, layout, speed=1):
        super().__init__(layout)
        self.speed = speed

    def pre_run(self):
        self._step = 0
        self.blade_pos = 0
        self.blade_color = 0

    def step(self, amt=1):
        self.layout.all_off()

        self.layout.fill(self.palette(self.blade_color), 0, self.blade_pos)
        self.blade_pos += self.speed

        if self.speed > 0 and self.blade_pos + self.speed > self._size:
            self.speed *= -1
        elif self.speed < 0 and self.blade_pos <= 0:
            self.blade_pos = 0
            self.blade_color += 1
            self.speed *= -1
