from bibliopixel.receiver_anim import BaseReceiver
import bibliopixel.drivers.network_receiver as net
from bibliopixel import log


class GenericNetworkReceiver(BaseReceiver):
    def __init__(self, led, port=3142, interface='0.0.0.0'):
        super(GenericNetworkReceiver, self).__init__(led)
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
        self._led.setBuffer(list(data))
        self._hold_for_data.set()
