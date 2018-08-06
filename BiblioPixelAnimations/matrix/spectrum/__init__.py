from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors
from bibliopixel import log
from . system_eq import EQ


class BaseSpectrumDraw(object):

    def __init__(self, anim):
        self.anim = anim
        self.width = anim.width
        self.height = anim.height
        self.led = anim._led
        self.height_map = [((i * (self.height - 1)) // (1023))
                           for i in range(1024)]
        self.width_map = [((i * (self.width - 1)) // (1023))
                          for i in range(1024)]

    def draw(self, data):
        raise NotImplementedError("Cannot call draw on the base class.")

    def draw_bar(self, x, y, w, h, c, fill=True):
        if w > 1:
            if fill:
                self.led.fillRect(x, y, w, h, c)
            else:
                self.led.drawRect(x, y, w, h, c)
        else:
            self.led._drawFastVLine(x, y, h, c)

    def color_map(self, width, offset=0):
        return [colors.hue2rgb((((i * (255)) // (width - 1)) + offset) % 256) for i in range(width)]


class PeakLineGraph(BaseSpectrumDraw):

    def __init__(self, anim):
        super(PeakLineGraph, self).__init__(anim)
        self.peak_dots = True
        self.peaks = [0] * self.width

    def draw(self, data, amt=1):
        chan = len(data)
        bar_w = int(self.width / chan)
        pos = (self.width - (bar_w * chan)) // 2

        color_list = self.color_map(chan)

        count = 0
        for level in data:
            c = color_list[count]
            h = self.height_map[level]
            if h:
                self.draw_bar(pos, self.height - h, bar_w, h, c, fill=True)

            if self.peak_dots:
                if self.peaks[count] > 0 and self.peaks[count] > h:
                    for i in range(bar_w):
                        self.led.set(pos + i, self.height -
                                     self.peaks[count], c)
                if h >= self.peaks[count]:
                    self.peaks[count] = h
                else:
                    self.peaks[count] -= 1
                if self.peaks[count] < 0:
                    self.peaks[count] = 0

            pos += bar_w
            count += 1


class BasicLineGraph(PeakLineGraph):

    def __init__(self, anim):
        super(BasicLineGraph, self).__init__(anim)
        self.peak_dots = False


class Spread(BaseSpectrumDraw):

    def __init__(self, anim):
        super(Spread, self).__init__(anim)
        self.center_line = self.height // 2
        self.offset = 0
        self.color_offset = 0
        self.inverse = False
        self.scroll = False

    def draw(self, data, amt=1):
        chan = len(data)
        color_list = self.color_map(chan, self.color_offset)
        bar_w = int(self.width / chan)
        pos = (self.width - (bar_w * chan)) // 2
        for i in range(chan):
            h = self.height_map[data[(i + self.offset) % len(data)]]
            c = color_list[i]
            if self.inverse:
                self.draw_bar(pos, 0, bar_w, self.center_line - h, c)
                self.draw_bar(pos, self.center_line + h, bar_w, self.height - h, c)
            else:
                if h:
                    self.draw_bar(pos, self.center_line - h, bar_w, h, c)
                    self.draw_bar(pos, self.center_line, bar_w, h, c)
            pos += bar_w
        if self.scroll:
            self.offset += amt
        self.color_offset += amt


class ScrollSpread(Spread):
    def __init__(self, anim):
        super(ScrollSpread, self).__init__(anim)
        self.scroll = True


class InverseSpread(Spread):
    def __init__(self, anim):
        super(InverseSpread, self).__init__(anim)
        self.inverse = True


class InverseScrollSpread(Spread):
    def __init__(self, anim):
        super(InverseScrollSpread, self).__init__(anim)
        self.scroll = True
        self.inverse = True


DEFAULT_VIS_LIST = [
    Spread,
    ScrollSpread,
    InverseSpread,
    InverseScrollSpread,
    PeakLineGraph,
    BasicLineGraph
]


class Spectrum(BaseMatrixAnim):

    def __init__(self, layout, vis_list=None, steps_per_vis=None,
                 bins=64, max_freq=4000, log_scale=True, auto_gain=False, gain=3):

        super(Spectrum, self).__init__(layout)
        self.source = EQ(bins=bins, max_freq=max_freq,
                         log_scale=log_scale, auto_gain=auto_gain, gain=gain)
        self.draw_obj = None
        self.steps_per_vis = steps_per_vis

        self.vis_dict = {}
        for v in DEFAULT_VIS_LIST:
            self.vis_dict[v.__name__] = v(self)

        self.vis_list = vis_list
        if not self.vis_list:
            self.vis_list = [v.__name__ for v in DEFAULT_VIS_LIST]

        self.cur_vis = len(self.vis_list)
        self.next_draw_obj()

    def pre_run(self):
        self.source.start()

    def _exit(self, type, value, traceback):
        self.source.stop()

    def next_draw_obj(self):
        self.cur_vis += 1
        if self.cur_vis >= len(self.vis_list):
            self.cur_vis = 0
        if self.draw_obj:
            del self.draw_obj
        name = self.vis_list[self.cur_vis]
        log.debug("Loading {}".format(name))
        self.draw_obj = self.vis_dict[name]

    def step(self, amt=1):
        assert self.draw_obj, "No loaded visualizers!"
        self.layout.all_off()
        data = self.source.get_audio_data()
        self.draw_obj.draw(data, amt)

        if self.steps_per_vis:
            self._step += 1
            if self._step % self.steps_per_vis == 0:
                self.next_draw_obj()


def get_vis_options():
    options = {}
    options_map = [v.__name__ for v in DEFAULT_VIS_LIST]
    count = 0
    for name in options_map:
        options[name] = name
        count += 1

    return (options, options_map)
