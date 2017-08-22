import bibliopixel.colors as colors
from bibliopixel.animation import BaseStripAnim
import random


class Pulse(BaseStripAnim):
    def __init__(self, layout, colors=[colors.Red], tail=2, chance=30, min_speed=1, max_speed=5):
        super().__init__(layout)
        self._colors = colors

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
        self.pulse_color = self._colors[random.randrange(0, len(self._colors))]
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


# class LarsonRainbow(LarsonScanner):
#     """Larson scanner (i.e. Cylon Eye or K.I.T.T.) but Rainbow."""
#
#     def __init__(self, layout, tail=2, start=0, end=-1):
#         super(LarsonRainbow, self).__init__(layout, colors.Off, tail, start, end)
#
#     def step(self, amt=1):
#         self._color = colors.hue_helper(0, self._size, self._step)
#
#         super(LarsonRainbow, self).step(amt)
