#!/usr/bin/python

import time, audioop
import logging
import argparse

import mic2mid.inputs
import mic2mid.process
import mic2mid.outputs

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", default="dummy")
    parser.add_argument("--output", "-o", default="dummy")
    args, extra = parser.parse_known_args()

    if args.input == "list":
        print "Inputs:"
        for name, ob in mic2mid.inputs.available.items():
            if type(ob) == str:
                print " ", name, "-", ob
            else:
                print " ", name, "-", "ok"
        input = None
    elif args.input == "auto":
        # TODO: give plugins priorities, pick the one which
        # has the highest priority out of those which work
        input = mic2mid.inputs.available["pyaudio"]()
    else:
        input = mic2mid.inputs.available[args.input]()

    if args.output == "list":
        print "Outputs:"
        for name, ob in mic2mid.outputs.available.items():
            if type(ob) == str:
                print " ", name, "-", ob
            else:
                print " ", name, "-", "ok"
        output = None
    elif args.output == "auto":
        # TODO: give plugins priorities, pick the one which
        # has the highest priority out of those which work
        output = mic2mid.outputs.available["rtmidi"]()
    else:
        output = mic2mid.outputs.available[args.output]()

    if input and output:
        try:
            mic2mid.process.process(input, output)
        except KeyboardInterrupt:
            print "Got Ctrl-C, exiting"


if __name__ == "__main__":
    main()
