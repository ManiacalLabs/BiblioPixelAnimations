from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors
import time


class TallClock(BaseMatrixAnim):

    def __init__(self, led):
        super(TallClock, self).__init__(led)

    def step(self, amt):
        self._led.setTexture([[colors.hue_helper(
            y, self.height, self._step * 2)] * self.width for y in range(self.height)])
        self._led.all_off()
        t = time.localtime()
        hrs = str(t.tm_hour).zfill(2)
        mins = str(t.tm_min).zfill(2)
        sec = str(t.tm_sec).zfill(2)
        self._led.drawText(hrs, x=2, y=2, font_scale=2)
        self._led.drawText(mins, x=2, y=18, font_scale=2)
        self._led.drawText(sec, x=2, y=34, font_scale=2)

        self._step += amt
        self._led.setTexture(tex=None)


MANIFEST = [
    {
        "class": TallClock,
        "controller": "matrix",
        "desc": "Clock for tall display",
        "display": "Tall Clock",
        "id": "TallClock",
        "params": [],
        "type": "animation"
    }
]
