class Element:

    def __init__(self):
        self.bold = False
        self.underline = False
        self.italics = False
        self.text = ""
        self.strikethrough = False
        self.subscript = False
        self.superscript = False

    def setBold(self,boldIn):
        self.bold = boldIn

    def setUnderline(self,underlineIn):
        self.underline = underlineIn

    def setText(self,textIn):
        self.text = textIn

    def setItalics(self,italicsIn):
        self.italics = italicsIn

    def setStrikethrough(self,strikethroughIn):
        self.strikethrough = strikethroughIn

    def setSubscript(self,subscriptIn):
        self.subscript = subscriptIn

    def setSuperscript(self,superscriptIn):
        self.superscript = superscriptIn

    def getBold(self):
        return self.bold

    def getUnderline(self):
        return self.underline

    def getText(self):
        return self.text

    def getItalics(self):
        return self.italics

    def getStrikethrough(self):
        return self.strikethrough

    def getSubscript(self):
        return self.subscript

    def getSuperscript(self):
        return self.superscript