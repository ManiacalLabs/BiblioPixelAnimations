import time
from bibliopixel.animation.circle import Circle
from bibliopixel.colors import COLORS


class ArcClock(Circle):

    def __init__(self, layout, **kwds):
        super().__init__(layout, **kwds)
        self.hands = [
            {
                'rings': [0, 1],
                'color': COLORS.Red,
                'segments': 60,
                'key': 'tm_sec'
            },
            {
                'rings': [2, 3],
                'color': COLORS.Green,
                'segments': 60,
                'key': 'tm_min'
            },
            {
                'rings': [4, 5],
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
            end = (360 / segs) * (getattr(t, h['key']) % segs)
            if end:
                for i in h['rings']:
                    self.layout.fillRing(
                        i, h['color'], startAngle=0, endAngle=end)
