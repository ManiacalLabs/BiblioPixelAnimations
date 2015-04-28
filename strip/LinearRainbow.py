from bibliopixel.animation import *

class LinearRainbow(BaseStripAnim):

    def __init__(self, led, max_led, sleep=0.01, individual_pixel=False):
        super(LinearRainbow, self).__init__(led, 0, -1)
        self._step = 0
        self._current = 0
        self._minLed = 0
        self._maxLed = max_led
        self._delay = sleep
        self._individualPixel = individual_pixel

    def step(self, amt=1):
        if self._individualPixel:
            # This setting will change the colour of each pixel on each cycle
            self._led.fill(colors.wheel_color(self._step), self._current, self._current)

        else:
            # This setting will change the colour of all pixels on each cycle
            self._led.fill(colors.wheel_color(self._step), 0, self._current)

        if self._step == len(colors._wheel)-1:
            self._step = 0
        else:
            self._step += 1

        if self._current == self._maxLed:
            self._current = self._minLed
        else:
            self._current += 1

        time.sleep(self._delay)