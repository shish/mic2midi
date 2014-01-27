import logging
import time
from mic2midi.utils import NoteMapper

log = logging.getLogger(__name__)
available = {}


class Output(object):
    def __init__(self):
        self._open = True
        self.last_note = None
        self.note_mapper = NoteMapper()

    def __del__(self):
        if self._open:
            self.close()

    def close(self):
        self._open = False

    def note_to_midi(self, note):
        return self.note_mapper.note_to_midi(note)

    def trigger_note(self, note):
        if note != self.last_note:
            if not note:
                log.info(self.last_note + " OFF")
                self.note_off(self.last_note)
            elif self.last_note:
                log.info(self.last_note + " TO " + note)
                self.note_change(self.last_note, note)
            else:
                log.info(note + " ON")
                self.note_on(note)
        self.last_note = note

    def note_on(self, note):
        pass

    def note_off(self, note):
        pass

    def note_change(self, note_from, note_to):
        self.note_off(note_from)
        self.note_on(note_to)


class DummyOutput(Output):
    url_example = "dummy://"

    def __init__(self, url):
        Output.__init__(self)

available["dummy"] = DummyOutput


try:
    import pypm

    class PyPMOutput(Output):
        url_example = "pypm://"

        def __init__(self, url):
            Output.__init__(self)
            log.info("Opening PyPM output")
            pypm.Initialize()
            self.midi = pypm.Output()

        def close(self):
            Output.close(self)
            pypm.Terminate()

        def note_on(self, note):
            self.midi.WriteShort(0x90, self.note_to_midi(note), 100)

        def note_off(self, note):
            self.midi.WriteShort(0x80, self.note_to_midi(note), 100)

    available["pypm"] = PyPMOutput
except ImportError:
    available["pypm"] = "Failed to import pypm"


try:
    import rtmidi

    class RtMidiOutput(Output):
        url_example = "rtmidi://<port number>"

        def __init__(self, url):
            Output.__init__(self)
            if not url.netloc:
                print "rtmidi:// needs a port number"
                print "\nAvailable Ports:"
                for port in self.midi.get_ports():
                    print "  ", port
                    raise ValueError("RtMidi needs a port")
            port = int(url.netloc)
            log.info("Opening RtMIDI output #%d" % port)
            self.midi = rtmidi.MidiOut()
            self.midi.open_port(port)
            #self.midi.open_virtual_port("Noter Virtual Keyboard")

        def note_on(self, note):
            self.midi.send_message([0x90, self.note_to_midi(note), 100])

        def note_off(self, note):
            self.midi.send_message([0x80, self.note_to_midi(note), 100])

    available["rtmidi"] = RtMidiOutput
except ImportError:
    available["rtmidi"] = "Failed to import rtmidi"


try:
    import pygame
    import pygame.midi
    from pygame.locals import *

    class PyGameOutput(Output):
        url_example = "pygame://<device id>"

        def __init__(self, url):
            Output.__init__(self)

            pygame.init()
            pygame.midi.init()

            if not url.netloc:
                print "pygame:// needs a device ID"
                for i in range( pygame.midi.get_count() ):
                    r = pygame.midi.get_device_info(i)
                    (interf, name, input, output, opened) = r

                    in_out = ""
                    if input:
                        in_out = "(input)"
                    if output:
                        in_out = "(output)"

                    print ("%2i: interface :%s:, name :%s:, opened :%s:  %s" %
                           (i, interf, name, opened, in_out))
                raise ValueError("PyGame output needs a device ID")

            device_id = int(url.netloc)
            log.info("Opening PyGame output")
            clock = pygame.time.Clock()
            midi_out = pygame.midi.Output(device_id, 0)

        def close(self):
            Output.close(self)
            pygame.quit()

    available["pygame"] = PyGameOutput
except ImportError:
    available["pygame"] = "Failed to import pygame"


try:
    from midiutil.MidiFile import MIDIFile

    class FileOutput(Output):
        url_example = "file://foo.mid"

        def __init__(self, url):
            Output.__init__(self)
            outfile = url.netloc + url.path

            if not outfile:
                print "file:// output needs a filename"
                raise ValueError("File output needs a filename")

            log.info("Opening File output: %s", outfile)
            self.midi = MIDIFile(1)
            self.midi.addTrackName(0, 0, "Mic2Mid Track 0")
            self.midi.addTempo(0, 0, 60)
            self.midi.addProgramChange(0, 0, 0, 27)
            self.start = time.time()
            self.filename = outfile

        def close(self):
            Output.close(self)
            log.info("Closing File output: %s", self.filename)
            fp = open(self.filename, "wb")
            self.midi.writeFile(fp)
            fp.close()

        def note_on(self, note):
            self.midi.addNote(0, 0, self.note_to_midi(note), time.time() - self.start, 1, 100)

    available["file"] = FileOutput
except ImportError:
    available["file"] = "Failed to import midiutil"
