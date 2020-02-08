from Paragraph import Paragraph
from Element import Element
from tagStack import tagStack

def buildXMLElements(targetXML, fileName,numberingXML):
    outFile = open("HTMLOutput/" + fileName + ".html", "w")
    readFile = open(targetXML,encoding="utf8",mode="r")
    numberingFile = open(numberingXML,encoding="utf8",mode="r")

    numberingLines = numberingFile.readlines()
    lines = readFile.readlines()

    tagSplit = []
    appendedLines = ''
    appendedNumbering = ''
    tagSplitNumbering = []

    for line in lines:
        appendedLines = appendedLines + line

    for line in numberingLines:
        appendedNumbering = appendedNumbering + line

    while appendedLines != "":
        if appendedLines[0] == "<":
            tagSplit.append((appendedLines[appendedLines.index("<"):appendedLines.index(">") + 1]))
            appendedLines = appendedLines[appendedLines.index(">") + 1:]
        else:
            tagSplit.append(appendedLines[0:appendedLines.index("<")])
            appendedLines = appendedLines[appendedLines.index("<"):]

    while appendedNumbering != "":
        if appendedNumbering[0] == "<":
            tagSplitNumbering.append((appendedNumbering[appendedNumbering.index("<"):appendedNumbering.index(">") + 1]))
            appendedNumbering = appendedNumbering[appendedNumbering.index(">") + 1:]
        else:
            tagSplitNumbering.append(appendedNumbering[0:appendedNumbering.index("<")])
            appendedNumbering = appendedNumbering[appendedNumbering.index("<"):]

    print(tagSplit)
    print(tagSplitNumbering)

    abstractToListMap, abstractToNumIdMap = captureListTyping(tagSplitNumbering)
    paragraphList = buildParagraphs(tagSplit)
    createHTMLOutput(outFile,paragraphList,abstractToListMap,abstractToNumIdMap)

def captureListTyping(tagSplitNumbering):
    abstractToNumIdMap = dict()
    inNumId = False
    inAbstract = False
    currentAbstractId = 0
    currentNumId = 0
    abstractToListMap = dict()

    for tags in tagSplitNumbering:
        if "<w:num w:numId=" in tags:
            inNumId = True
            currentNumId = tags[tags.index('"')+1:tags.rfind('"')]
        elif "<w:abstractNumId w:val=" in tags and inNumId:
            abstractToNumIdMap[currentNumId] = tags[tags.index('"')+1:tags.rfind('"')]
            inNumId = False
        elif "<w:abstractNum " in tags:
            inAbstract = True
            splitTag = tags.split(" ")

            i = 0
            currentAbstractId = ""
            while "w:abstractNumId" not in currentAbstractId:
                currentAbstractId = splitTag[i]
                i += 1

            currentAbstractId = currentAbstractId[currentAbstractId.index('"')+1:currentAbstractId.rfind('"')]

        elif "<w:numFmt w:val" in tags and inAbstract:
            if not tags[tags.index('"')+1:tags.rfind('"')] in abstractToListMap:
                abstractToListMap[currentAbstractId] = tags[tags.index('"')+1:tags.rfind('"')]
            inAbstract = False

    return abstractToListMap, abstractToNumIdMap

def buildParagraphs(tagSplit):
    paragraphList = []

    paraEnabled = False

    for tags in tagSplit:
        if "<w:p" in tags and "w:rsidRDefault" in tags:
            currentParagraph = Paragraph()
            currentParagraph.setType("Paragraph")
            paraEnabled = True
        elif "</w:p>" in tags:
            paragraphList.append(currentParagraph)
        elif paraEnabled:
            currentParagraph.addElement(tags)

    for formats in paragraphList:
        inFormat = False
        formatStartIndex = 0
        i = 0

        for elements in formats.getElements():
            if "<w:pPr" in elements:
                inFormat = True
                formatStartIndex = i
            if "</w:pPr" in elements:
                inFormat = False
                listHolder = formats.getElements()
                del listHolder[formatStartIndex:i+1]
                formats.clearElements()
                formats.setElements(listHolder)
            if "<w:pStyle w:val" in elements and inFormat:
                formats.setType(elements[elements.index('"')+1:elements.rfind('"')])
            if "<w:ilvl w:val" in elements and inFormat:
                formats.setListIndent(elements[elements.index('"')+1:elements.rfind('"')])
            if "<w:numId w:val" in elements and inFormat:
                formats.setListId(elements[elements.index('"')+1:elements.rfind('"')])
            i += 1

    for formats in paragraphList:
        currentElementList = []
        currentText = ""
        inText = False
        for elements in formats.getElements():
            if "<w:r" in elements:
                currentElement = Element()
            elif "<w:b/>" in elements:
                currentElement.bold = True
            elif "<w:strike/>" in elements:
                currentElement.setStrikethrough(True)
            elif '<w:vertAlign w:val="subscript"/>' in elements:
                currentElement.setSubscript(True)
            elif '<w:vertAlign w:val="superscript"/>' in elements:
                currentElement.setSuperscript(True)
            elif "<w:i/>" in elements:
                currentElement.italics = True
            elif "<w:u" in elements:
                currentElement.underline = True
            elif "<w:t>" in elements or '<w:t xml:space=' in elements:
                inText = True
            elif "</w:r>" in elements:
                inElement = False
                currentElementList.append(currentElement)
            elif "</w:t>" in elements and inText:
                inText = False
                currentElement.setText(currentText)
                currentText = ""
            elif inText:
                currentText = currentText + elements


        formats.clearElements()
        formats.setElements(currentElementList)



    return paragraphList

def createHTMLOutput(outFile,paragraphList,abstractToListMap,abstractToNumIdMap):

    outFile.write("<html>\n")
    outFile.write("<head>\n")
    outFile.write('<link rel="stylesheet" href="style.css">\n')
    outFile.write("</head>\n")

    outFile.write("<body>\n")
    i = 0
    needOpenList = True

    for entries in paragraphList:
        closingTagOrder = tagStack()

        if entries.getType().lower() == "listparagraph":
            listType = abstractToNumIdMap[entries.getListid()]
            listType = abstractToListMap[listType]

            if needOpenList:
                if listType.lower() == "bullet":
                    outFile.write("<ul>\n")
                    needOpenList = False
                else:
                    outFile.write("<ol>\n")
                    needOpenList = False

            outFile.write("<li>")
        elif entries.getType().lower() == "paragraph":
            outFile.write("<p>")

        for elements in entries.getElements():
            if elements.getBold():
                outFile.write("<strong>")
                closingTagOrder.push("</strong>")
            if elements.getItalics():
                outFile.write("<em>")
                closingTagOrder.push("</em>")
            if elements.getUnderline():
                outFile.write('<span class="WordToHTML_SingleUnderline">')
                closingTagOrder.push("</span>")
            if elements.getStrikethrough():
                outFile.write("<strike>")
                closingTagOrder.push("</strike>")
            if elements.getSubscript():
                outFile.write("<sub>")
                closingTagOrder.push("</sub>")
            if elements.getSuperscript():
                outFile.write("<sup>")
                closingTagOrder.push("</sup>")

            outFile.write(elements.getText())

            while closingTagOrder.getSize() != 0:
                outFile.write(closingTagOrder.pop())

        if entries.getType().lower() == "listparagraph":
            outFile.write("</li>\n")

            if i + 1 < len(paragraphList):
                nextId = paragraphList[i + 1].getListid()

                if nextId != entries.getListid():
                    needOpenList = True
                    if listType.lower() == "bullet":
                        outFile.write("</ul>\n")
                    else:
                        outFile.write("</ol>\n")
            else:
                if listType.lower() == "bullet":
                    outFile.write("</ul>\n")
                else:
                    outFile.write("</ol>\n")
        else:
            outFile.write("</p>\n")
        i += 1

    outFile.write("</body>\n")
    outFile.write("</html>\n")
    outFile.close()