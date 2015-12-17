from bibliopixel.animation import *


class LinearRainbow(BaseStripAnim):

    def __init__(self, led, max_led=-1, individual_pixel=False):
        super(LinearRainbow, self).__init__(led, 0, -1)
        self._step = 0
        self._current = 0
        self._minLed = 0
        self._maxLed = max_led
        if self._maxLed < 0 or self._maxLed < self._minLed:
            self._maxLed = self._led.lastIndex

        self._individualPixel = individual_pixel

    def step(self, amt=1):
        if self._individualPixel:
            # This setting will change the colour of each pixel on each cycle
            self._led.fill(
                colors.hue2rgb_rainbow(self._step), self._current, self._current)

        else:
            # This setting will change the colour of all pixels on each cycle
            self._led.fill(colors.wheel_color(self._step), 0, self._current)

        if self._step == len(colors.hue_rainbow) - 1:
            self._step = 0
        else:
            self._step += amt

        if self._current == self._maxLed:
            self._current = self._minLed
        else:
            self._current += amt



# MANIFEST = [
#     {
#         "class": LinearRainbow,
#         "controller": "strip",
#         "desc": None,
#         "display": "LinearRainbow",
#         "id": "LinearRainbow",
#         "params": [
#             {
#                 "default": -1,
#                 "help": "",
#                 "id": "max_led",
#                 "label": "",
#                 "type": "int"
#             },
#             {
#                 "default": False,
#                 "help": "",
#                 "id": "individual_pixel",
#                 "label": "",
#                 "type": "bool"
#             }
#         ],
#         "type": "animation"
#     }
# ]
