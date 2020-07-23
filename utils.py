import sys

def quitWithError(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    sys.exit(84)

def eprintbis(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs, end='')

def printProbablesLetters(probables, inpt):
    for i in range(probables.__len__()):
        print("{" + inpt + probables[i] + "} " if i is not 5 else "}", end='')
    print("\n", end='')