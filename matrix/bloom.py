from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors

import math
import time
import random

def genVector(width, height, x_mult = 1, y_mult = 1):
    """Generates a map of vector lengths from the center point to each coordinate

    widht - width of matrix to generate
    height - height of matrix to generate
    x_mult - value to scale x-axis by
    y_mult - value to scale y-axis by
    """
    centerX = (width - 1) / 2.0
    centerY = (height - 1) / 2.0

    return [[int(math.sqrt(math.pow(x - centerX, 2*x_mult) + math.pow(y - centerY, 2*y_mult))) for x in range(width)] for y in range(height)]

def pointOnCircle(cx, cy, radius, angle):
    """Calculates the coordinates of a point on a circle given the center point, radius, and angle"""
    angle = math.radians(angle) - (math.pi / 2)
    x = cx + radius * math.cos(angle)
    if x < cx:
        x = math.ceil(x)
    else:
        x = math.floor(x)

    y = cy + radius * math.sin(angle)

    if y < cy:
        y = math.ceil(y)
    else:
        y = math.floor(y)

    return (int(x), int(y))

class Bloom(BaseMatrixAnim):

    def __init__(self, led, dir = True):
        super(Bloom, self).__init__(led)
        self._vector = genVector(self._led.width, self._led.height)
        self._dir = dir

    def step(self, amt = 8):
        if self._dir:
            s = 255 - self._step
        else:
            s = self._step

        h = self._led.height
        w = self._led.width

        #this ignores master brightness in the interest of speed
        # buf = [colors.hue_helper(self._vector[y][x], h, s) for y in range(h) for x in range(w)]
        # buf = [i for sub in buf for i in sub]
        # self._led.setBuffer(buf)

        #this respects master brightness but is slower
        for y in range(self._led.height):
           for x in range(self._led.width):
               c = colors.hue_helper(self._vector[y][x], self._led.height, s)
               self._led.set(x, y, c)

        self._step += amt
        if(self._step >= 255):
            self._step = 0
