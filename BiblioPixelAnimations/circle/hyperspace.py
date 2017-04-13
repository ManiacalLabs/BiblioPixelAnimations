from __future__ import division
from bibliopixel.animation import BaseCircleAnim
import bibliopixel.colors as colors
import random


class Hyperspace(BaseCircleAnim):
    def __init__(self, led, colors=[colors.Green], tail=4, growthRate=4, angleDiff=6):
        super(Hyperspace, self).__init__(led)
        if not isinstance(colors, list):
            colors = [colors]
        self._colors = colors
        self._tail = tail
        self._tails = [[] for x in range(360)]
        self._growthRate = growthRate
        self._angleDiff = angleDiff

    def _drawTail(self, angle, ring, color):
        for i in range(self._tail):
            if ring - i >= 0 and ring - i <= self.lastRing:
                level = 255 - ((255 // self._tail) * i)
                self._led.set(ring - i, angle, colors.color_scale(color, level))

    def step(self, amt=1):
        self._led.all_off()

        for i in range(self._growthRate):
            newTail = random.randrange(0, 360, self._angleDiff)
            cInt = random.randint(0, len(self._colors) - 1)
            self._tails[newTail].append((0, self._colors[cInt]))

        for a in range(360):
            angle = self._tails[a]
            if len(angle) > 0:
                removals = []
                for r in range(len(angle)):
                    tail = angle[r]
                    if tail[0] <= self.lastRing:
                        self._drawTail(a, tail[0], tail[1])
                    if tail[0] - (self._tail - 1) <= self.lastRing:
                        tail = (tail[0] + amt, tail[1])
                        self._tails[a][r] = tail
                    else:
                        removals.append(tail)
                for r in removals:
                    self._tails[a].remove(r)

        self._step = 0


class HyperspaceRainbow(BaseCircleAnim):
    def __init__(self, led, tail=4, growthRate=4, angleDiff=6):
        super(HyperspaceRainbow, self).__init__(led)

        self._tail = tail
        self._tails = [[] for x in range(360)]
        self._growthRate = growthRate
        self._angleDiff = angleDiff

    def _drawTail(self, angle, ring, color):
        for i in range(self._tail):
            if ring - i >= 0 and ring - i <= self.lastRing:
                level = 255 - ((255 // self._tail) * i)
                self._led.set(ring - i, angle, colors.color_scale(color, level))

    def step(self, amt=1):
        self._led.all_off()

        for i in range(self._growthRate):
            newTail = random.randrange(0, 360, self._angleDiff)
            self._tails[newTail].append(0)

        for a in range(360):
            angle = self._tails[a]
            if len(angle) > 0:
                removals = []
                for r in range(len(angle)):
                    tail = angle[r]
                    if tail <= self.lastRing:
                        c = colors.hue2rgb(tail * (255 // self.lastRing))
                        self._drawTail(a, tail, c)
                        colors.hue2rgb(tail * (255 // self.lastRing))
                    if tail - (self._tail - 1) <= self.lastRing:
                        tail = tail + amt
                        self._tails[a][r] = tail
                    else:
                        removals.append(tail)
                for r in removals:
                    self._tails[a].remove(r)

        self._step = 0


MANIFEST = [
    {
        "class": Hyperspace,
        "controller": "circle",
        "desc": None,
        "display": "Hyperspace",
        "id": "Hyperspace",
        "params": [
            {
                "default": 4,
                "help": "Number of new tails per frame",
                "id": "growthRate",
                "label": "Growth Rate",
                "type": "int"
            },
            {
                "default": 4,
                "help": "Length of tail",
                "id": "tail",
                "label": "Length",
                "type": "int"
            },
            {
                "default": [
                    [
                        0,
                        255,
                        0
                    ]
                ],
                "help": "Colors of tails",
                "id": "colors",
                "label": "Colors",
                "type": "multi",
                "controls": {
                    "default": [
                        [
                            0,
                            255,
                            0
                        ]
                    ],
                    "help": "Tail color",
                    "label": "Color",
                    "type": "color"
                }
            }
        ],
        "type": "animation"
    },
    {
        "class": HyperspaceRainbow,
        "controller": "circle",
        "desc": None,
        "display": "HyperspaceRainbow",
        "id": "HyperspaceRainbow",
        "params": [
            {
                "default": 4,
                "help": "Number of new tails per frame",
                "id": "growthRate",
                "label": "Growth Rate",
                "type": "int"
            },
            {
                "default": 4,
                "help": "Length of tail",
                "id": "tail",
                "label": "Length",
                "type": "int"
            }
        ],
        "type": "animation"
    }
]
