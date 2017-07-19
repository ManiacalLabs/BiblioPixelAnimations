from bibliopixel.animation import BaseMatrixAnim
from websocket import create_connection
import threading
import numpy as np

WS_FRAME_WIDTH = 640
WS_FRAME_HEIGHT = 480
WS_FRAME_SIZE = WS_FRAME_WIDTH * WS_FRAME_HEIGHT


def clamp(v, _min, _max):
    return max(min(v, _max), _min)


def lerp(n, low, high):
    return clamp((n - low) / (high - low), 0.0, 1.0)


def rebin(a, shape):
    sh = shape[0], a.shape[0] // shape[0], shape[1], a.shape[1] // shape[1]
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


class KimotionShader(object):
    def __init__(self, anim):
        self.anim = anim
        self.width = self.anim.width
        self.height = self.anim.height
        self.led = self.anim._led


class SandStorm(KimotionShader):
    def __init__(self, anim, min_z=440, max_z=1100,
                 near_color=[229, 107, 0], near_z=760,
                 mid_color=[40, 0, 114],
                 far_color=[2, 2, 12], far_z=1100):

        super(SandStorm, self).__init__(anim)

        self.min_z = float(min_z)
        self.max_z = float(max_z)
        self.near_color = np.array(near_color)
        self.near_z = float(near_z)
        self.mid_color = np.array(mid_color)
        self.mid_z = ((self.max_z + self.near_z) / 2.0)
        self.far_color = np.array(far_color)
        self.far_z = float(far_z)

        self.z_colors = np.array([self.z_color(z) for z in range(0, int(Kimotion.max_depth) + 1)]).tolist()

    def z_color(self, z):
        z = float(z)
        alpha = 1.0

        if z <= self.mid_z:
            ns = lerp(z, self.near_z, self.mid_z)
            color = (1.0 - ns) * self.near_color + ns * self.mid_color
        else:  # z must be between self.mid_z and FAR_Z
            fs = lerp(z, self.mid_z, self.far_z)
            color = (1.0 - fs) * self.mid_color + fs * self.far_color

        alpha = 1.0 - lerp(z, self.min_z, self.max_z)

        if z <= -self.min_z:
            alpha = 0.0

        # gl_FragColor = vec4(color, alpha) * texture2D( texture, gl_PointCoord )

        return (color * alpha).astype(np.uint8).tolist()

    def render(self, frame):
        for y in range(self.height):
            for x in range(self.width):
                c = self.z_colors[frame[y][x]]
                self.led.set(x, y, c)


class Kimotion(BaseMatrixAnim):
    max_depth = 1200.0
    shaders = {
        "Sandstorm": SandStorm
    }

    def __init__(self, layout, server="localhost:1337", mirror=True, crop=True, shader="Sandstorm", **kwargs):
        super(Kimotion, self).__init__(layout)
        self.server = server
        self.mirror = mirror
        self.crop = crop

        self.fw = WS_FRAME_WIDTH
        self.fh = WS_FRAME_HEIGHT

        # TODO: Implement something to actually use this
        # Right now needs 4:3 aspect display
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

        self.shader = Kimotion.shaders[shader](self, **kwargs)

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

        self.shader.render(d)
