Mic2Midi
========

Usage:
------
```
./main.py --input alsa --output rtmidi
```
```
./main.py --input file --infile song.wav --output file --outfile song.mid
```

`-i list` and `-o list` will show drivers and whether or not the necessary
libraries to use them are available.

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

The RtMIDI driver is currently hard-coded to use output port 1 because that's
where my loopmidi[1] instance listens. If you're running on windows
and just want to play notes directly, you can change it to use port
0 to write midi commands into the OS's player software.

[1] loopmidi can be useful for win32 -- mic2mid can use loopmidi as
an output device, then your other software can use loopmidi as
an input device - http://www.tobias-erichsen.de/software/loopmidi.html
