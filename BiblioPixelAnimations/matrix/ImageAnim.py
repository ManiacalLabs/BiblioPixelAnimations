# Usage
# Run the animation in "pacman.gif" for 5 total cycles. When loading from an animated GIF file, the timing of each frame is automatically loaded from the file but if a different, constant time is needed the "fps" or "sleep" parameters of run() can be used.
#
# ```python
# import bibliopixel.image as image
# anim = image.ImageAnim(led, "./anims/pacman.gif")
# anim.run(untilComplete = True, max_cycles = 5)
# ```
#
# Run the animation from sequential files stored in "./anim/supermario". Files are loaded in alpha/numeric order. To ensure files load in the same order on all systems, best practice is to name the files as: 001.bmp, 002.bmp, 003.bmp, 004.bmp, etc...
#
# Note that when loading static files as a sequence, the "fps" or "sleep" parameters of run() are required to control the timing between each frame. Like above, untilComplete and max_cycles are still valid when using static sequences.
#
# ```python
# import bibliopixel.image as image
# anim = image.ImageAnim(led, "./anims/supermario/")
# anim.run()
# ```

from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.log as log

try:
    from PIL import Image, ImageSequence
except ImportError as e:
    error = "Please install Python Imaging Library: pip install pillow"
    log.logger.error(error)
    raise ImportError(error)

import glob
import os
import bibliopixel.colors as colors
import threading
import random as rand


def _getBufferFromImage(img, led, bgcolor, bright, offset):
    duration = None
    if 'duration' in img.info:
        duration = img.info['duration']

    w = led.width - offset[0]
    if img.size[0] < w:
        w = img.size[0]

    h = led.height - offset[1]
    if img.size[1] < h:
        h = img.size[1]

    ox = offset[0]
    oy = offset[1]

    buffer = [0 for x in range(led.numLEDs * 3)]
    gamma = led.driver[0].gamma
    if bgcolor != (0, 0, 0):
        for i in range(led.numLEDs):
            buffer[i * 3 + 0] = gamma[bgcolor[0]]
            buffer[i * 3 + 1] = gamma[bgcolor[1]]
            buffer[i * 3 + 2] = gamma[bgcolor[2]]

    frame = Image.new("RGBA", img.size)
    frame.paste(img)

    for x in range(ox, w + ox):
        for y in range(oy, h + oy):
            if x < 0 or y < 0:
                continue
            pixel = led.matrix_map[y][x]
            r, g, b, a = frame.getpixel((x - ox, y - oy))
            if a == 0:
                r, g, b = bgcolor
            else:
                r = (r * a) >> 8
                g = (g * a) >> 8
                b = (b * a) >> 8
            if bright != 255:
                r, g, b = colors.color_scale((r, g, b), bright)

            buffer[pixel * 3 + 0] = gamma[r]
            buffer[pixel * 3 + 1] = gamma[g]
            buffer[pixel * 3 + 2] = gamma[b]

    return (duration, buffer)


def _loadGIFSequence(imagePath, led, bgcolor, bright, offset):
    img = Image.open(imagePath)
    if offset == (0, 0):
        w = 0
        h = 0
        if img.size[0] < led.width:
            w = (led.width - img.size[0]) / 2
        if img.size[1] < led.height:
            h = (led.height - img.size[1]) / 2
        offset = (w, h)

    images = []
    count = 0
    for frame in ImageSequence.Iterator(img):
        images.append(
            _getBufferFromImage(frame, led, bgcolor, bright, offset))
        count += 1

    return images


class loadnextthread(threading.Thread):

    def __init__(self, imganim):
        super(loadnextthread, self).__init__()
        self.setDaemon(True)
        self._stop = threading.Event()
        self._wait = threading.Event()
        self.anim = imganim

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def loading(self):
        return self._wait.isSet()

    def loadNext(self):
        self._wait.set()

    def run(self):
        while not self.stopped():
            self._wait.wait()
            self.anim.loadNextGIF()
            self._wait.clear()


class ImageAnim(BaseMatrixAnim):
    def __init__(self, led, imagePath, offset=(0, 0), bgcolor=colors.Off, brightness=255, cycles=1, random=False, use_file_fps=True):
        """Helper class for displaying image animations for GIF files or a set of bitmaps

        led - LEDMatrix instance
        imagePath - Path to either a single animated GIF image or folder of GIF files
        offset - X,Y tuple coordinates at which to place the top-left corner of the image
        bgcolor - RGB tuple color to replace any transparent pixels with. Avoids transparent showing as black
        brightness - Brightness value (0-255) to scale the image by. Otherwise uses master brightness at the time of creation
        """
        super(ImageAnim, self).__init__(led)

        self.cycles = cycles
        self.cycle_count = 0

        self.random = random
        self.use_file_fps = use_file_fps

        self._bright = brightness
        if self._bright == 255 and led.masterBrightness != 255:
            self._bright = led.masterBrightness

        self._bgcolor = colors.color_scale(bgcolor, self._bright)
        self._offset = offset
        self._image_buffers = [None, None]
        self._cur_img_buf = 1  # start here because loadNext swaps it

        self.folder_mode = os.path.isdir(imagePath)
        self.gif_files = []
        self.gif_indices = []
        self.folder_index = -1
        self.load_thread = None

        if self.folder_mode:
            self.gif_files = glob.glob(imagePath + "/*.gif")
            self.gif_indices = range(len(self.gif_files))
            self.loadNextGIF()  # first load is manual
            self.swapbuf()
            self.load_thread = loadnextthread(self)
            self.load_thread.start()
            self.load_thread.loadNext()  # pre-load next image
        else:
            self.loadGIFFile(imagePath)
            self.swapbuf()

        self._curImage = 0

    def _exit(self, type, value, traceback):
        if self.load_thread:
            self.load_thread.stop()

    def loadGIFFile(self, gif):
        _, ext = os.path.splitext(gif)
        next_buf = self.next_img_buf()
        if ext.lower().endswith("gif"):
            log.logger.info("Loading {0} ...".format(gif))
            self._image_buffers[next_buf] = _loadGIFSequence(gif, self._led, self._bgcolor, self._bright, self._offset)
        else:
            raise ValueError('Must be a GIF file!')

    def loadNextGIF(self):
        if self.random:
            if len(self.gif_indices) < 2:
                self.folder_index = self.gif_indices[0]
                self.gif_indices = range(len(self.gif_files))
            else:
                self.folder_index = self.gif_indices.pop(rand.randrange(0, len(self.gif_indices)))
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

    def preRun(self):
        self._curImage = 0

    def step(self, amt=1):
        self._led.all_off()
        img = self._image_buffers[self._cur_img_buf]

        self._led.setBuffer(img[self._curImage][1])
        if self.use_file_fps:
            self._internalDelay = img[self._curImage][0]

        self._curImage += 1
        if self._curImage >= len(img):
            self._curImage = 0
            if self.folder_mode:
                if self.cycle_count < self.cycles - 1:
                    self.cycle_count += 1
                elif not self.load_thread.loading():  # wait another cycle if still loading
                    self.animComplete = True
                    self.load_thread.loadNext()
                    self.swapbuf()
                    self.cycle_count = 0
            else:
                self.animComplete = True

        self._step = 0


MANIFEST = [
    {
        "class": ImageAnim,
        "controller": "matrix",
        "desc": "Display animated GIFs",
        "display": "ImageAnim",
        "id": "ImageAnim",
        "params": [
            {
                "default": None,
                "help": "Path to either a single GIF or folder of GIF files",
                "id": "imagePath",
                "label": "GIF/Folder Path",
                "type": "str"
            },
            {
                "default": [
                    0,
                    0,
                    0
                ],
                "help": "",
                "id": "bgcolor",
                "label": "Background",
                "type": "color"
            },
            {
                "default": 255,
                "help": "",
                "id": "brightness",
                "label": "Brightness",
                "type": "int"
            },
            {
                "default": [0, 0],
                "help": "Image placement offset",
                "id": "offset",
                "label": "Offset",
                "type": "multi_tuple",
                "controls": [{
                    "label": "X",
                    "type": "int",
                    "default": 0
                }, {
                    "label": "Y",
                    "type": "int",
                    "default": 0
                }]
            },
            {
                "default": 1,
                "help": "# of cycles to run before next GIF. Folder mode only.",
                "id": "cycles",
                "label": "# Cycles",
                "type": "int"
            },
            {
                "default": True,
                "help": "Random GIF selection. Folder mode only.",
                "id": "random",
                "label": "Random",
                "type": "bool"
            },
            {
                "default": True,
                "help": "Use framerate stored in GIF",
                "id": "use_file_fps",
                "label": "Use File FPS",
                "type": "bool"
            }
        ],
        "type": "animation"
    }
]
