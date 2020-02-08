from tagNode import tagNode

class tagStack:

    def __init__(self):
        self.top = None
        self.size = 0

    def push(self,elementIn):
        currentNode = tagNode()

        currentNode.setValue(elementIn)
        currentNode.setNext(self.top)
        self.top = currentNode
        self.size += 1

    def pop(self):
        holder = self.top
        self.top = self.top.getNext()
        self.size -= 1

        return holder.getValue()

    def peek(self):
        return self.top.getValue()

    def getSize(self):
        return self.size