import os
import zipfile
from wordParser import *


for file in os.listdir("targetWord"):
    if file.endswith(".docx"):
        with zipfile.ZipFile("targetWord/" + file, 'r') as zipref:
            zipref.extractall("targetWord/" + file[0:file.index(".docx")])
            buildXMLElements("targetWord/" + file[0:file.index(".docx")] + "/word/document.xml", file[0:file.index(".docx")],"targetWord/" + file[0:file.index(".docx")] + "/word/numbering.xml" )