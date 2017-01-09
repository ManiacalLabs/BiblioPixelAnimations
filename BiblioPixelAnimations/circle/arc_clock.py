from bibliopixel.animation import BaseCircleAnim
from bibliopixel import colors
import time


class ArcClock(BaseCircleAnim):

    def __init__(self, led):
        super(ArcClock, self).__init__(led)
        last = self.lastRing
        self.hands = [
            {
                'rings': [last - 0, last - 1],
                'color': colors.Red,
                'segments': 60,
                'key': 'tm_sec'
            },
            {
                'rings': [last - 2, last - 3],
                'color': colors.Green,
                'segments': 60,
                'key': 'tm_min'
            },
            {
                'rings': [last - 4, last - 5],
                'color': colors.Blue,
                'segments': 12,
                'key': 'tm_hour'
            }
        ]

    def step(self, amt=1):
        self._led.all_off()
        t = time.localtime()
        # t.tm_hour
        # t.tm_min
        # t.tm_sec
        for h in self.hands:
            segs = h['segments']
            end = (360 / segs) * (getattr(t, h['key']) % segs)
            if end:
                for i in h['rings']:
                    self._led.fillRing(i, h['color'],
                                       startAngle=0, endAngle=end)


rainbow = [colors.Red, colors.Orange, colors.Yellow,
           colors.Green, colors.Blue, colors.Purple]

MANIFEST = [
    {
        "class": ArcClock,
        "controller": "circle",
        "desc": None,
        "display": "ArcClock",
        "id": "ArcClock",
        "params": [],
        "type": "animation"
    }
]
