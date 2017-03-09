from bibliopixel.animation import BaseMatrixAnim
from bibliopixel import log
import numpy as np
import cv2
import os

grab = None

if os.name == 'nt':
    try:
        from desktopmagic.screengrab_win32 import getRectAsImage, getScreenAsImage
        log.debug("Using desktopmagic module")

        def nt_grab(bbox=None):
            if bbox is None:
                img = getScreenAsImage()
            else:
                img = getRectAsImage(bbox)
            return img

        grab = nt_grab
    except:
        pass

if grab is None:
    try:
        from mss.linux import MSS as mss
        from PIL import Image
        log.info('Using mss module')

        sct = mss()
        monitor = sct.enum_display_monitors()[0]

        def mss_grab(bbox):
            sct.get_pixels(monitor)
            img = Image.frombytes('RGB',
                                  (sct.width, sct.height),
                                  sct.image).crop(bbox)
            return img

        grab = mss_grab
    except:
        try:
            from pil import ImageGrab
            log.info("Using PIL ImageGrab module")
        except:
            try:
                import pyscreenshot as ImageGrab
                log.info("Using pyscreenshot module")
            except:
                raise Exception("Unable to find any available screenshot option.")

        grab = ImageGrab.grab


class ScreenGrab(BaseMatrixAnim):

    def __init__(self, led, bbox=None, mirror=True, offset=0.0, crop=True):
        super(ScreenGrab, self).__init__(led)

        if not sum(bbox):
            bbox = None
        self.bbox = bbox
        self.crop = crop
        self.mirror = mirror

        self.image = frame = self._capFrame()

        self._iw = frame.shape[1]
        self._ih = frame.shape[0]

        self.width = led.width
        self.height = led.height

        # self._scale = (self.height*1.0/self._ih)
        self._cropY = 0
        self._cropX = 0

        xoffset = yoffset = offset
        if xoffset > 1.0:
            xoffset = 1.0
        elif xoffset < -1.0:
            xoffset = -1.0
        if yoffset > 1.0:
            yoffset = 1.0
        elif yoffset < -1.0:
            yoffset = -1.0
        xoffset += 1.0
        yoffset += 1.0

        if self.height >= self.width:
            self._cropX = (self._iw - int(self.width /
                                          (self.height / float(self._ih)))) / 2
            if self._ih >= self._iw:
                scale = (self.height * 1.0) / self._ih
            else:
                scale = (self.width * 1.0) / self._iw
        else:
            self._cropY = (self._ih - int(self.height /
                                          (self.width / float(self._iw)))) / 2
            if self._ih >= self._iw:
                scale = (self.width * 1.0) / self._iw
            else:
                scale = (self.height * 1.0) / self._ih

        scaleW = int(self.width / scale)
        scaleH = int(self.height / scale)

        padTB = (scaleH - self._ih) / 2
        padLR = (scaleW - self._iw) / 2

        padYoff = int(round(padTB * yoffset)) - padTB
        padXoff = int(round(padLR * xoffset)) - padLR

        self._pad = (padTB + padYoff, padTB - padYoff,
                     padLR + padXoff, padLR - padXoff)

        self.xoff = int(round(self._cropX * xoffset)) - self._cropX
        self.yoff = int(round(self._cropY * yoffset)) - self._cropY

    def _capFrame(self):
        img = grab(self.bbox)
        return np.array(img)

    def step(self, amt=1):
        image = self._capFrame()

        if self.crop:
            image = image[self._cropY + self.yoff:self._ih - self._cropY +
                          self.yoff, self._cropX + self.xoff:self._iw - self._cropX + self.xoff]
        else:
            t, b, l, r = self._pad
            image = cv2.copyMakeBorder(
                image, t, b, l, r, cv2.BORDER_CONSTANT, value=[0, 0, 0])

        resized = cv2.resize(image, (self.width, self.height),
                             interpolation=cv2.INTER_LINEAR)
        if self.mirror:
            resized = cv2.flip(resized, 1)

        for y in range(self.height):
            for x in range(self.width):
                self._led.set(x, y, tuple(resized[y, x][0:3]))


MANIFEST = [
    {
        "class": ScreenGrab,
        "controller": "matrix",
        "desc": None,
        "display": "ScreenGrab",
        "id": "ScreenGrab",
        "params": [
            {
                "default": (0, 0, 0, 0),
                "help": "Bounding box of screen area to capture. Leave all 0 to capture whole screen.",
                "id": "bbox",
                "label": "Bounding Box",
                "type": "multi_tuple",
                "controls": [{
                    "label": "Top-Left X",
                    "type": "int",
                    "default": 0
                }, {
                    "label": "Top-Left Y",
                    "type": "int",
                    "default": 0
                }, {
                    "label": "Bottom-Left X",
                    "type": "int",
                    "default": 0
                }, {
                    "label": "Bottom-Left Y",
                    "type": "int",
                    "default": 0
                }]
            },
            {
                "default": False,
                "help": "True crops image to matrix aspect. False resizes input to fit.",
                "id": "crop",
                "label": "Crop",
                "type": "bool"
            },
            {
                "default": False,
                "help": "Mirror output",
                "id": "mirror",
                "label": "Mirror",
                "type": "bool"
            }
        ],
        "type": "animation"
    }
]
