from Address import Address
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

def isValidAddress(line):
    pass

def processLines(line):
    if line == "ABORT\n" or line == "ABORT":
        sys.exit(0)
    match = re.findall(r"(?i)^((?![×Þß÷þø])[ \-\'a-zÀ-ÿ]+,?)(\s?)+([\d]+)(\s?)+(impasse|quai|rue|square|allée|place|boulevard|rue|chemin|avenue)(\s?)+((?![×Þß÷þø])[ \-\'a-zÀ-ÿ]+)$", line)
    address = Address()
    if (match and len(match[0]) == 7):
        match = match[0]
        address.city = match[0].replace(',', '')
        address.number = match[2]
        address.streetType = match[4]
        address.streetName = match[6]
        address.value = address.city + ", " + address.number + " " + address.streetType + " " + address.streetName
    else:
        address.isKnown = False
        address.value = line
    if not address.isKnown:
        utils.eprintbis(address.value)
    return address


def parse(path):
    res = []
    lines = getLinesOfFile(path)
    for line in lines:
        res.append(processLines(line))
    return res