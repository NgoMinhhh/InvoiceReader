from re import compile
import os
import fitz
from tkinter import Tk
from tkinter.filedialog import askdirectory

class inv_element:
    inv_element_list = []
    def __init__(self, name, pattern):
        self.name   = name
        self.pattern  = pattern
        self.__class__.inv_element_list.append(self)

    # Compile regex object and return group 1 in matching result
    def getResult(self,text):
        regex = compile(self.pattern)
        try:
            match = regex.search(text)
            return  match.group(1)
        except AttributeError:
            return None 

# Function to get all text from a pdf
def getAllText(path):
    doc = fitz.open(path)
    text = ''
    for page in doc:
        text += page.get_text()
    return text

# Get input prompt to select folder directory
Tk().withdraw() 
folderPath = askdirectory() 

# Create list for filepath
pdfPath = []
pdfPath = [os.path.join(folderPath,pdf) for pdf in os.listdir(folderPath)]

# Create a dictionary with pdf file path as key and its text as value
pdfText = []
pdfText = [getAllText(i) for i in pdfPath]

regex = (r'Invoice No.*\n(.*)|Invoice Number\:(\d*)')
invNumber = compile(regex)
mo = invNumber.search(pdfText[1])

n = regex.count('|')
for i in range(n+1):
    print(f'this is i: {i}')
    if mo.group(i+1) != None:
        print(mo.group(i+1))
        print(f'This is i+1: {i+1}')
    else:
        print('No matching result')
        print(f'This is i+1: {i+1}')
