from bibliopixel.animation import BaseStripAnim
from bibliopixel import colors


class PartyMode(BaseStripAnim):
    """Stobe Light Effect."""
    COLOR_DEFAULTS = ('colors', [colors.Red, colors.Green, colors.Blue]),

    def __init__(self, layout, start=0, end=-1, **kwds):
        super().__init__(layout, start, end, **kwds)

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        amt = 1  # anything other than 1 would be just plain silly

        if self._step % 2 == 0:
            color = self.palette(self._step / 2)
            self.layout.fill(color, self._start, self._end)
        else:
            self.layout.all_off()

        self._step += amt
