import os
import collections
from tkinter import Tk
from tkinter.filedialog import askdirectory
from pathlib import Path

# Get user to select folder
Tk().withdraw() 
folderPath = askdirectory()

# Get all the files in selected folder
name_list = os.listdir(folderPath)
inv_list = collections.defaultdict(dict)

# Create nested dict with each sub dict is the pdf
for i in name_list:
    inv_list[i] = {}
    inv_list[i]['Path'] = os.path.join(folderPath,i) #Get path

