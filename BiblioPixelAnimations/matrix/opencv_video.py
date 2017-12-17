# OpenCVVideo
# Author - Adam Haile - Maniacal Labs
# License: MIT

# Requires numpy 1.9.x or greated and opencv-python 3.0.0 or greater
# On Windows, see here for install instructions: http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html
# For the Raspberry Pi, see here:
# http://www.pyimagesearch.com/2015/07/27/installing-opencv-3-0-for-both-python-2-7-and-python-3-on-your-raspberry-pi-2/

# OpenCVVideo displays video from either a webcam or video file
# to an LEDMatrix instance. Parameters are as follows:
# videoSource: Leave as default to use the default system webcam, otherwise set to a video file* path.
# mirror: Mirror image over the vertical axis. Mainly for use with webcams.
# offset: -1.0 to 1.0, when image is cropped or padded to fix on the display, setting this will shift the image.
#     -1.0 means shift to far left or top, 1.0 means far right or bottom.
# crop: Fill the display be cropping the image to best fit.
# userVidFPS: If true, the fps param can be left off anim.run() and it will use the FPS value of the provided video.
# Does nothing with webcams. This is always overriden by the run() fps or
# sleep parameters.

# *Video file codec support is system dependent, but in general very poor.
# it is best to conver any videos first, including decreasing their size.
# Pre-converting to a smaller resolution will decrease required CPU usage.
# The following ffmpeg command line with convert most videos to the required format:
# ffmpeg -i <inputfile> -c:v rawvideo -vf scale=<width>:<height> -r "<framerate>" -an <output>.avi
# You must set <inputfile>, <output>, <width>, <height>, <framerate>

# Load driver for your hardware, visualizer just for example
from bibliopixel.animation import BaseMatrixAnim
import cv2


class OpenCVVideo(BaseMatrixAnim):

    def __init__(self, layout, videoSource=None, mirror=True, offset=0.0, crop=True, useVidFPS=False):
        super(OpenCVVideo, self).__init__(layout)

        self.crop = crop
        self.mirror = mirror

        self.videoSource = videoSource

        if self.videoSource is None:
            self.videoSource = 0

        self._vid = cv2.VideoCapture(self.videoSource)
        # cv2 param defs here:
        # https://github.com/Itseez/opencv/blob/master/modules/videoio/include/opencv2/videoio/videoio_c.h

        self._frameCount = 0
        self._vidfps = 0
        ret, i = self._vid.read()

        if not isinstance(self.videoSource, int):
            try:
                self._vid.set(1, 0)  # CV_CAP_PROP_POS_FRAMES
                self._vidfps = int(self._vid.get(5))  # CV_CAP_PROP_FPS
                if useVidFPS:
                    self.internal_delay = (1000 / (self._vidfps * 1000))
                # CV_CAP_PROP_FRAME_COUNT
                self._frameTotal = int(self._vid.get(7))
            except Exception as e:
                pass

        if i is None:
            raise IOError("Error loading video source")

        self._iw = i.shape[1]
        self._ih = i.shape[0]

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

    def _exit(self, type, value, traceback):
        # self._vid.release()
        pass

    def step(self, amt=1):
        ret, frame = self._vid.read()

        image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGRA)

        if self.crop:
            image = image[self._cropY + self.yoff:self._ih - self._cropY +
                          self.yoff, self._cropX + self.xoff:self._iw - self._cropX + self.xoff]
        else:
            t, b, l, r = self._pad
            image = cv2.copyMakeBorder(
                image, t, b, l, r, cv2.BORDER_CONSTANT, value=[0, 0, 0])

        resized = cv2.resize(image, (self.width, self.height),
                             interpolation=cv2.INTER_CUBIC)
        if self.mirror:
            resized = cv2.flip(resized, 1)

        for y in range(self.height):
            for x in range(self.width):
                self.layout.set(x, y, tuple(resized[y, x][0:3]))

        if not isinstance(self.videoSource, int):
            self._frameCount += 1
            if self._frameCount >= self._frameTotal:
                self._vid.set(1, 0)  # CV_CAP_PROP_POS_FRAMES
                self._frameCount = 0
                self.animComplete = True
