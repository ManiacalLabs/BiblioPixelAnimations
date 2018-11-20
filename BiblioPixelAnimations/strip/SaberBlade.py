from bibliopixel.animation.strip import Strip
from bibliopixel.colors import COLORS


class SaberBlade(Strip):
    COLOR_DEFAULTS = ('colors', [COLORS.Red])

    def __init__(self, layout, speed=1, **kwds):
        super().__init__(layout, **kwds)
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
