import logging
import numpy
import time
import math
import audioop
import random

log = logging.getLogger(__name__)
available = {}


class Input(object):
    pass


try:
    import alsaaudio

    class AlsaInput(Input):
        def __init__(self, rate=8000):
            self.rate = rate

            log.info("Opening ALSA input")
            # Open the device in nonblocking capture mode. The last argument could
            # just as well have been zero for blocking mode. Then we could have
            # left out the sleep call in the bottom of the loop
            #inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)
            inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, 0)

            # Set attributes: Mono, 8000 Hz, 16 bit little endian samples
            inp.setchannels(1)
            inp.setrate(rate)
            inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

            # The period size controls the internal number of frames per period.
            # The significance of this parameter is documented in the ALSA api.
            # For our purposes, it is suficcient to know that reads from the device
            # will return this many frames. Each frame being 2 bytes long.
            # This means that the reads below will return either 320 bytes of data
            # or 0 bytes of data. The latter is possible because we are in nonblocking
            # mode.
            inp.setperiodsize(160)

            self.inp = inp

        def read(self):
            data = self.inp.read()
            samples = [audioop.getsample(data, 2, n) for n in range(0, 160)]
            return samples

    available["alsa"] = AlsaInput
except ImportError:
    available["alsa"] = "Failed to import alsaaudio"


try:
    import jack

    class JackInput(Input):
        def __init__(self):
            log.info("Opening JACK input")
            jack.attach("Noter Virtual Keyboard")
            self.rate = jack.get_sample_rate()
            jack.activate()
            jack.register_port("Input 1", jack.IsInput)
            jack.register_port("Input 2", jack.IsInput)
            jack.connect("system:capture_1", "Noter Virtual Keyboard:Input 1")
            jack.connect("system:capture_2", "Noter Virtual Keyboard:Input 2")

            self.buffer_size = jack.get_buffer_size()
            self.input = numpy.zeros((2, self.buffer_size), 'f')
            self.output = numpy.zeros((2, self.buffer_size), 'f')

        def __del__(self):
            jack.detach()

        def read(self):
            jack.process(self.output, self.input)
            #i16s = self.input * 2**16
            i16s = [int(n * 2**16) for n in self.input[0]]
            return self.buffer_size, i16s

    available["jack"] = JackInput
except ImportError:
    available["jack"] = "Failed to import jack"


try:
    import pyaudio

    class PyAudioInput(Input):
        def __init__(self):
            self.rate = 41000
            p = pyaudio.PyAudio()
            self.stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.rate,
                input=True,
                frames_per_buffer=1024
            )

        def read(self):
            data = self.stream.read(1024)
            samples = [audioop.getsample(data, 2, n) for n in range(0, 1024)]
            return len(samples), samples

    available["pyaudio"] = PyAudioInput
except ImportError:
    available["pyaudio"] = "Failed to import pyaudio"


class DummyInput(Input):
    def __init__(self):
        log.info("Opening Dummy input")
        self.rate = 8000

    def read(self):
        frequency = random.choice([110, 220, 440, 880])
        duration_in_samples = self.rate / 10
        samples = [math.sin(2.0 * math.pi * frequency * t / self.rate) * (2 ** 16) for t in xrange(0, duration_in_samples)]
        time.sleep(1.0/self.rate)
        return len(samples), samples

available["dummy"] = DummyInput
