from bibliopixel.animation import BaseStripAnim
import math

class Wave(BaseStripAnim):
    """Sine wave animation."""

    def __init__(self, led, color, cycles, start=0, end=-1):
        super(Wave, self).__init__(led, start, end)
        self._color = color
        self._cycles = cycles

    def step(self, amt = 1):
        for i in range(self._size):
            y = math.sin(
                math.pi *
                float(self._cycles) *
                float(self._step * i) /
                float(self._size))

            if y >= 0.0:
                # Peaks of sine wave are white
                y = 1.0 - y  # Translate Y to 0.0 (top) to 1.0 (center)
                r, g, b = self._color
                c2 = (int(255 - float(255 - r) * y), int(255 - float(255 - g) * y), int(255 - float(255 - b) * y))
            else:
                # Troughs of sine wave are black
                y += 1.0  # Translate Y to 0.0 (bottom) to 1.0 (center)
                r, g, b = self._color
                c2 = (int(float(r) * y),
                           int(float(g) * y),
                           int(float(b) * y))
            self._led.set(self._start + i, c2)

        self._step += amt

class WaveMove(BaseStripAnim):
    """Sine wave animation."""

    def __init__(self, led, color, cycles, start=0, end=-1):
        super(WaveMove, self).__init__(led, start, end)
        self._color = color
        self._cycles = cycles
        self._moveStep = 0

    def step(self, amt = 1):
        for i in range(self._size):
            y = math.sin(
                (math.pi *
                float(self._cycles) *
                float(i) /
                float(self._size))
                + self._moveStep)

            if y >= 0.0:
                # Peaks of sine wave are white
                y = 1.0 - y  # Translate Y to 0.0 (top) to 1.0 (center)
                r, g, b = self._color
                c2 = (int(255 - float(255 - r) * y), int(255 - float(255 - g) * y), int(255 - float(255 - b) * y))
            else:
                # Troughs of sine wave are black
                y += 1.0  # Translate Y to 0.0 (bottom) to 1.0 (center)
                r, g, b = self._color
                c2 = (int(float(r) * y),
                           int(float(g) * y),
                           int(float(b) * y))
            self._led.set(self._start + i, c2)

        self._step += amt
        self._moveStep += 1
        if(self._moveStep >= self._size):
            self._moveStep = 0
