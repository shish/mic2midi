Mic2Midi
========

Usage:
------
```
./main.py <input url> <output url>
./main.py alsa:// rtmidi://0
./main.py file://song.wav file://song.mid
```

You can mix and match realtime and files; everything is processed in realtime
(It should be possible to make file-to-file run as fast as the CPU can handle,
which is ~100x realtime, I just haven't got round to it yet)

Inputs:
-------
- PyAudio (Tested on Linux and Windows)
- ALSA (Tested on Linux)
- JACK (Tested on Linux)
- File (16-bit mono .wav)
- Dummy (Generate random A notes - 110Hz, 220Hz, 440Hz, etc)

Outputs:
--------
- RtMIDI (Tested on Linux and Windows)
- PyGame
- File (1-channel .mid)
- Dummy (Just print the keys)

Note that on windows, port 0 (rtmidi://0) is the software synth that
plays midi directly, which can be useful for tweaking settings.

loopmidi can be useful for win32 -- mic2midi can use loopmidi as an
output device (rtmidi://1), then your other software can use loopmidi as
an input device - http://www.tobias-erichsen.de/software/loopmidi.html
