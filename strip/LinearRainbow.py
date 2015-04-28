from bibliopixel.animation import *

class LinearRainbow(BaseStripAnim):

    def __init__(self, led, maxLed, sleep = 0.01):
        super(LinearRainbow, self).__init__(led, 0, -1)
        self._step = 0
        self._current = 0
        self._minLed = 0
        self._maxLed = maxLed
        self._delay = sleep

    def step(self, amt = 1):
        self._led.fill(colors.wheel_color(self._step), 0, self._current)

        if self._step == len(colors._wheel)-1:
            self._step = 0

        if self._current == self._maxLed:
            self._current = self._minLed

        self._step += 1
        self._current += 1

        time.sleep(self._delay)