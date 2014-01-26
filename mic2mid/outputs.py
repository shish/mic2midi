import logging
from mic2mid.utils import NoteMapper

log = logging.getLogger(__name__)
available = {}


class Output(object):
    def __init__(self):
        self.last_note = None
        self.note_mapper = NoteMapper()

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
    pass

available["dummy"] = DummyOutput


try:
    import pypm

    class PyPMOutput(Output):
        def __init__(self):
            Output.__init__(self)
            log.info("Opening PyPM output")
            pypm.Initialize()
            self.midi = pypm.Output()

        def __del__(self):
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
        def __init__(self):
            Output.__init__(self)
            log.info("Opening RtMIDI output")
            self.midi = rtmidi.MidiOut()
            available_ports = self.midi.get_ports()
            print "Ports:", available_ports
            self.midi.open_port(1)
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
        def __init__(self):
            Output.__init__(self)
            log.info("Opening PyGame output")

            device_id = 2

            try:
                device_id = int( sys.argv[-1] )
            except:
                pass

            # Init
            pygame.init()
            pygame.midi.init()

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

            clock = pygame.time.Clock()
            midi_out = pygame.midi.Output(device_id, 0)

        def __del__(self):
            pygame.quit()

    available["pygame"] = PyGameOutput
except ImportError:
    available["pygame"] = "Failed to import pygame"
