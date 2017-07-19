from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors
import time


class TallClock(BaseMatrixAnim):

    def __init__(self, layout):
        super(TallClock, self).__init__(layout)

    def step(self, amt):
        self.layout.setTexture([[colors.hue_helper(
            y, self.height, self._step * 2)] * self.width for y in range(self.height)])
        self.layout.all_off()
        t = time.localtime()
        hrs = str(t.tm_hour).zfill(2)
        mins = str(t.tm_min).zfill(2)
        sec = str(t.tm_sec).zfill(2)
        self.layout.drawText(hrs, x=2, y=2, font_scale=2)
        self.layout.drawText(mins, x=2, y=18, font_scale=2)
        self.layout.drawText(sec, x=2, y=34, font_scale=2)

        self._step += amt
        self.layout.setTexture(tex=None)
