from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors
import random


class Munching(BaseMatrixAnim):
    def __init__(self, layout, t=0, comparator=None):
        super().__init__(layout)
        self.t_start = t
        self.t = 0

    def pre_run(self):
        if self.t_start is None:
            self.t = random.randrange(32)
        else:
            self.t = self.t_start

    def step(self, amt=1):
        self.layout.all_off()
        print(self.t)
        for y in range(self.height):
            for x in range(self.width):
                if (x ^ y > self.t):
                    self.layout.set(x, y, colors.Red)
        self.t += amt
