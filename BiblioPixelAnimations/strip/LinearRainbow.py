from bibliopixel.animation import BaseStripAnim
from bibliopixel import colors


class LinearRainbow(BaseStripAnim):

    def __init__(self, layout, max_led=-1, individual_pixel=False):
        super(LinearRainbow, self).__init__(layout, 0, -1)
        self._minLed = 0
        self._maxLed = max_led
        if self._maxLed < 0 or self._maxLed < self._minLed:
            self._maxLed = self.layout.numLEDs - 1

        self._individualPixel = individual_pixel

    def pre_run(self):
        self._current = 0
        self._step = 0

    def step(self, amt=1):
        if self._individualPixel:
            # This setting will change the colour of each pixel on each cycle
            self.layout.fill(
                colors.hue2rgb(self._step), self._current, self._current)

        else:
            # This setting will change the colour of all pixels on each cycle
            self.layout.fill(colors.wheel_color(self._step), 0, self._current)

        if self._step == len(colors.conversions.HUE_RAINBOW) - 1:
            self._step = 0
        else:
            self._step += amt

        if self._current == self._maxLed:
            self._current = self._minLed
        else:
            self._current += amt
