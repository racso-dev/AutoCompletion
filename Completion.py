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

    def printProbablesLetters(self, probables):
        i = 0
        for seq, nbr in probables:
            print("{" + (self.completedByEngine if self.completionState == CompletionState.STREETNAME else "") + seq[:len(seq) - 1].upper() + seq[-1].lower() + "} " if i is not 5 else "}", end='')
            i += 1
        print("\n", end='')

    def getAddressFromCity(self, city):
        tmp = ""

        for match in self.matchedAddresses:
            if match.value.lower().find(city.lower()) == 0:
                tmp = match.value
        return tmp

    def autoCompleteInput(self, criterias, pairs):
        if not criterias["noInput"]:
            if len(pairs) == 1:
                for key in pairs:
                    if pairs[key] > 1:
                        self.concatInput += key[-1]
        ret = self.getPairsOfSequenceOccurrencesIn(self.matchedAddresses, criterias)
        return ret

    def displayMostProbablesLetters(self, criterias):
        pairsOfSeqOcc = self.getPairsOfSequenceOccurrencesIn(self.matchedAddresses, criterias)
        pairsCompleted = self.autoCompleteInput(criterias, pairsOfSeqOcc)
        sortedPairsOfSeqOcc = sorted(pairsCompleted.items(), key=lambda x: (-x[1], x[0]))[:5]
        self.matchedAddresses = sorted(self.matchedAddresses, key=lambda address: address.value)

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