from numpy.fft import fft

import logging

log = logging.getLogger(__name__)

def get_spectrum(samples):
    result = fft(samples)
    return result[:len(result)/2]


def get_peak_frequency(spectrum, rate):
    best = -1
    best_idx = 0
    for n in range(0, len(spectrum)):
        if abs(spectrum[n]) > best:
            best = abs(spectrum[n])
            best_idx = n

    peak_frequency = best_idx * rate / (len(spectrum) * 2)
    return peak_frequency, best


def get_peak_frequencies(spectrum, rate):
    best = sorted(range(len(spectrum)), key=lambda i: spectrum[i], reverse=True)[:3]
    return [(n * rate / (len(spectrum) * 2), spectrum[n]) for n in best]


class NoteMapper(object):
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "Bb", "B"]

    def __init__(self):
        self._frequencies = []
        self._note_to_midi = {}

    def note_to_midi(self, note):
        """
        >>> nm = NoteMapper()

        High and low boundaries

        >>> nm.note_to_midi("C0")
        0
        >>> nm.note_to_midi("G10")
        127

        Octave cross over

        >>> nm.note_to_midi("B3")
        47
        >>> nm.note_to_midi("C4")
        48
        """
        if not self._note_to_midi:
            for n in range(0, 128):
                key = self.note_names[n % len(self.note_names)]
                octave = (n / len(self.note_names))
                self._note_to_midi[key + str(octave)] = n
        return self._note_to_midi[note]

    def frequency_to_note(self, target):
        """
        440Hz = A4 --> http://www.phys.unsw.edu.au/jw/graphics/notes.GIF

        >>> nm = NoteMapper()

        Lower and upper bounds

        >>> nm.frequency_to_note(32)
        'C0'
        >>> nm.frequency_to_note(440)
        'A3'
        >>> nm.frequency_to_note(12543.9)
        'G8'

        Octave boundary

        >>> nm.frequency_to_note(246.94)
        'B2'
        >>> nm.frequency_to_note(261.63)
        'C3'

        Non-exact matches
        >>> nm.frequency_to_note(870)
        'A4'
        >>> nm.frequency_to_note(890)
        'A4'
        """
        if not target:
            return "none"

        if not self._frequencies:
            a = 440.0
            for octave in range(0, 10):
                for note in range(0, 12):
                    i = (octave - 4) * 12 + note
                    self._frequencies.append(a * 2 ** (i/12.0))

            # the above generates a frequency table from A0 to A10,
            # but midi goes from C0 onwards, so cut A, A#, and B
            self._frequencies = self._frequencies[3:]

        min_distance = 999999
        best_idx = 0

        for n, frequency in enumerate(self._frequencies):
            distance = abs(frequency - target)
            if distance < min_distance:
                min_distance = distance
                best_idx = n

        octave = best_idx / 12
        note = best_idx % 12
        return self.note_names[note] + str(octave)
