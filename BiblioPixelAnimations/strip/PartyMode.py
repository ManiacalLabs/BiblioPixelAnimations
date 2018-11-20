from bibliopixel.animation.strip import Strip
from bibliopixel.colors import COLORS


class PartyMode(Strip):
    """Stobe Light Effect."""
    COLOR_DEFAULTS = ('colors', [COLORS.Red, COLORS.Green, COLORS.Blue]),

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
