import numpy
import struct
import pyaudio
import threading
import struct
from collections import deque

from bibliopixel import LEDMatrix
from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors


class Recorder:
    """Simple, cross-platform class to record from the microphone."""

    def __init__(self):
        """minimal garb is executed when class is loaded."""
        self.RATE=48100
        self.BUFFERSIZE=2**12 #4069 is a good buffer size
        self.secToRecord=.1
        self.threadsDieNow=False
        self.newAudio=False
        self.maxVals = deque(maxlen=500)

    def setup(self):
        """initialize sound card."""
        #TODO - windows detection vs. alsa or something for linux
        #TODO - try/except for sound card selection/initiation

        self.buffersToRecord=int(self.RATE*self.secToRecord/self.BUFFERSIZE)
        if self.buffersToRecord==0: self.buffersToRecord=1
        self.samplesToRecord=int(self.BUFFERSIZE*self.buffersToRecord)
        self.chunksToRecord=int(self.samplesToRecord/self.BUFFERSIZE)
        self.secPerPoint=1.0/self.RATE

        self.p = pyaudio.PyAudio()
        self.inStream = self.p.open(format=pyaudio.paInt16,channels=1,rate=self.RATE,input=True, output=False,frames_per_buffer=self.BUFFERSIZE)

        self.xsBuffer=numpy.arange(self.BUFFERSIZE)*self.secPerPoint
        self.xs=numpy.arange(self.chunksToRecord*self.BUFFERSIZE)*self.secPerPoint
        self.audio=numpy.empty((self.chunksToRecord*self.BUFFERSIZE),dtype=numpy.int16)

    def close(self):
        """cleanly back out and release sound card."""
        self.p.close(self.inStream)

    ### RECORDING AUDIO ###

    def getAudio(self):
        """get a single buffer size worth of audio."""
        audioString=self.inStream.read(self.BUFFERSIZE)
        return numpy.fromstring(audioString,dtype=numpy.int16)

    def record(self,forever=True):
        """record secToRecord seconds of audio."""
        while True:
            if self.threadsDieNow: break
            for i in range(self.chunksToRecord):
                self.audio[i*self.BUFFERSIZE:(i+1)*self.BUFFERSIZE]=self.getAudio()
            self.newAudio=True
            if forever==False: break

    def continuousStart(self):
        """CALL THIS to start running forever."""
        self.t = threading.Thread(target=self.record)
        self.t.start()

    def continuousEnd(self):
        """shut down continuous recording."""
        self.threadsDieNow=True

    ### MATH ###

    def fft(self,xMax, yMax):
        data=self.audio.flatten()

        left,right=numpy.split(numpy.abs(numpy.fft.fft(data)),2)
        ys=numpy.add(left,right[::-1])

        #FFT max values can vary widely depending on the hardware/audio setup.
        #Take the average of the last few values which will keep everything
        #in a "normal" range (visually speaking). Also makes it volume independent.
        self.maxVals.append(numpy.amax(ys))

        ys = ys[:xMax]
        m = max(100000, numpy.average(self.maxVals))
        ys = numpy.rint(numpy.interp(ys,[0,m],[0,yMax-1]))
        return ys

class EQ(BaseMatrixAnim):

    def __init__(self, led):
        super(EQ, self).__init__(led)
        self.rec = Recorder()
        self.rec.setup()
        self.rec.continuousStart()
        self.colors = [colors.hue_helper(y, self.height, 0) for y in range(self.height)]

    def endRecord(self):
        self.rec.continuousEnd()

    def step(self, amt = 1):
        self._led.all_off()
        eq_data = self.rec.fft(self.width, self.height + 1)
        for x in range(self.width):
            for y in range(self.height):
                if y < int(eq_data[x]):
                    self._led.set(x, self.height - y - 1, self.colors[y])
        # x = 0
        # for y in eq_data:
        #     self._led.drawLine(x, self._led.height - 1, x, self._led.height - int(y), colors.hue_helper(int(y), self._led.height, 0))
        #     x += 1
        self._step = amt

#Load driver for your hardware, visualizer just for example
# from bibliopixel.drivers.visualizer import DriverVisualizer
# driver = DriverVisualizer(width = 24, height = 24, stayTop = True)

# from bibliopixel.drivers.serial_driver import *
# import bibliopixel.gamma as gamma
# num = 24*24
# print "Pixel Count: {}".format(num)
# driver = DriverSerial(LEDTYPE.LPD8806, num, c_order=ChannelOrder.BRG, SPISpeed=2, gamma = gamma.LPD8806)
#
# #load the LEDMatrix class
# from bibliopixel.led import *
# #change rotation and vert_flip as needed by your display
# led = LEDMatrix(driver, rotation = MatrixRotation.ROTATE_0, vert_flip = True)
# led.setMasterBrightness(128)
# import bibliopixel.log as log
# #log.setLogLevel(log.DEBUG)
#
# try:
#     anim = EQ(led)
#     anim.run(fps=30)
# except KeyboardInterrupt:
#     anim.endRecord()
#     led.all_off()
#     led.update()



MANIFEST = [
    {
        "class": EQ,
        "controller": "matrix",
        "desc": "Reads system audio output and displays VU meter.", 
        "display": "EQ",
        "id": "EQ",
        "params": [],
        "type": "animation"
    }
]
