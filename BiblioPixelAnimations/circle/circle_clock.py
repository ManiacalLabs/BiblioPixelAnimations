import time
from bibliopixel.animation.circle import Circle
from bibliopixel.colors import COLORS


class CircleClock(Circle):

    def __init__(self, layout, **kwds):
        super().__init__(layout, **kwds)
        last = self.lastRing
        self.hands = [
            {
                'radius': last - 0,
                'color': COLORS.Red,
                'segments': 60,
                'key': 'tm_sec'
            },
            {
                'radius': last - 2,
                'color': COLORS.Green,
                'segments': 60,
                'key': 'tm_min'
            },
            {
                'radius': last - 4,
                'color': COLORS.Blue,
                'segments': 12,
                'key': 'tm_hour'
            }
        ]

    def step(self, amt=1):
        self.layout.all_off()
        t = time.localtime()

        for h in self.hands:
            segs = h['segments']
            angle = (360 / segs) * (getattr(t, h['key']) % h['segments'])
            self.layout.drawRadius(angle, h['color'], endRing=h['radius'])
