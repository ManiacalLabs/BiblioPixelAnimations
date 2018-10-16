from bibliopixel.animation import BaseStripAnim
import bibliopixel.colors as colors


class ColorFade(BaseStripAnim):
    """Fill the dots progressively along the strip."""
    COLOR_DEFAULTS = ('colors', [colors.Red]),

    def wave_range(self, start, peak, step):
        main = [i for i in range(start, peak + 1, step)]
        return main + [i for i in reversed(main[0:len(main) - 1])]

    def __init__(self, layout, step=5, start=0, end=-1, **kwds):
        super().__init__(layout, start, end, **kwds)
        self._levels = self.wave_range(30, 255, step)
        self._level_count = len(self._levels)

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        c_index, l_index = divmod(self._step, self._level_count)
        color = self.palette(c_index)
        color = colors.color_scale(color, self._levels[l_index])
        self.layout.fill(color, self._start, self._end)
        self._step += amt
