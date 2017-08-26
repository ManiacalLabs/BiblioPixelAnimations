from bibliopixel.animation import BaseCircleAnim
from bibliopixel import colors
import time


class ArcClock(BaseCircleAnim):

    def __init__(self, layout):
        super(ArcClock, self).__init__(layout)
        self.hands = [
            {
                'rings': [0, 1],
                'color': colors.Red,
                'segments': 60,
                'key': 'tm_sec'
            },
            {
                'rings': [2, 3],
                'color': colors.Green,
                'segments': 60,
                'key': 'tm_min'
            },
            {
                'rings': [4, 5],
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
            end = (360 / segs) * (getattr(t, h['key']) % segs)
            if end:
                for i in h['rings']:
                    self.layout.fillRing(i, h['color'], startAngle=0, endAngle=end)
