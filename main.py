#!/usr/bin/env python3

import re
import sys
import utils
from Parser import parse
from Completion import Completion

def getline(stream, delimiter="\n"):
    def _gen():
        while 1:
            line = stream.readline()
            if line:
                if delimiter in line:
                    yield line[0:line.index(delimiter)]
                    break
                else:
                    yield line
            else:
                sys.exit(84)
    return "".join(_gen())

def displayUsage():
    print("USAGE")
    print("     ./autoCompletion dictionary\n")
    print("DESCRIPTION")
    print("      dictionary    file containing one address per line, as knowledge base")

def main(argv):
    addresses = parse(argv[1])
    engine = Completion(addresses)
    begining = True

    engine.displayMostProbablesLetters(True)
    while engine.currentInput != "ABORT":
        engine.concatInput += getline(sys.stdin).lower()
        engine.process(begining)
        begining = False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        utils.quitWithError("Invalid usage, see ./autoCompletion -h for further informations")
        sys.exit(84)
    elif sys.argv[1] == "-h":
        displayUsage()
        sys.exit(0)
    main(sys.argv)