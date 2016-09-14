from bibliopixel.animation import BaseMatrixAnim
from bibliopixel import colors
from websocket import create_connection
import threading
import numpy as np
import PIL
from PIL import Image
import cv2

WS_FRAME_WIDTH = 640
WS_FRAME_HEIGHT = 480
WS_FRAME_SIZE = WS_FRAME_WIDTH * WS_FRAME_HEIGHT


def thread_lock():
    e = threading.Event()
    e.lock = e.clear
    e.release = e.set
    e.is_released = e.is_set

    e.release()
    return e


class ws_thread(threading.Thread):

    def __init__(self, server):
        super(ws_thread, self).__init__()
        self.setDaemon(True)
        self._stop = threading.Event()
        self._reading = thread_lock()
        self.dt = np.dtype(np.uint16)
        self.dt = self.dt.newbyteorder('>')
        self._data = [np.zeros(WS_FRAME_SIZE, self.dt),
                      np.zeros(WS_FRAME_SIZE, self.dt)]
        self._buf = False
        self.ws = create_connection("ws://{}/".format(server))

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def get_frame(self):
        self._reading.lock()
        d = np.copy(self._data[0 if self._buf else 1])
        self._reading.release()
        return d

    def run(self):
        while not self.stopped():
            d = self.ws.recv()
            d = np.frombuffer(d, dtype=self.dt)
            self._reading.wait()
            self._data[1 if self._buf else 0] = d
            self._buf = not self._buf
        self.ws.close()


class Kimotion(BaseMatrixAnim):

    def __init__(self, led, server="localhost:1337", mirror=True, crop=True):
        super(Kimotion, self).__init__(led)
        self.server = server
        self.mirror = mirror
        self.crop = crop
        self.min = np.iinfo(np.uint16).min
        self.max = np.iinfo(np.uint16).max

        self.fw = WS_FRAME_WIDTH
        self.fh = WS_FRAME_HEIGHT

        self.frame_aspect = (float(WS_FRAME_WIDTH) / float(WS_FRAME_HEIGHT))
        self.aspect = (float(self.width) / float(self.height))
        self.resize_box = (self.width, self.height)
        self.crop_box = (0, 0, self.width, self.height)
        if self.frame_aspect > self.aspect:
            self.resize_box[0] = int(self.height * self.frame_aspect)
            half = (self.resize_box[0] - self.width) / 2
            self.crop_box[0] = half
            self.crop_box[2] = self.resize_box[0] - half
        elif self.frame_aspect < self.aspect:
            self.resize_box[1] = int(self.width / self.aspect)
            half = (self.resize_box[1] - self.height) / 2
            self.crop_box[1] = half
            self.crop_box[3] = self.resize_box[1] - half

        self.gradient = [colors.hue2rgb(h) for h in colors.hue_gradient(255, 0, 256)]
        self._ws_thread = ws_thread(self.server)
        self._ws_thread.start()

    def _exit(self, type, value, traceback):
        self._ws_thread.stop()

    def step(self, amt=1):
        d = self._ws_thread.get_frame()
        d = np.round(255.0 * (d - self.min) /
                     (self.max - self.min - 1.0)).astype(np.uint8)
        d = d.reshape(WS_FRAME_HEIGHT, WS_FRAME_WIDTH)

        if self.mirror:
            d = np.fliplr(d)
        img = Image.fromarray(d)
        img = img.resize(self.resize_box, Image.BILINEAR)
        if self.crop:
            img = img.crop(self.crop_box)
            img.load()

        for y in range(self.height):
            for x in range(self.width):
                p = img.getpixel((x, y))
                if p == 0:
                    c = colors.Black
                else:
                    c = self.gradient[p]
                self._led.set(x, y, c)
