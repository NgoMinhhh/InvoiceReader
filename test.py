from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askdirectory

Tk().withdraw() 
folderPath = askdirectory() 

# Create list for filepath
pdfPath = []
pdfPath = list(Path(folderPath).glob('*.pdf'))

inv_list = {}

### Create nested dict with each sub dict is the pdf
for i in pdfPath:
    inv_list[i] = {}
    inv_list[i]['Path'] = str(pdfPath[i]) #Get path

print(str(inv_list))
