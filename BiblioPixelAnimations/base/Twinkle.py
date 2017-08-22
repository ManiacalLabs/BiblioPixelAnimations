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

from bibliopixel import colors as bp_colors
import random


# Base class to be used by any display type

class TwinkleBase:
    def __init__(self, layout, colors=[bp_colors.Red, bp_colors.Green, bp_colors.Blue],
                 density=20, speed=2, max_bright=255):
        self.layout = layout
        self.colors = colors
        self.density = density
        self.speed = speed
        self.max_bright = max_bright

        # Make sure speed, density & max_bright are in sane ranges
        self.speed = min(self.speed, 100)
        self.speed = max(self.speed, 2)
        self.density = min(self.density, 100)
        self.density = max(self.density, 2)
        self.max_bright = min(self.max_bright, 255)
        self.max_bright = max(self.max_bright, 5)

    def pre_run(self):
        self._step = 0
        # direction, color, level
        self.pixels = [(0, bp_colors.Off, 0)] * self.layout.numLEDs

    def pick_led(self, speed):
        idx = random.randrange(0, self.layout.numLEDs)
        p_dir, p_color, p_level = self.pixels[idx]

        if random.randrange(0, 100) < self.density:
            if p_dir == 0:  # 0 is off
                p_level += speed
                p_dir = 1  # 1 is growing
                p_color = random.choice(self.colors)
                self.layout._set_base(idx, bp_colors.color_scale(p_color, p_level))

                self.pixels[idx] = p_dir, p_color, p_level

    def step(self, amt=1):
        self.layout.all_off()
        self.pick_led(self.speed)

        for i, val in enumerate(self.pixels):
            p_dir, p_color, p_level = val
            if p_dir == 1:
                p_level += self.speed
                if p_level > 255:
                    p_level = 255
                    p_dir = 2  # start dimming
                self.layout._set_base(i, bp_colors.color_scale(p_color, p_level))
            elif p_dir == 2:
                p_level -= self.speed
                if p_level < 0:
                    p_level = 0
                    p_dir = 0  # turn off
                self.layout._set_base(i, bp_colors.color_scale(p_color, p_level))

            self.pixels[i] = (p_dir, p_color, p_level)

        self._step += amt
