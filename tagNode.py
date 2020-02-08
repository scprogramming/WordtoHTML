class tagNode:

    def __init__(self):
        self.value = ""
        self.next = None

    def setValue(self,valueIn):
        self.value = valueIn

    def setNext(self,nextIn):
        self.next = nextIn

    def getValue(self):
        return self.value

    def getNext(self):
        return self.next


