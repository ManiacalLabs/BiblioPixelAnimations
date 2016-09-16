"""
Credit to kasperfish, posted on the forums:
http://forum.maniacallabs.com/showthread.php?tid=9&highlight=circlepop
"""

import random
from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors


class Circle():

    def __init__(self, posy, posx, color, frameratio, radius):
        self._y = posy
        self._x = posx
        self._color = color
        # animation speed of a single circle relative to the fps of the actual
        # animation.
        self.frameratio = frameratio
        self._radius = radius

    def grow(self, amt=1):
        self._radius += amt

    def changeColor(self, amt=8):
        self._color += amt
        if self._color >= 360:
            self._color %= 360


class CirclePop(BaseMatrixAnim):

    def __init__(self, led, bgcolor=colors.Off):
        super(CirclePop, self).__init__(led)
        self.cont = []  # list for storing Circle objects
        self.max_circ = 3  # max number of cirles in the list
        # probability for adding a new Circle to the list. higher values make
        # it less probable.
        self.prob_circ = 8
        self.bgcolor = bgcolor
        self.addCircle()  # add a first circle to our list

    def step(self, amt=1):
        self._led.fillScreen(self.bgcolor)  # background color
        # check if we may add a new circle to the list
        if not random.randrange(self.prob_circ) and len(self.cont) <= self.max_circ:
            self.addCircle()

        # loop through our circles, draw and update them
        for circ in self.cont:
            self._led.drawCircle(circ._x, circ._y, circ._radius,
                                 colors.hue2rgb_360(circ._color))

            if not self._step % circ.frameratio:
                circ.grow()
                circ.changeColor()

        self._step += amt
        # don't let our step counter grow endlessly
        if self._step >= 100:
            self._step %= 100

        # remove circles that have grown bigger than our matrix
        self.cont = [c for c in self.cont if c._radius !=
                     max(self._led.height, self._led.width) + 1]

    def addCircle(self):
        # let's add some randomness. You can play with these values.
        posx = random.randint(3, self._led.width - 3)
        posy = random.randint(3, self._led.height - 3)
        color = random.randint(1, 359)
        # choose between 2 speeds fps/1 and fps/2.
        frameratio = random.choice([1, 2])
        radius = 1
        self.cont.append(Circle(posy, posx, color, frameratio, radius))


MANIFEST = [
    {
        "class": CirclePop,
        "controller": "matrix",
        "desc": "Growing random circles",
        "display": "CirclePop",
        "id": "CirclePop",
        "params": [
            {
                "default": [
                    0,
                    0,
                    0
                ],
                "help": "",
                "id": "bgcolor",
                "label": "Background Color",
                "type": "color"
            }
        ],
        "type": "animation"
    }
]
