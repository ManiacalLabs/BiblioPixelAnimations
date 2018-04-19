from bibliopixel.animation import BaseStripAnim
import bibliopixel.colors as colors


class ColorFade(BaseStripAnim):
    """Fill the dots progressively along the strip."""

    def wave_range(self, start, peak, step):
        main = [i for i in range(start, peak + 1, step)]
        return main + [i for i in reversed(main[0:len(main) - 1])]

    def __init__(self, layout, colors=[colors.Red], step=5, start=0, end=-1):
        super(ColorFade, self).__init__(layout, start, end)
        self._colors = colors
        self._levels = self.wave_range(30, 255, step)
        self._level_count = len(self._levels)
        self._color_count = len(colors)

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        if self._step > self._level_count * self._color_count:
            self._step = 0

        c_index = (self._step // self._level_count) % self._color_count
        l_index = (self._step % self._level_count)
        color = self._colors[c_index]

        self.layout.fill(colors.color_scale(color, self._levels[l_index]), self._start, self._end)

        self._step += amt
