from numpy.fft import fft
from mic2midi.utils import NoteMapper

import logging

log = logging.getLogger()


def process(input, output):
    mapper = NoteMapper()

    while True:
        # Read data from device
        # eg noise = blablabla
        sample_count, samples = input.read()
        if not sample_count:
            continue

        # Turn noise into individual frequencies
        # eg noise = (260Hz * 2) + (430Hz * 10) + (1800Hz * 6)
        spectrum = get_spectrum(samples)

        # Check if the total volume of the noise is over a basic threshold
        # (perhaps we should check the volume of individual notes?)
        if max(samples) > 4000:
            # Find the most powerful frequency (bail if we can't find one)
            # eg (430Hz * 10)
            peak_frequency, power = get_peak_frequency(spectrum, input.rate)
            if not peak_frequency:
                continue

            # Round the frequency to the closest note
            # eg 430Hz detected -> 392Hz = G, 440Hz = A -> A is closest
            note = mapper.frequency_to_note(peak_frequency)

            # Print the note
            output.trigger_note(note)
        else:
            output.trigger_note(None)


def get_spectrum(samples):
    result = fft(samples)
    return result[:len(result)/2]


def get_peak_frequency(spectrum, rate):
    best = -1
    best_idx = 0
    for n, value in enumerate(spectrum):
        if abs(value) > best:
            best = abs(value)
            best_idx = n

    peak_frequency = best_idx * rate / (len(spectrum) * 2)
    return peak_frequency, best


def get_peak_frequencies(spectrum, rate):
    """
    Given a FFT result spectrum, return a list of

        [(freq, power), (freq, power), (freq, power), ...]

    sorted by power, most powerful first
    """
    best = sorted(range(len(spectrum)), key=lambda i: spectrum[i], reverse=True)[:3]
    return [(n * rate / (len(spectrum) * 2), spectrum[n]) for n in best]
