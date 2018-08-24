from bibliopixel.animation import BaseCubeAnim
import bibliopixel.colors as colors
from bibliopixel import log
from . system_eq import EQ
from bibliopixel import matrix


class BaseSpectrumDraw(object):

    def __init__(self, frame):
        self.frame = frame
        self.width = frame.x
        self.height = frame.y
        self.height_map = [((i * (self.height - 1)) // (1023))
                           for i in range(1024)]
        self.width_map = [((i * (self.width - 1)) // (1023))
                          for i in range(1024)]

    def draw(self, data):
        raise NotImplementedError("Cannot call draw on the base class.")

    def draw_bar(self, x, y, w, h, c, fill=True):
        if w > 1:
            if fill:
                self.frame.fill_rect(x, y, w, h, c)
            else:
                self.frame.draw_rect(x, y, w, h, c)
        else:
            self.frame._draw_fast_vline(x, y, h, c)

    def color_map(self, width, offset=0):
        return [colors.hue2rgb((((i * (255)) // (width - 1)) + offset) % 256) for i in range(width)]


class PeakLineGraph(BaseSpectrumDraw):

    def __init__(self, frame):
        super(PeakLineGraph, self).__init__(frame)
        self.peak_dots = True
        self.peaks = [0] * self.width

    def draw(self, data, amt=1):
        chan = len(data)
        bar_w = int(self.width // chan)
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
                        self.frame.set(pos + i, self.height -
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

    def __init__(self, frame):
        super(BasicLineGraph, self).__init__(frame)
        self.peak_dots = False


class Spread(BaseSpectrumDraw):

    def __init__(self, frame):
        super(Spread, self).__init__(frame)
        self.center_line = self.height // 2
        self.offset = 0
        self.color_offset = 0
        self.inverse = False
        self.scroll = False

    def draw(self, data, amt=1):
        chan = len(data)
        color_list = self.color_map(chan, self.color_offset)
        bar_w = int(self.width // chan)
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
    def __init__(self, frame):
        super(ScrollSpread, self).__init__(frame)
        self.scroll = True


class InverseSpread(Spread):
    def __init__(self, frame):
        super(InverseSpread, self).__init__(frame)
        self.inverse = True


class InverseScrollSpread(Spread):
    def __init__(self, frame):
        super(InverseScrollSpread, self).__init__(frame)
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


class FrameDraw(object):
    def __init__(self, anim):
        self.x = anim.x
        self.y = anim.y
        self.frame = [[(0, 0, 0)] * anim.x] * anim.y

    def set(self, x, y, color):
        self.frame[y][x] = color

    def draw_rect(self, x, y, w, h, color):
        matrix.draw_rect(self.set, x, y, w, h, color)

    def fill_rect(self, x, y, w, h, color):
        matrix.fill_rect(self.set, x, y, w, h, color)

    def _draw_fast_vline(self, x, y, h, color):
        matrix._draw_fast_vline(self.set, x, y, h, color)


class Spectrum(BaseCubeAnim):

    def __init__(self, layout, vis_list=None, steps_per_vis=None,
                 bins=64, max_freq=4000, log_scale=True, auto_gain=False, gain=3):

        super(Spectrum, self).__init__(layout)
        self.source = EQ(bins=bins, max_freq=max_freq,
                         log_scale=log_scale, auto_gain=auto_gain, gain=gain)

        self.x, self.y, self.z = layout.x, layout.y, layout.z

        self.frames = [[[(0, 0, 0)] * self.x] * self.y] * self.z
        self.frame = FrameDraw(self)

        self.draw_obj = None
        self.steps_per_vis = steps_per_vis

        self.vis_dict = {}
        for v in DEFAULT_VIS_LIST:
            self.vis_dict[v.__name__] = v(self.frame)

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

        print(self.frame.frame)
        self.frames[0] = self.frame.frame[:]

        for z in range(1):
            for y in range(self.y):
                for x in range(self.x):
                    self.layout.set(x, y, z, self.frames[z][y][x])

        if self.steps_per_vis:
            self._step += 1
            if self._step % self.steps_per_vis == 0:
                self.next_draw_obj()
