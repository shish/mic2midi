Mic2Mid
=======

Usage:
------
./main.py --input alsa --output rtmidi

"-i list" / "-o list" will show drivers and whether or not the necessary
libraries to use them are available

Inputs:
-------
- ALSA (Tested on Linux)
- JACK (Tested on Linux)
- PyAudio (Tested on Win32)
- File (16-bit mono .wav)
- Dummy (Generate random A notes)

Outputs:
--------
- PyGame
- RtMIDI (Tested on Linux and Windows)
- File (1-channel .mid)
- Dummy (Just print the keys)

loopmidi[1] can be useful for win32 -- mic2mid can use loopmidi as
an output device, then your other software can use loopmidi as
an input device

The RtMIDI driver is currently hard-coded to use output port 1 because that's
where my loopmidi instance listens. If you're running on windows
and just want to play notes directly, you can change it to use port
0 to write midi commands into the OS's player software.

[1] http://www.tobias-erichsen.de/software/loopmidi.html
