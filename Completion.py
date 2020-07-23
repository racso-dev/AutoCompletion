import utils
import operator
import sys
from Address import Address
from collections import Counter
from enum import Enum, auto

class CompletionState(Enum):
    CITY = 1
    STREETNAME = 2

class Completion(object):
    def __init__(self, dicOfAddresses):
        self.dicOfAddresses = dicOfAddresses
        self.matchedAddresses = []
        self.matchedCities = [] #à retirrer ?
        self.matchedStreetNames = [] # idem ?
        self.isProcessing = True
        self.currentInput = ""
        self.concatInput = ""
        self.completedByEngine = ""
        self.completionState = CompletionState.CITY

    def process(self, isBegining):
        if self.completionState == CompletionState.CITY:
            self.lookForCity(isBegining)
            if not self.matchedCities:
                utils.quitWithError("Unknown address")
            elif self.matchedCities.__len__() == 1:
                self.completionState = CompletionState.STREETNAME
                self.completedByEngine = self.matchedCities[0].upper() + ", "
                self.concatInput = ""
            else:
                self.concatInput = self.concatInput.upper()
                # self.conpletedByEngine += self.concatInput
                self.displayMostProbablesLetters(False)
        if self.completionState == CompletionState.STREETNAME:
            self.lookForStreetName(True)
            self.displayMostProbablesLetters(False)

    def sortByOccAndAlpha(self, pairs):
        tab = []
        res, tmp = "", ""
        i = 0

        while i < pairs.__len__():
            while i < pairs.__len__() - 1 and pairs[i][1] != pairs[i + 1][1]:
                res += pairs[i][0]
                i += 1
            tab = pairs[i:pairs.__len__()]
            break

        for char, nbr in tab:
            tmp += char
        return (res + "".join(sorted(tmp)))[:5]

    def displayMostProbablesLetters(self, isBegining):
        pairOfCharOccur = {}
        toMap = self.dicOfAddresses if isBegining else self.matchedAddresses

        for address in toMap:
            strs = address.city.split() if self.completionState == CompletionState.CITY else address.streetName.split()
            for string in strs:
                if not string[self.concatInput.__len__()].lower() in pairOfCharOccur:
                    pairOfCharOccur[string[self.concatInput.__len__()].lower()] = 1
                else:
                    pairOfCharOccur[string[self.concatInput.__len__()].lower()] += 1
        sorted_char = list(reversed(sorted(pairOfCharOccur.items(), key=operator.itemgetter(1))))
        sorted_char = self.sortByOccAndAlpha(sorted_char)
        if self.completionState == CompletionState.CITY:
            utils.printProbablesLetters(sorted_char, self.concatInput)
        else:
            utils.printProbablesLetters(sorted_char, self.completedByEngine)

    def lookForCity(self, isFirstCall):
        matchingAddresses = []
        matchingCities = []
        toMap = self.dicOfAddresses if isFirstCall else self.matchedAddresses

        for address in toMap:
            if address.isKnown:
                if address.city.lower().find(self.concatInput.lower()) == 0:
                    matchingAddresses.append(address)
                if address.city.lower().find(self.concatInput.lower()) == 0 and address.city not in matchingCities:
                    matchingCities.append(address.city)
        self.matchedAddresses = matchingAddresses
        self.matchedCities = matchingCities

    def lookForStreetName(self, isFirstCall):
        matchingAddresses = []
        matchingStreetNames = []
        if not isFirstCall:
            for address in self.matchedAddresses:
                if address.isKnown:
                    if address.streetName.lower().find(self.completedByEngine.lower()) == 0:
                        matchingAddresses.append(address)
                    if address.streetName.lower().find(self.completedByEngine.lower()) == 0 and address.streetName not in matchingStreetNames:
                        matchingStreetNames.append(address.streetName)
            self.matchedAddresses = matchingAddresses
            self.matchedStreetNames = matchingStreetNames