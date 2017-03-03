from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors
import time
from datetime import datetime, timedelta


class TallCountdown(BaseMatrixAnim):

    def __init__(self, led, target):
        super(TallCountdown, self).__init__(led)
        try:
            self.target = datetime.strptime(target, "%H:%M:%S").time()
        except Exception as e:
            raise Exception("Unable to parse target time!\n" + str(e))

    def getRemaining(self):
        n = datetime.now().time()
        dn = timedelta(hours=n.hour, minutes=n.minute, seconds=n.second)
        dt = timedelta(hours=self.target.hour,
                       minutes=self.target.minute, seconds=self.target.second)
        l = (dt - dn)
        return (l.seconds // 3600, (l.seconds % 3600) // 60, l.seconds % 60)

    def step(self, amt):
        self._led.setTexture([[colors.hue_helper(
            self.height - y, self.height, self._step * 2)] * self.width for y in range(self.height)])
        self._led.all_off()
        hrs, mins, sec = self.getRemaining()
        if(hrs + mins + sec == 0):
            self.animComplete = True

        hrs = str(hrs).zfill(2)
        mins = str(mins).zfill(2)
        sec = str(sec).zfill(2)
        self._led.drawText(hrs, x=2, y=2, font_scale=2)
        self._led.drawText(mins, x=2, y=18, font_scale=2)
        self._led.drawText(sec, x=2, y=34, font_scale=2)

        self._step += amt
        self._led.setTexture(tex=None)


MANIFEST = [
    {
        "class": TallCountdown,
        "controller": "matrix",
        "desc": "Countdown for tall display. Nothin happens when complete aside from setting the animComplete flag and starting the countdown again. The intent is to run with untilComplete and queue up some other animation to happen when this animation completes.",
        "display": "Tall Countdown",
        "id": "TallCountdown",
        "params": [{
            "label": "Target Time",
            "id": "target",
            "type": "str",
            "default": "00:00:00",
            "help": "Countdown target time in hh:mm:ss (24-hour) format."
        }],
        "type": "animation"
    }
]
