from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors
import time


class OneKClock(BaseMatrixAnim):

    def __init__(self, layout):
        super().__init__(layout)

    def step(self, amt):
        self.layout.setTexture([[colors.hue_helper(
            y, self.height, self._step * 2)] * self.width for y in range(self.height)])
        self.layout.all_off()
        t = time.localtime()
        hrs = str(t.tm_hour).zfill(2)
        mins = str(t.tm_min).zfill(2)
        secs = str(t.tm_sec).zfill(2)
        self.layout.drawText(hrs, x=0, y=0, font_scale=2)
        self.layout.drawText(mins, x=0, y=18, font_scale=2)
        self.layout.drawText(secs[0], x=24, y=8)
        self.layout.drawText(secs[1], x=24, y=17)

        self._step += amt
        self.layout.setTexture(tex=None)
