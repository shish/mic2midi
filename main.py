#!/usr/bin/python

import time, audioop
import logging
import argparse

from mic2midi.inputs import available as available_inputs
from mic2midi.process import process
from mic2midi.outputs import available as available_outputs

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", default="dummy")
    parser.add_argument("--output", "-o", default="dummy")
    args, extra = parser.parse_known_args()

    if args.input == "list":
        print "Inputs:"
        for name, ob in available_inputs.items():
            if type(ob) == str:
                print " ", name, "-", ob
            else:
                print " ", name, "-", "ok"
        input = None
    elif args.input == "auto":
        # TODO: give plugins priorities, pick the one which
        # has the highest priority out of those which work
        input = available_inputs["pyaudio"]()
    else:
        input = available_inputs[args.input]()

    if args.output == "list":
        print "Outputs:"
        for name, ob in available_outputs.items():
            if type(ob) == str:
                print " ", name, "-", ob
            else:
                print " ", name, "-", "ok"
        output = None
    elif args.output == "auto":
        # TODO: give plugins priorities, pick the one which
        # has the highest priority out of those which work
        output = available_outputs["rtmidi"]()
    else:
        output = available_outputs[args.output]()

    if input and output:
        try:
            process(input, output)
        except KeyboardInterrupt:
            print "Got Ctrl-C, exiting"


if __name__ == "__main__":
    main()
