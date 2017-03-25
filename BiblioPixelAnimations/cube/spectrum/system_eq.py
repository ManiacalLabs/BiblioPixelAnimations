import numpy as np
import pyaudio
import threading


class Recorder(object):
    def __init__(self, rate=8000, chunksize=128):
        self.rate = rate
        self.chunksize = chunksize
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.rate,
                                  input=True,
                                  frames_per_buffer=self.chunksize,
                                  stream_callback=self.new_frame)
        self.lock = threading.Lock()
        self.stop = False
        self.frames = []

    def new_frame(self, data, frame_count, time_info, status):
        data = np.fromstring(data, 'int16')
        with self.lock:
            self.frames.append(data)
            if self.stop:
                return None, pyaudio.paComplete
        return None, pyaudio.paContinue

    def get_frames(self):
        with self.lock:
            frames = self.frames
            self.frames = []
            return frames

    def start(self):
        self.stream.start_stream()

    def close(self):
        with self.lock:
            self.stop = True
        self.stream.close()
        self.p.terminate()


class EQ(object):

    def __init__(self, bins, max_freq=4000, log_scale=True, auto_gain=False, gain=3):
        self.max_freq = max_freq
        self.bins = bins
        self.log_scale = log_scale
        self.auto_gain = auto_gain
        self.gain = gain

        self.rec = Recorder(rate=self.max_freq * 2, chunksize=self.bins * 2)

        # computes the parameters that will be used during plotting
        self.freq_vect = np.fft.rfftfreq(self.rec.chunksize, 1. / self.rec.rate)
        self.time_vect = np.arange(self.rec.chunksize, dtype=np.float32) / self.rec.rate * 1000

    def start(self):
        self.rec.start()

    def stop(self):
        self.rec.close()

    def get_audio_data(self):
        frames = self.rec.get_frames()
        result = [0] * self.bins
        if len(frames) > 0:
            # keeps only the last frame
            current_frame = frames[-1]
            # plots the time signal
            # self.line_top.set_data(self.time_vect, current_frame)
            # computes and plots the fft signal
            fft_frame = np.fft.rfft(current_frame)
            if self.auto_gain:
                fft_frame /= np.abs(fft_frame).max()
            else:
                fft_frame *= (1 + self.gain) / 5000000.

            fft_frame = np.abs(fft_frame)
            if self.log_scale:
                fft_frame = np.log10(np.add(1, np.multiply(10, fft_frame)))

            result = [min(int(max(i, 0.) * 1023), 1023) for i in fft_frame][0:self.bins]

        return result
