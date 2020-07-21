from Adress import Adress
import utils

import re
import sys

def getLinesOfFile(path):
    try:
        file = open(path, 'r')
        Lines = file.readlines()
        return Lines
    except FileNotFoundError:
        utils.eprint("Invalid argument")
        sys.exit(84)

def isValidAdress(line):
    pass

def processLines(line):
    if line == "ABORT\n" or line == "ABORT":
        sys.exit(0)
    match = re.findall(r"(?i)^((?![×Þß÷þø])[ \-\'a-zÀ-ÿ]+,)(\s?)+([\d]+)(\s?)+(impasse|quai|rue|square|allée|place|boulevard|rue|chemin|avenue)(\s?)+((?![×Þß÷þø])[ \-\'a-zÀ-ÿ]+)$", line)
    adress = Adress()
    if (match and len(match[0]) == 7):
        match = match[0]
        adress.city = match[0].replace(',', '')
        adress.number = match[2]
        adress.streetType = match[4]
        adress.streetName = match[6]
        adress.value = adress.city + ", " + adress.number + " " + adress.streetType + " " + adress.streetName
    else:
        adress.isKnown = False
    if not adress.isKnown:
        utils.eprint(line)
    return adress


def parse(path):
    res = []
    lines = getLinesOfFile(path)
    for line in lines:
        res.append(processLines(line))
    return res