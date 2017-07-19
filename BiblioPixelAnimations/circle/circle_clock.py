from bibliopixel.animation import BaseCircleAnim
from bibliopixel import colors
import time


class CircleClock(BaseCircleAnim):

    def __init__(self, layout):
        super(CircleClock, self).__init__(layout)
        last = self.lastRing
        self.hands = [
            {
                'radius': last - 0,
                'color': colors.Red,
                'segments': 60,
                'key': 'tm_sec'
            },
            {
                'radius': last - 2,
                'color': colors.Green,
                'segments': 60,
                'key': 'tm_min'
            },
            {
                'radius': last - 4,
                'color': colors.Blue,
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
