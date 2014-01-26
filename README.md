Mic2Mid
~~~~~~~

Usage:
./main.py --input alsa --output rtmidi

"-i list" / "-o list" will show drivers and whether or not the necessary
libraries to use them are available

Inputs:
- ALSA
- JACK
- PyAudio (Win32)
- Dummy (Generate random A notes)

Outputs:
- PyGame
- RtMIDI
- Dummy (Just print the keys)

loopmidi can be useful for win32 -- mic2mid can use loopmidi as
an output device, then your other software can use loopmidi as
an input device
