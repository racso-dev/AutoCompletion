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
        utils.quitWithError("Invalid argument")

def isValidAddress(line):
    pass

def trimWhitesSpaces(string):
    i = 0
    res1 = ""
    res2 = ""
    lgth = string.__len__()

    while i < lgth and string[i] == ' ':
        i += 1
    while i < lgth and string[i]:
        res1 += string[i]
        i += 1
    tmp = reversed(res1).__str__()
    i = 0
    while i < lgth and tmp[i] == ' ':
        i += 1
    while i < lgth and tmp[i]:
        res2 += string[i]
        i += 1

    return res2

def processLines(line):
    if line == "ABORT\n" or line == "ABORT":
        sys.exit(0)
    match = re.findall(r"(?i)^(\s?)+((?![×Þß÷þø])[ \-\'a-zÀ-ÿ]+,?)(\s?)+([\d]+)(\s?)+(impasse|quai|rue|square|allée|place|boulevard|rue|chemin|avenue)(\s?)+((?![×Þß÷þø])[ \-\'a-zÀ-ÿ]+)$", line)
    address = Address()
    if (match and len(match[0]) == 8):
        match = match[0]
        address.city = trimWhitesSpaces(match[1].replace(",", ""))
        # print("ADress.city ===", address.city)
        address.number = match[3]
        address.streetType = match[5]
        address.streetName = match[7]
        address.value = address.city + " " + address.number + " " + address.streetType + " " + address.streetName
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