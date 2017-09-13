from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors
import random
import math


def hue_fade(a, b, val):
    if a > b:
        b = b + 360
    return (a + ((b - a) * val)) % 360


class MathFunc(BaseMatrixAnim):
    funcs = [
        lambda x, y, s: x + (x * y) + s,
        lambda x, y, s: x * s + (x * y),
        lambda x, y, s: x * y * s + s,
        lambda x, y, s: x * y - math.log(s + 1) + s,
        lambda x, y, s: math.cos(0.5 * x) * y + s,
        lambda x, y, s: math.cos(x * y) * y + s,
        lambda x, y, s: math.tan(y) * math.cos(x) + s,
        lambda x, y, s: math.sin(y) + x * s,
        lambda x, y, s: math.sin(x) + y * s,
        lambda x, y, s: math.sin(x * y) + y * x + s,
        lambda x, y, s: x * x - y * y + s,
        lambda x, y, s: (x * y - y * y) + s,
        lambda x, y, s: (x * y - y * y) % (s + 1),
        lambda x, y, s: (y * y + x * x) + s,
        lambda x, y, s: x * y * 2 - y * y * 2 + s,
        lambda x, y, s: (x / (y + 1)) + (y * y) + s,
        lambda x, y, s: ((x * x) / 2 * (y + 1)) + s,
        lambda x, y, s: x * y * (x + y) + s,
        lambda x, y, s: x * y * (s / (x + 1)),
        lambda x, y, s: (x * x * x) - (y * y * 2) + s,
        lambda x, y, s: x * 12 - y * 4 + s,
        lambda x, y, s: math.log10(x + 1) * (y * 2) + s
    ]

    def __init__(self, layout, frames_per=300, func=0, rand=True, fade_frames=30):
        super().__init__(layout)
        self.start_func = func
        self.frames_per = frames_per
        self.rand = rand
        self.fade_frames = fade_frames
        self.fade_step = 1.0 / fade_frames if fade_frames else 0.0

    def pre_run(self):
        self._step = 0
        self.count = 0
        self.fade_count = 0
        self.cur_func = random.choice(range(len(self.funcs))) if self.rand else self.start_func
        self.next_func = None

    def call_func(self, func, x, y, s):
        return abs(int(self.funcs[func](x, y, s))) % 360

    def step(self, amt=1):
        self.layout.all_off()
        for y in range(self.height):
            for x in range(self.width):
                h = self.call_func(self.cur_func, x, y, self._step)
                if self.next_func:
                    h_next = self.call_func(self.next_func, x, y, self._step)
                    h = hue_fade(h, h_next, self.fade_step * self.fade_count)
                c = colors.hue2rgb_360(h)
                self.layout.set(x, y, c)
        if self.next_func:
            self.fade_count += 1
            if self.fade_count >= self.fade_frames:
                self.cur_func = self.next_func
                self.next_func = None
                self.fade_count = 0
                self.count = 0
        else:
            self.count += 1
        if not self.next_func and self.frames_per and self.count >= self.frames_per:
            if self.rand:
                self.next_func = random.choice(range(len(self.funcs)))
            else:
                self.next_func = self.cur_func + 1
                if self.next_func >= len(self.funcs):
                    self.next_func = 0
                    self.state = 2
            self.count = 0
            if not self.fade_frames:
                self.cur_func = self.next_func
                self.next_func = None
        self._step += amt
