import utils
import operator
import sys
from Address import Address
from collections import Counter

class Completion(object):
    def __init__(self, dicOfAddresses):
        self.dicOfAddresses = dicOfAddresses
        self.matchedAddresses = []
        self.isProcessing = True
        self.currentInput = ""
        self.concatInput = ""

    def process(self):
        self.lookForCity()
        if len(self.matchedAddresses) == 0:
            utils.eprint("Unknown address")
            sys.exit(84)
        self.displayMostProbables()
        self.lookForStreetName()

    def sort(self, pairs):
        tab = []
        res = ""
        tmp = ""

        for i in range(pairs.__len__() - 1):
            if pairs[i][1] == pairs[i + 1][1]:
                tab = pairs[i:pairs.__len__()]
                break
            else:
                res += pairs[i][0]
        for char, nbr in tab:
            tmp += char
        return (res + "".join(sorted(tmp)))[:5]


    def displayMostProbables(self):
        pairOfCharOccur = {}
        for address in self.dicOfAddresses:
            if address.isKnown:
                strs = address.city.split()
                for string in strs:
                    if not string[0].lower() in pairOfCharOccur:
                        pairOfCharOccur[string[0].lower()] = 1
                    else:
                        pairOfCharOccur[string[0].lower()] += 1
        sorted_char = list(reversed(sorted(pairOfCharOccur.items(), key=operator.itemgetter(1))))
        sorted_char = self.sort(sorted_char)
        utils.printProbables(sorted_char)


    def lookForCity(self):
        matchingAddresses = []
        for address in self.dicOfAddresses:
            if self.concatInput in address.city:
                matchingAddresses.append(address)
        self.matchedAddresses = matchingAddresses

    def lookForStreetName(self):
        matchingAddresses = []
        for address in self.dicOfAddresses:
            if self.concatInput in address.streetName:
                matchingAddresses.append(address)
        self.matchedAddresses = matchingAddresses