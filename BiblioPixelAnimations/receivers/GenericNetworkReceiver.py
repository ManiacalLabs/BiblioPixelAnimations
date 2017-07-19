from bibliopixel.receiver_anim import BaseReceiver
import bibliopixel.drivers.network_receiver as net
from bibliopixel import LEDMatrix, LEDStrip


class GenericNetworkReceiver(BaseReceiver):
    def __init__(self, layout, port=3142, interface='0.0.0.0', raw=False, width=None, height=None):
        super(GenericNetworkReceiver, self).__init__(layout)
        self.raw = raw
        self.address = (interface, port)
        net.SocketServer.TCPServer.allow_reuse_address = True
        self._server = net.ThreadedDataServer(self.address, net.ThreadedDataHandler)
        self._server.update = self.recv
        self._server.setBrightness = self.layout.setMasterBrightness
        self._recv_thread_obj = self._server.serve_forever

    def thread_cleanup(self):
        self._server.shutdown()
        self._server.server_close()

    def recv(self, data):
        data = list(data)
        if self.raw:
            self.layout.setBuffer(data)
        else:
            if isinstance(self.layout, LEDMatrix):
                for y in range(self.layout.height):
                    for x in range(self.layout.width):
                        pixel = x + y * self.layout.width
                        self.layout.setRGB(x, y, data[pixel * 3 + 0], data[pixel * 3 + 1], data[pixel * 3 + 2])
            elif isinstance(self.layout, LEDStrip):
                for i in range(self.layout.numLEDs):
                    self.layout.setRGB(i, data[pixel * 3 + 0], data[pixel * 3 + 1], data[pixel * 3 + 2])

        self._hold_for_data.set()
