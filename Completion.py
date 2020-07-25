import utils
import operator
import sys
from Address import Address
from collections import Counter
from enum import Enum, auto
import Match

class CompletionState(Enum):
    CITY = 1
    STREETNAME = 2

class Completion(object):
    def __init__(self, dicOfAddresses):
        self.dicOfAddresses = dicOfAddresses
        self.matchedAddresses = dicOfAddresses
        self.completionState = CompletionState.CITY
        self.concatInput = ""
        self.completedByEngine = ""

    def process(self):
        self.matchedAddresses = Match.matchWithCriterias({
            "toLookIn": self.matchedAddresses,
            "completionState": self.completionState,
            "toMatch": self.concatInput
        })
        tmp = Match.getTabOfDiffEltsOfAddrFrom(self.matchedAddresses, {"completionState": self.completionState})
        if len(tmp) == 0:
            utils.quitWithError("Unknown address")
        elif len(tmp) == 1:
            if self.completionState == CompletionState.CITY:
                self.completedByEngine = tmp[0].upper() + ", "
                self.completionState = CompletionState.STREETNAME
                self.concatInput = ""
                self.displayMostProbablesLetters({"noInput": True})
            elif self.completionState == CompletionState.STREETNAME:
                utils.printFinalCompletionAndQuit(tmp[0].value)
        else:
            self.matchedAddresses = Match.matchWithCriterias({
                "toLookIn": self.matchedAddresses,
                "completionState": self.completionState,
                "toMatch": self.concatInput
            })
            self.displayMostProbablesLetters({"noInput": False})

    def getPairsOfSequenceOccurrencesIn(self, toMap, criterias):
        pairs = {}

        for address in toMap:
            string = address.city.split(" ") if self.completionState == CompletionState.CITY else address.streetName.split(" ")
            for subString in string:
                lettersSequence = subString[:self.concatInput.__len__() + 1]
                if not lettersSequence in pairs:
                    pairs[lettersSequence] = 1
                else:
                    pairs[lettersSequence] += 1
                if not criterias["noInput"] and subString.find(self.concatInput) != 0:
                    pairs.pop(lettersSequence)
        return pairs

    def sortPairsOfSequenceOccurrences(self, pairsOfSeqOcc):
        rev_sorted = reversed(sorted(pairsOfSeqOcc.items(), key=operator.itemgetter(1)))
        sortedPairsOfSeqOcc = list(rev_sorted)
        sortedPairsOfSeqOcc = utils.sortByOccAndAlpha(sortedPairsOfSeqOcc)
        return sortedPairsOfSeqOcc

    def printProbablesLetters(self, probables):
        i = 0
        for probable in probables:
            print("{" + (self.completedByEngine if self.completionState == CompletionState.STREETNAME else "") + probable[:len(probable) - 1].upper() + probable[-1].lower() + "} " if i is not 5 else "}", end='')
            i += 1
        print("\n", end='')

    def getAddressFromCity(self, city):
        tmp = ""

        for match in self.matchedAddresses:
            if match.value.lower().find(city.lower()) == 0:
                tmp = match.value
        return tmp

    def displayMostProbablesLetters(self, criterias):
        pairsOfSeqOcc = self.getPairsOfSequenceOccurrencesIn(self.matchedAddresses, criterias)
        sortedPairsOfSeqOcc = self.sortPairsOfSequenceOccurrences(pairsOfSeqOcc)

        self.matchedAddresses = utils.sortAlphaMatches(self.matchedAddresses)
        if self.completionState == CompletionState.CITY:
            if len(sortedPairsOfSeqOcc) == 1:
                tmp = Match.getTabOfDiffEltsOfAddrFrom(self.matchedAddresses, {"completionState": self.completionState})
                inpt = utils.askForAnInputWithNum(tmp, {"completionState": self.completionState})
                final = self.getAddressFromCity(inpt)
                utils.printFinalCompletionAndQuit(final)
            else:
                self.printProbablesLetters(sortedPairsOfSeqOcc)
        else:
            if len(sortedPairsOfSeqOcc) == 1 and utils.isSameCitiesAndStreetNames(self.matchedAddresses):
                utils.askForAnInputWithNum(self.matchedAddresses, {"completionState": self.completionState})
            else:
                if len(self.matchedAddresses) == 1:
                    utils.printFinalCompletionAndQuit(self.matchedAddresses[0].value)
                else:
                    self.printProbablesLetters(sortedPairsOfSeqOcc)