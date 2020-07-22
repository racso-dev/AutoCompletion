import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def eprintbis(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs, end='')

def printProbables(probables):
    for probable in probables:
        print("{" + probable + "} ", end='')
    print("\n", end='')