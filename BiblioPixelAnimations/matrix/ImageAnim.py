import fractions, glob, os, pathlib, random, threading, time
from bibliopixel.animation.matrix import Matrix
from bibliopixel.util import log
from bibliopixel.colors import COLORS
from bibliopixel.colors.arithmetic import color_scale

try:
    from PIL import Image, ImageSequence
except ImportError:
    error = "Please install Python Imaging Library: pip install pillow"
    log.error(error)

ROOT = pathlib.Path(__file__).parents[2]
DEFAULT_ANIM = ROOT / 'Graphics' / 'MarioRotating.gif'


class LoadNextThread(threading.Thread):
    def __init__(self, imganim):
        super().__init__()
        self.setDaemon(True)
        self._stop_event = threading.Event()
        self._wait_event = threading.Event()
        self.anim = imganim

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.isSet()

    def loading(self):
        return self._wait_event.isSet()

    def loadNext(self):
        self._wait_event.set()

    def run(self):
        while not self.stopped():
            self._wait_event.wait()
            self.anim.loadNextGIF()
            self._wait_event.clear()


class ImageAnim(Matrix):
    def __init__(
            self, layout, imagePath=None, offset=(0, 0), bgcolor=COLORS.Off,
            brightness=255, cycles=1, seconds=None, random=False,
            use_file_fps=True, use_gamma=True, scale_to=None, **kwds):
        """
        Animation class for displaying image animations for GIF files or a set of
        bitmaps

        layout:
            layout.Matrix instance

        imagePath:
            Path to either a single animated GIF image or folder of GIF files

        offset:
            X, Y coordinates of the top-left corner of the image

        bgcolor:
            RGB tuple color to replace any transparent pixels with.
            Avoids transparent showing as black

        brightness:
            Brightness value (0-255) to scale the image by.
            Otherwise uses master brightness at the time of creation

        use_gamma:
            If true, use the driver's gamma on the raw image data.
            TODO: why do we do this?

        scale_to:
            Which dimensions to scale the image to?
            None:  Don't scale
            'x':   Scale to use full width
            'y':   Scale to use full height
            'xy':  Scale both width and height
            'fit:  Use best fit from 'x' or 'y'
        """
        super().__init__(layout, **kwds)

        self.cycles = cycles
        self.cycle_count = 0

        self.seconds = seconds
        self.last_start = 0

        self.random = random
        self.use_file_fps = use_file_fps

        self._bright = brightness
        self._bgcolor = color_scale(bgcolor, self._bright)
        self._offset = offset
        self._image_buffers = [None, None]
        self._cur_img_buf = 1  # start here because loadNext swaps it

        self.imagePath = imagePath or str(DEFAULT_ANIM)
        self.folder_mode = os.path.isdir(self.imagePath)
        self.gif_files = []
        self.gif_indices = []
        self.folder_index = -1
        self.load_thread = None
        self.use_gamma = use_gamma
        self.scale_to = scale_to and SCALE_TO[scale_to]

        if self.folder_mode:
            self.gif_files = glob.glob(self.imagePath + "/*.gif")
            self.gif_indices = list(range(len(self.gif_files)))
            self.loadNextGIF()  # first load is manual
            self.swapbuf()
            self.load_thread = None
        else:
            self.loadGIFFile(self.imagePath)
            self.swapbuf()

    def cleanup(self, clean_layout=True):
        if self.load_thread:
            self.load_thread.stop()
        super().cleanup(clean_layout)

    def pre_run(self):
        if self.folder_mode:
            if not self.load_thread or not self.load_thread.is_alive():
                self.load_thread = LoadNextThread(self)
                self.load_thread.start()

            self.load_thread.loadNext()
            self.last_start = time.time()

        self._curImage = 0

    def loadGIFFile(self, gif):
        _, ext = os.path.splitext(gif)
        next_buf = self.next_img_buf()
        if not ext.lower().endswith("gif"):
            raise ValueError('Must be a GIF file!')

        log.debug("Loading {0} ...".format(gif))
        self._image_buffers[next_buf] = self._loadGIFSequence(gif)

    def _getBufferFromImage(self, img, ox, oy):
        frame = Image.new('RGBA', img.size)
        frame.paste(img)

        if self.scale_to:
            ix, iy = frame.size
            rx, ry = self.scale_to(fractions.Fraction(self.width, ix),
                                   fractions.Fraction(self.height, iy))
            new_size = round(rx * ix), round(ry * iy)
            resamp = Image.LANCZOS if rx * ry < 1 else Image.BICUBIC
            frame = frame.resize(new_size, resamp)

        duration = img.info.get('duration')
        w = min(self.layout.width - ox, frame.size[0])
        h = min(self.layout.height - oy, frame.size[1])

        buffer = [0] * (self.layout.numLEDs * 3)

        if self.use_gamma:
            gamma = self.layout.drivers[0].gamma

            def apply_gamma(i, color):
                buffer[i:i + 3] = (gamma.get(c) for c in color)
        else:
            def apply_gamma(i, color):
                buffer[i:i + 3] = color

        if self._bgcolor != (0, 0, 0):
            for i in range(0, 3 * self.layout.numLEDs, ):
                apply_gamma(i, self._bgcolor)

        for x in range(max(ox, 0), w + ox):
            for y in range(max(oy, 0), h + oy):
                pixel = self.layout.coord_map[y][x]
                *color, a = frame.getpixel((x - ox, y - oy))
                if a:
                    color = tuple((c * a) >> 8 for c in color)
                else:
                    color = self._bgcolor
                apply_gamma(3 * pixel, color)

        return (duration, buffer)

    def _loadGIFSequence(self, imagePath):
        img = Image.open(imagePath)
        if any(self._offset):
            ox, oy = self._offset
        elif self.scale_to:
            ox, oy = 0, 0
        else:
            ox = max(0, (self.layout.width - img.size[0]) // 2)
            oy = max(0, (self.layout.height - img.size[1]) // 2)

        return [self._getBufferFromImage(frame, ox, oy)
                for frame in ImageSequence.Iterator(img)]

    def loadNextGIF(self):
        if self.random:
            if len(self.gif_indices) < 2:
                self.folder_index = self.gif_indices[0]
                self.gif_indices = list(range(len(self.gif_files)))
            else:
                index = random.randrange(len(self.gif_indices))
                self.folder_index = self.gif_indices.pop(index)
        else:
            self.folder_index += 1
            if self.folder_index >= len(self.gif_files):
                self.folder_index = 0
        self.loadGIFFile(self.gif_files[self.folder_index])

    def next_img_buf(self):
        i = self._cur_img_buf
        i += 1
        if i > 1:
            i = 0
        return i

    def swapbuf(self):
        self._cur_img_buf = self.next_img_buf()

    def step(self, amt=1):
        self.layout.all_off()
        img = self._image_buffers[self._cur_img_buf]

        self.layout.setBuffer(img[self._curImage][1])
        if self.use_file_fps:
            self.internal_delay = img[self._curImage][0] / 1000.0

        self._curImage += 1
        if self._curImage >= len(img):
            self._curImage = 0
            if self.folder_mode:
                loadnext = False
                if self.seconds:
                    if ((time.time() - self.last_start) > self.seconds):
                        loadnext = True
                else:
                    if self.cycle_count < self.cycles - 1:
                        self.cycle_count += 1
                    else:
                        loadnext = True

                if loadnext and not self.load_thread.loading():
                    # wait another cycle if still loading
                    self.animComplete = True
                    self.load_thread.loadNext()
                    self.swapbuf()
                    self.cycle_count = 0
                    self.last_start = time.time()
            else:
                self.animComplete = True


SCALE_TO = {
    'x': lambda rx, ry: (rx, 1),
    'y': lambda rx, ry: (1, ry),
    'xy': lambda rx, ry: (rx, ry),
    'fit': lambda rx, ry: (min(rx, ry), min(rx, ry)),
}
