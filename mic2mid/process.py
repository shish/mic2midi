from mic2mid.utils import NoteMapper, get_peak_frequency, get_peak_frequencies, get_spectrum

import logging

log = logging.getLogger()


def process(input, output):
    mapper = NoteMapper()

    while True:
        # Read data from device
        l, samples = input.read()
        if l:
            spectrum = get_spectrum(samples)
            if max(samples) > 5000:
                peak_frequency, power = get_peak_frequency(spectrum, input.rate)
                #log.info("%s %s", peak_frequency, power)

                # ignore mic noise / silence / static
                if 10 < peak_frequency < 8000:
                    note = mapper.frequency_to_note(peak_frequency)
                    output.trigger_note(note)
            else:
                output.trigger_note(None)
