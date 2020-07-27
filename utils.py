import sys
import Match
from Completion import CompletionState

def getline(stream, delimiter="\n"):
    def _gen():
        while 1:
            line = stream.readline()
            if line:
                if line.lower() == "abort":
                    sys.exit(0)
                if delimiter in line:
                    yield line[0:line.index(delimiter)]
                    break
                else:
                    yield line
    return "".join(_gen())

def quitWithError(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    sys.exit(84)

def eprintbis(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs, end='')

def printFinalCompletionAndQuit(completion):
    print("=> " + completion)
    sys.exit(0)

def askForAnInputWithNum(inputs, criterias, completedCity, completedStreetName):
    i = 1

    for elt in inputs:
        if criterias["completionState"] == CompletionState.CITY:
            print("{" + str(i) + " : " + elt.replace(completedCity, completedCity.upper()) + "}" + (" " if i != len(inputs) else "\n"), end='')
        else:
            print("{" + str(i) + " : " + elt.value.lower().replace(completedCity.lower(), completedCity.upper()).replace(completedStreetName, completedStreetName.upper()) + "}" + (" " if i != len(inputs) else "\n"), end='')
        i += 1
    inpt = getline(sys.stdin)
    try:
        value = int(inpt)
        if value < 1 or value >= i:
            sys.exit(12)
            askForAnInputWithNum(inputs, criterias)
    except:
        sys.exit(12)
        askForAnInputWithNum(inputs, criterias)
    if criterias["completionState"] == CompletionState.STREETNAME:
        printFinalCompletionAndQuit(inputs[int(inpt) - 1].value)
    else:
        return inputs[int(inpt) - 1]