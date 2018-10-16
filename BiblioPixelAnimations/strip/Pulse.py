
import bibliopixel.colors as colors
from bibliopixel.animation import BaseStripAnim
import random


class Pulse(BaseStripAnim):
    COLOR_DEFAULTS = ('colors', [colors.Red])

    def __init__(self, layout, tail=2, chance=30, min_speed=1, max_speed=5, **kwds):
        super().__init__(layout, **kwds)

        self._tail = tail + 1  # makes tail math later easier
        if self._tail >= self._size // 2:
            self._tail = (self._size // 2) - 1

        if self._tail == 0:
            self._tail = 1
        self._fadeAmt = 256 // self._tail

        self.chance = chance
        self.min_speed = min_speed
        self.max_speed = max_speed

    def pre_run(self):
        self.pulse_color = None
        self.pulse_position = 0
        self.pulse_speed = 0

    def add_pulse(self):
        self.pulse_color = random.choice(self.palette)
        self.pulse_speed = random.randrange(self.min_speed, self.max_speed)
        self.pulse_position = 0

    def step(self, amt=1):
        self.layout.all_off()

        if self.pulse_speed == 0 and random.randrange(0, 100) <= self.chance:
            self.add_pulse()

        if self.pulse_speed > 0:
            self.layout.set(self.pulse_position, self.pulse_color)
            for i in range(self._tail):
                c = colors.color_scale(self.pulse_color, 255 - (self._fadeAmt * i))
                self.layout.set(self.pulse_position - i, c)
                self.layout.set(self.pulse_position + i, c)

            if self.pulse_position > self._size + self._tail:
                self.pulse_speed = 0
            else:
                self.pulse_position += self.pulse_speed
