import re
import Completion

#        Criterias needs to include:
#                   the initial dictionary OR a list of previous matched addresses to loop on
#                   the element that needs to be search in
#                   the element that needs to be search with
def matchWithCriterias(criterias):
    toLookIn = criterias["toLookIn"]
    completionState = criterias["completionState"]
    toMatch = criterias["toMatch"]
    matches = []

    for address in toLookIn:
        string = address.city.split(" ") if completionState == Completion.CompletionState.CITY else address.streetName.split(" ")
        for subString in string:
            if subString.find(toMatch) == 0:
                matches.append(address)
    return matches

def getTabOfDiffEltsOfAddrFrom(matched, criterias):
    tmp = []

    for address in matched:
        if criterias["completionState"] == Completion.CompletionState.CITY:
            if not address.city in tmp:
                tmp.append(address.city)
        if not criterias["completionState"]:
            if not address.streetName in tmp:
                tmp.append(address.streetName)
        elif criterias["completionState"] == Completion.CompletionState.STREETNAME:
            tmp = matched
    return tmp