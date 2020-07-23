class Address(object):
    def __init__(self):
        self.city = ""
        self.number = ""
        self.streetType = ""
        self.streetName = ""
        self.value = ""
        self.isKnown = True
        self.matched = "" #TODO : Init to the type of the matched (ex: self.city or self.streetName)