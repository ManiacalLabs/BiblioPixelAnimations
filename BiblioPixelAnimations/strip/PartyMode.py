from bibliopixel.animation import BaseStripAnim
from bibliopixel import colors


class PartyMode(BaseStripAnim):
    """Stobe Light Effect."""

    def __init__(self, layout, colors=[colors.Red, colors.Green, colors.Blue], start=0, end=-1):
        super(PartyMode, self).__init__(layout, start, end)
        self._colors = colors
        self._color_count = len(colors)

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        amt = 1  # anything other than 1 would be just plain silly
        if self._step > (self._color_count * 2) - 1:
            self._step = 0

        if self._step % 2 == 0:
            self.layout.fill(self._colors[self._step // 2], self._start, self._end)
        else:
            self.layout.all_off()

        self._step += amt
