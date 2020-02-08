class Paragraph:

    def __init__(self):
        self.type = ""
        self.elements = []
        self.listIndent = -1
        self.listId = -1

    def getType(self):
        return self.type

    def getElements(self):
        return self.elements

    def getListIndent(self):
        return self.listIndent

    def getListid(self):
        return self.listId

    def setListIndent(self,listIndentIn):
        self.listIndent = listIndentIn

    def setType(self,typeIn):
        self.type = typeIn

    def addElement(self,elementToAdd):
        self.elements.append(elementToAdd)

    def clearElements(self):
        self.elements = []

    def setElements(self,elementsIn):
        self.elements = elementsIn

    def setListId(self,listIdIn):
        self.listId = listIdIn