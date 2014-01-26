from numpy.fft import fft
from mic2mid.utils import NoteMapper

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


