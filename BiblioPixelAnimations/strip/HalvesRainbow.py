from bibliopixel.animation import *
import math

# This one is best run in the region of 50 frames a second


class HalvesRainbow(BaseStripAnim):

    def __init__(self, led, max_led=-1, centre_out=True, rainbow_inc=4):
        super(HalvesRainbow, self).__init__(led, 0, -1)
        self._current = 0
        self._minLed = 0
        self._maxLed = max_led
        if self._maxLed < 0 or self._maxLed < self._minLed:
            self._maxLed = self._led.lastIndex
        self._positive = True
        self._step = 0
        self._centerOut = centre_out
        self._rainbowInc = rainbow_inc

    def step(self, amt=1):

        center = float(self._maxLed)/2
        center_floor = math.floor(center)
        center_ceil = math.ceil(center)

        if self._centerOut:
            self._led.fill(
                colors.hue2rgb_rainbow(self._step), int(center_floor - self._current), int(center_floor - self._current))
            self._led.fill(
                colors.hue2rgb_rainbow(self._step), int(center_ceil + self._current), int(center_ceil + self._current))
        else:
            self._led.fill(
                colors.hue2rgb_rainbow(self._step), int(self._current), int(self._current))
            self._led.fill(
                colors.hue2rgb_rainbow(self._step), int(self._maxLed - self._current), int(self._maxLed - self._current))

        if self._step == len(colors.hue_rainbow)-1:
            self._step = 0
        else:
            self._step += amt + self._rainbowInc
            if self._step > len(colors.hue_rainbow)-1:
                self._step = 0

        if self._current == center_floor:
            self._current = self._minLed
        else:
            self._current += amt



# MANIFEST = [
#     {
#         "class": HalvesRainbow,
#         "controller": "strip",
#         "desc": None,
#         "display": "HalvesRainbow",
#         "id": "HalvesRainbow",
#         "params": [
#             {
#                 "default": -1,
#                 "help": "",
#                 "id": "max_led",
#                 "label": "",
#                 "type": "int"
#             },
#             {
#                 "default": 4,
#                 "help": "",
#                 "id": "rainbow_inc",
#                 "label": "",
#                 "type": "int"
#             },
#             {
#                 "default": True,
#                 "help": "",
#                 "id": "centre_out",
#                 "label": "",
#                 "type": "bool"
#             }
#         ],
#         "type": "animation"
#     }
# ]
