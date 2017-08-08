from bibliopixel.animation import BaseCircleAnim
from bibliopixel import colors
import time


class RingClock(BaseCircleAnim):

    def __init__(self, layout,
                 c_hour=colors.Red, c_min=colors.Green, c_sec=colors.Blue,
                 ring_hour=0, ring_min=0, ring_sec=0,
                 tail_hour=6, tail_min=6, tail_sec=6):
        super().__init__(layout)
        self.hands = [
            {
                'ring': ring_sec,
                'tail': tail_sec,
                'color': c_sec,
                'segments': 60,
                'key': 'tm_sec'
            },
            {
                'ring': ring_min,
                'tail': tail_min,
                'color': c_min,
                'segments': 60,
                'key': 'tm_min'
            },
            {
                'ring': ring_hour,
                'tail': tail_hour,
                'color': c_hour,
                'segments': 12,
                'key': 'tm_hour'
            }
        ]

    def step(self, amt=1):
        self.layout.all_off()
        t = time.localtime()
        for h in self.hands:
            segs = h['segments']
            point = (360 / segs) * (getattr(t, h['key']) % segs)
            self.layout.set(h['ring'], point, h['color'])
            if h['tail'] > 0:
                for i in range(h['tail']):
                    scaled = colors.color_scale(h['color'], 255 - ((256 // h['tail']) * i))
                    self.layout.set(h['ring'], point + i, scaled)
                    self.layout.set(h['ring'], point - i, scaled)
