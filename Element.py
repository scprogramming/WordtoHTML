class Element:

    def __init__(self):
        self.bold = False
        self.underline = False
        self.italics = False
        self.text = ""

    def setBold(self,boldIn):
        self.bold = boldIn

    def setUnderline(self,underlineIn):
        self.underline = underlineIn

    def setText(self,textIn):
        self.text = textIn

    def setItalics(self,italicsIn):
        self.italics = italicsIn

    def getBold(self):
        return self.bold

    def getUnderline(self):
        return self.underline

    def getText(self):
        return self.text

    def getItalics(self):
        return self.italics