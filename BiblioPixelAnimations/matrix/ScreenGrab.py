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
    except Exception as e:
        pass

if grab is None:
    try:
        from mss.linux import MSS as mss
        from PIL import Image

        sct = mss()
        monitor = sct.monitors[0]

        def mss_grab(bbox):
            sct_img = sct.grab(monitor)
            img = Image.frombytes('RGBA', sct_img.size, bytes(sct_img.raw), 'raw', 'BGRA').crop(bbox)
            img = img.convert('RGB')

            return img

        grab = mss_grab
        log.debug('Using mss module')
    except Exception as e:
        try:
            from PIL import ImageGrab
            log.debug("Using PIL ImageGrab module")
        except Exception as e:
            try:
                import pyscreenshot as ImageGrab
                log.debug("Using pyscreenshot module")
            except Exception as e:
                raise Exception("Unable to find any available screenshot option.")

        grab = ImageGrab.grab


class ScreenGrab(BaseMatrixAnim):

    def __init__(self, layout, bbox=(300, 300, 332, 332), mirror=False, offset=0.0, crop=True):
        super(ScreenGrab, self).__init__(layout)

        if not sum(bbox):
            bbox = None
        self.bbox = bbox
        self.crop = crop
        self.mirror = mirror

        self.image = frame = self._capFrame()

        self._iw = frame.shape[1]
        self._ih = frame.shape[0]

        self.width = self.width
        self.height = self.height

        # self._scale = (self.height*1.0//self._ih)
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
            self._cropX = (self._iw - int(self.width / (self.height / float(self._ih)))) // 2
            if self._ih >= self._iw:
                scale = (self.height * 1.0) // self._ih
            else:
                scale = (self.width * 1.0) // self._iw
        else:
            self._cropY = (self._ih - int(self.height / (self.width / float(self._iw)))) // 2
            if self._ih >= self._iw:
                scale = (self.width * 1.0) // self._iw
            else:
                scale = (self.height * 1.0) // self._ih

        scaleW = int(self.width / scale)
        scaleH = int(self.height / scale)

        padTB = (scaleH - self._ih) // 2
        padLR = (scaleW - self._iw) // 2

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
                self.layout.set(x, y, tuple(resized[y, x][0:3]))
