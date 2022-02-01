import os
import fitz
from tkinter import Tk
from tkinter.filedialog import askdirectory

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
pdfText = {}
pdfText = {i : getAllText(i) for i in pdfPath}

