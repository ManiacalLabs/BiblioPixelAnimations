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

from bibliopixel.animation import BaseMatrixAnim, AnimationQueue
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

    buffer = [0 for x in range(led.bufByteCount)]
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


class ImageAnim(BaseMatrixAnim):
    def __init__(self, led, imagePath, offset=(0, 0), bgcolor=colors.Off, brightness=255):
        """Helper class for displaying image animations for GIF files or a set of bitmaps

        led - LEDMatrix instance
        imagePath - Path to either a single animated GIF image or folder of sequential bitmap files
        offset - X,Y tuple coordinates at which to place the top-left corner of the image
        bgcolor - RGB tuple color to replace any transparent pixels with. Avoids transparent showing as black
        brightness - Brightness value (0-255) to scale the image by. Otherwise uses master brightness at the time of creation
        """
        super(ImageAnim, self).__init__(led)

        self._bright = brightness
        if self._bright == 255 and led.masterBrightness != 255:
            self._bright = led.masterBrightness

        self._bgcolor = colors.color_scale(bgcolor, self._bright)
        self._offset = offset
        self._images = []

        self.folder_mode = os.path.isdir(imagePath)
        self.gif_files = []
        self.folder_index = -1

        if self.folder_mode:
            self.gif_files = glob.glob(imagePath + "/*.gif")
            self.loadNextGIF()
        else:
            self.loadGIFFile(imagePath)

        self._curImage = 0

    def loadGIFFile(self, gif):
        _, ext = os.path.splitext(gif)

        if ext.lower().endswith("gif"):
            log.logger.info("Loading {0} ...".format(gif))
            self._images = _loadGIFSequence(gif, self._led, self._bgcolor, self._bright, self._offset)
        else:
            raise ValueError('Must be a GIF file!')

    def loadNextGIF(self):
        self.folder_index += 1
        if self.folder_index >= len(self.gif_files):
            self.folder_index = 0
        self.loadGIFFile(self.gif_files[self.folder_index])

    def preRun(self):
        self._curImage = 0

    def step(self, amt=1):
        self._led.all_off()

        self._led.setBuffer(self._images[self._curImage][1])
        self._internalDelay = self._images[self._curImage][0]

        self._curImage += 1
        if self._curImage >= len(self._images):
            self._curImage = 0
            self.animComplete = True
            self.loadNextGIF()

        self._step = 0


class ImageAnimFolder(AnimationQueue):

    def __init__(self, led, folder, cycles=1):
        super(ImageAnimFolder, self).__init__(led)
        self.folder = folder
        self.gifs = []
        for g in glob.glob(self.folder + "/*.gif"):
            anim = ImageAnim(led, g)
            self.gifs.append(anim)
            self.addAnim(anim, untilComplete=True, max_cycles=cycles)


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
                "help": "",
                "id": "imagePath",
                "label": "GIF Path",
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
            }
        ],
        "type": "animation"
    },
    {
        "class": ImageAnimFolder,
        "controller": "matrix",
        "desc": "Display folder of animated GIFs",
        "display": "ImageAnimFolder",
        "id": "ImageAnimFolder",
        "params": [
            {
                "default": None,
                "help": "",
                "id": "folder",
                "label": "GIF Folder Path",
                "type": "str"
            },
            {
                "default": 1,
                "help": "# of times to cycle each GIF",
                "id": "cycles",
                "label": "# Cycles",
                "type": "int"
            }
        ],
        "type": "animation"
    }
]
