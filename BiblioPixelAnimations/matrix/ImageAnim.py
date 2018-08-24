from bibliopixel.animation import BaseMatrixAnim
from bibliopixel import log

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
import time


def _getBufferFromImage(img, layout, bgcolor, bright, offset):
    duration = None
    if 'duration' in img.info:
        duration = img.info['duration']

    w = layout.width - offset[0]
    if img.size[0] < w:
        w = img.size[0]

    h = layout.height - offset[1]
    if img.size[1] < h:
        h = img.size[1]

    ox = offset[0]
    oy = offset[1]

    buffer = [0 for x in range(layout.numLEDs * 3)]
    gamma = layout.drivers[0].gamma
    if bgcolor != (0, 0, 0):
        for i in range(layout.numLEDs):
            buffer[i * 3 + 0] = gamma.get(bgcolor[0])
            buffer[i * 3 + 1] = gamma.get(bgcolor[1])
            buffer[i * 3 + 2] = gamma.get(bgcolor[2])

    frame = Image.new("RGBA", img.size)
    frame.paste(img)

    for x in range(ox, w + ox):
        for y in range(oy, h + oy):
            if x < 0 or y < 0:
                continue
            pixel = layout.coord_map[y][x]
            r, g, b, a = frame.getpixel((x - ox, y - oy))
            if a == 0:
                r, g, b = bgcolor
            else:
                r = (r * a) >> 8
                g = (g * a) >> 8
                b = (b * a) >> 8
            if bright != 255:
                r, g, b = colors.color_scale((r, g, b), bright)

            buffer[pixel * 3 + 0] = gamma.get(r)
            buffer[pixel * 3 + 1] = gamma.get(g)
            buffer[pixel * 3 + 2] = gamma.get(b)

    return (duration, buffer)


def _loadGIFSequence(imagePath, layout, bgcolor, bright, offset):
    img = Image.open(imagePath)
    if offset == (0, 0):
        w = 0
        h = 0
        if img.size[0] < layout.width:
            w = (layout.width - img.size[0]) // 2
        if img.size[1] < layout.height:
            h = (layout.height - img.size[1]) // 2
        offset = (w, h)

    images = []
    count = 0
    for frame in ImageSequence.Iterator(img):
        images.append(_getBufferFromImage(frame, layout, bgcolor, bright, offset))
        count += 1

    return images


class loadnextthread(threading.Thread):

    def __init__(self, imganim):
        super(loadnextthread, self).__init__()
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


class ImageAnim(BaseMatrixAnim):
    def __init__(self, layout, imagePath=None, offset=(0, 0), bgcolor=colors.Off,
                 brightness=255, cycles=1, seconds=None, random=False, use_file_fps=True):
        """Helper class for displaying image animations for GIF files or a set of bitmaps

        layout - layoutMatrix instance
        imagePath - Path to either a single animated GIF image or folder of GIF files
        offset - X,Y tuple coordinates at which to place the top-left corner of the image
        bgcolor - RGB tuple color to replace any transparent pixels with. Avoids transparent showing as black
        brightness - Brightness value (0-255) to scale the image by. Otherwise uses master brightness at the time of creation
        """
        super(ImageAnim, self).__init__(layout)

        self.cycles = cycles
        self.cycle_count = 0

        self.seconds = seconds
        self.last_start = 0

        self.random = random
        self.use_file_fps = use_file_fps

        self._bright = brightness

        self._bgcolor = colors.color_scale(bgcolor, self._bright)
        self._offset = offset
        self._image_buffers = [None, None]
        self._cur_img_buf = 1  # start here because loadNext swaps it

        if imagePath is None:
            cur_dir = os.path.dirname(os.path.realpath(__file__))
            imagePath = os.path.abspath(os.path.join(cur_dir, '../../Graphics/MarioRotating.gif'))

        self.imagePath = imagePath
        self.folder_mode = os.path.isdir(imagePath)
        self.gif_files = []
        self.gif_indices = []
        self.folder_index = -1
        self.load_thread = None

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
                self.load_thread = loadnextthread(self)
                self.load_thread.start()

            self.load_thread.loadNext()
            self.last_start = time.time()

        self._curImage = 0

    def loadGIFFile(self, gif):
        _, ext = os.path.splitext(gif)
        next_buf = self.next_img_buf()
        if ext.lower().endswith("gif"):
            log.logger.debug("Loading {0} ...".format(gif))
            self._image_buffers[next_buf] = _loadGIFSequence(gif, self.layout, self._bgcolor, self._bright, self._offset)
        else:
            raise ValueError('Must be a GIF file!')

    def loadNextGIF(self):
        if self.random:
            if len(self.gif_indices) < 2:
                self.folder_index = self.gif_indices[0]
                self.gif_indices = list(range(len(self.gif_files)))
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

                if loadnext and not self.load_thread.loading():  # wait another cycle if still loading
                    self.animComplete = True
                    self.load_thread.loadNext()
                    self.swapbuf()
                    self.cycle_count = 0
                    self.last_start = time.time()
            else:
                self.animComplete = True

        self._step = 0
