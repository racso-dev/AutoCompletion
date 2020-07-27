#!/usr/bin/env python3

import re
import sys
import utils
from Parser import parse
from Completion import Completion

def displayUsage():
    print("USAGE")
    print("     ./autoCompletion dictionary\n")
    print("DESCRIPTION")
    print("      dictionary    file containing one address per line, as knowledge base")

def main(argv):
    addresses = parse(argv[1])
    engine = Completion(addresses)

    if len(addresses) == 0:
        utils.quitWithError("No valid addresses found in dictionary")
    elif len(addresses) == 1:
        utils.printFinalCompletionAndQuit(addresses[0].value)
    engine.displayMostProbablesLetters({"noInput": True})
    while 1:
        currentInput = utils.getline(sys.stdin).lower()
        if currentInput:
            engine.concatInput += currentInput
            if (currentInput == "abort"):
                sys.exit(0)
            engine.process()
        else :
            engine.displayMostProbablesLetters({"noInput": True})


if __name__ == "__main__":
    if len(sys.argv) != 2:
        utils.quitWithError("Invalid usage, see ./autoCompletion -h for further informations")
        sys.exit(84)
    elif sys.argv[1] == "-h":
        displayUsage()
        sys.exit(0)
    main(sys.argv)