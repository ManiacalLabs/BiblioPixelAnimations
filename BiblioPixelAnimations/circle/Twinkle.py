#  ## Twinkle ##
# This Bibliopixel animation randomly picks leds and slowly brightens them to a max brightness
# then dims them to off.
# Based on BPA.strip.WhiteTwinkle and modified by Adam Haile
#
#  ## Usage ##
#
#  colors -      List of colors to use
#  speed   -    How fast the leds bighten then dim (best in range 2-40)
#  density -    How often to light a new pixel
#  max_bright - The maximum brightness, some leds twinkle better if they ramp to less than full
#                 brightness (19 - 255). Lower brightness also speeds up the twinkle rate.

from .. base.Twinkle import TwinkleBase
from bibliopixel.animation import BaseCircleAnim


class Twinkle(BaseCircleAnim):
    def __init__(self, layout, **kwds):
        super().__init__(layout)
        self.base = TwinkleBase(layout, **kwds)
        self.pre_run = self.base.pre_run
        self.step = self.base.step
