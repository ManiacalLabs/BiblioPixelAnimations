from bibliopixel.receiver_anim import BaseReceiver
import bibliopixel.drivers.network_receiver as net
from bibliopixel import log
from bibliopixel import LEDMatrix, LEDStrip


class GenericNetworkReceiver(BaseReceiver):
    def __init__(self, led, port=3142, interface='0.0.0.0', raw=False, width=None, height=None):
        super(GenericNetworkReceiver, self).__init__(led)
        self.raw = raw
        self.address = (interface, port)
        net.SocketServer.TCPServer.allow_reuse_address = True
        self._server = net.ThreadedDataServer(self.address, net.ThreadedDataHandler)
        self._server.update = self.recv
        self._server.setBrightness = self._led.setMasterBrightness
        self._recv_thread_obj = self._server.serve_forever

    def thread_cleanup(self):
        self._server.shutdown()
        self._server.server_close()

    def recv(self, data):
        data = list(data)
        if self.raw:
            self._led.setBuffer(data)
        else:
            if isinstance(self._led, LEDMatrix):
                for y in xrange(self._led.height):
                    for x in xrange(self._led.width):
                        pixel = x + y * self._led.width
                        self._led.setRGB(x, y, data[pixel * 3 + 0], data[pixel * 3 + 1], data[pixel * 3 + 2])
            elif isinstance(self._led, LEDStrip):
                for i in xrange(self._led.numLEDs):
                    self._led.setRGB(i, data[pixel * 3 + 0], data[pixel * 3 + 1], data[pixel * 3 + 2])

        self._hold_for_data.set()
