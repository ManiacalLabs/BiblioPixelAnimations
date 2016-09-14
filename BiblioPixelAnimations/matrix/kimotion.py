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

def clamp(v, _min, _max):
    return max(min(v, _max), _min)


def lerp(n, low, high):
    return clamp((n - low) / (high - low), 0.0, 1.0)


MIN_Z = 440.0
MAX_Z = 1100.0

NEAR_Z = 760.0
MID_Z = ((MAX_Z + NEAR_Z) / 2.0)
FAR_Z = MAX_Z

# MIN_Z = 0.0
# MAX_Z = 65000.0
#
# NEAR_Z = 2000.0
# MID_Z = ((MAX_Z + NEAR_Z) / 2.0)
# FAR_Z = 60000.0

near_color = np.array([255, 0, 0])  # np.array(colors.hex2rgb('#e56b00'))
mid_color = np.array([0, 0, 255])  # np.array(colors.hex2rgb('#280072'))
far_color = np.array([0, 255, 0])  # np.array(colors.hex2rgb('#02020c'))

near_color = np.array(colors.hex2rgb('#e56b00'))
mid_color = np.array(colors.hex2rgb('#280072'))
far_color = np.array(colors.hex2rgb('#02020c'))
# far_color = np.array([0, 0, 255])

def z_color(z):
    z = float(z)
    alpha = 1.0

    if z <= MID_Z:
        ns = lerp(z, NEAR_Z, MID_Z)
        color = (1.0 - ns) * near_color + ns * mid_color
    else:  # z must be between MID_Z and FAR_Z
        fs = lerp(z, MID_Z, FAR_Z)
        color = (1.0 - fs) * mid_color + fs * far_color

    alpha = 1.0 - lerp(z, MIN_Z, MAX_Z)

    if z <= -MIN_Z:
        alpha = 0.0

    # gl_FragColor = vec4(color, alpha) * texture2D( texture, gl_PointCoord )

    return (color * alpha).astype(np.uint8).tolist()


def rebin(a, shape):
    sh = shape[0],a.shape[0]//shape[0],shape[1],a.shape[1]//shape[1]
    return a.reshape(sh).mean(-1).mean(1)


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
        self.dt = self.dt.newbyteorder('<')
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
        self.max_depth = 1200
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

        self.z_colors = np.array([z_color(z) for z in range(0, self.max_depth + 1)]).tolist()
        self._ws_thread = ws_thread(self.server)
        self._ws_thread.start()

    def _exit(self, type, value, traceback):
        self._ws_thread.stop()

    def step(self, amt=1):
        d = self._ws_thread.get_frame()
        d = d.reshape(WS_FRAME_HEIGHT, WS_FRAME_WIDTH)
        if self.mirror:
            d = np.fliplr(d)

        d = rebin(d, (self.height, self.width)).astype(np.uint16)
        for y in range(self.height):
            for x in range(self.width):
                c = self.z_colors[d[y][x]]
                self._led.set(x, y, c)


MANIFEST = [
    {
        "class": Kimotion,
        "controller": "matrix",
        "desc": "Pull Kinect data from Michael Clayton's Kimotion server",
        "display": "Kimotion",
        "id": "Kimotion",
        "params": [
            {
                "default": "localhost:1337",
                "help": "Kimotion server address (minus the ws://)",
                "id": "server",
                "label": "Server",
                "type": "str"
            },
            {
                "default": True,
                "help": "Crop input video to display size.",
                "id": "crop",
                "label": "Crop",
                "type": "bool"
            },
            {
                "default": False,
                "help": "Mirrors image along vertical. Useful for webcam video.",
                "id": "mirror",
                "label": "Mirror",
                "type": "bool"
            }
        ],
        "type": "animation"
    }
]
