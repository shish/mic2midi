#!/usr/bin/python

import time, audioop
import logging
import sys
from urlparse import urlparse

from mic2midi.inputs import available as available_inputs
from mic2midi.process import process
from mic2midi.outputs import available as available_outputs

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


def help():
    print "Usage: %s <input url> <output url>" % sys.argv[0]

    print "\nInputs:"
    for name, ob in available_inputs.items():
        if type(ob) == str:
            print " ", name, "-", ob
        else:
            print " ", name, "-", ob.url_example

    print "\nOutputs:"
    for name, ob in available_outputs.items():
        if type(ob) == str:
            print " ", name, "-", ob
        else:
            print " ", name, "-", ob.url_example

def main():
    input = None
    output = None
    try:
        input_url = urlparse(sys.argv[1])
        output_url = urlparse(sys.argv[2])
    except IndexError:
        help()
        return 1

    try:
        input = available_inputs[input_url.scheme](input_url)
        output = available_outputs[output_url.scheme](output_url)
    except ValueError:
        # missing params in URL
        return 2

    try:
        process(input, output)
    except EOFError:
        print "End of file"
        output.close()
    except KeyboardInterrupt:
        print "Got Ctrl-C, exiting"


if __name__ == "__main__":
    main()
