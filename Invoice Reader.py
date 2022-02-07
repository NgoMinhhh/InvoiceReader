#### Choose a folder directory and extract text from all Invoice pdfs inside,
#### Find invoice infos and paste them into a CSV file

import csv
import datetime
import logging
import os
from pathlib import Path
import re
from tkinter import Tk, filedialog

import fitz  # This is pymupdf
import yaml

# For logging and debugging
logging.basicConfig(level=logging.DEBUG,format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of program')

# A class for invoice elements
class inv_element:
    def __init__(self, name, pattern=None, flag=None):
        self.name   = name
        self.pattern  = pattern
        self.flag = flag

    # Compile regex object and return the first non-null group in matching result
    def get_result(self,text):
        if self.pattern != None:
            regex = re.compile(self.pattern) if self.flag == None else re.compile(self.pattern,re.I)
            group_count = self.pattern.count('|') + 1
            try:
                match = regex.search(text)
                for i in range(group_count):
                    if match.group(i+1) != None:
                        return  match.group(i+1)
            except AttributeError:
                return None 
        else:
            return None
# Function to return a list of specific files from a specific folder path 
def get_file_name_list(folder_path,file_type):
    upper_file_type = file_type.upper()
    file_name_list = [file for file in os.listdir(folder_path) if file.upper().endswith(upper_file_type)]
    return file_name_list

# Function to get all text from a pdf
def get_inv_text(path):
    doc = fitz.open(path)
    text = ''
    for page in doc:
        text += page.get_text()
    return text

## Get a list of available template file and one for its path
dirname_ = Path.cwd()
template_name_list = get_file_name_list(Path.joinpath(dirname_,'Template'),'.yaml')
template_path_list = [Path.joinpath(dirname_,'Template',template_name_list[i]) for i in range(len(template_name_list))]

## Parse yaml template into nested dict of invoice element object
template_element_dict = {}
for i, template in enumerate(template_name_list):
    yml_data = yaml.safe_load(open(template_path_list[i],encoding='utf-8'))
    template_element_dict[template] = [inv_element(**yml_data[ele]) for ele in yml_data.keys()]

## Get input prompt to select folder directory
while True:
    Tk().withdraw() 
    userSelected_folder_path = filedialog.askdirectory() 
    break

## Get all the pdf files in selected folder
pdf_name_list = get_file_name_list(userSelected_folder_path,'.PDF')

## Dictionary to for DictWriter
inv_data_dict = {}

### Create nested dict with each sub dict is the pdf
for pdf in pdf_name_list:
    inv_data_dict[pdf] = {}
    inv_data_dict[pdf]['Path'] = os.path.join(userSelected_folder_path,pdf) #Get path
    inv_data_dict[pdf]['Text'] = get_inv_text(inv_data_dict[pdf].get('Path'))
    
    ## Iterate throuth the list of template to find correct template
    for template in template_element_dict.keys():
        if any(template_element_dict[template][0].pattern in inv_data_dict[pdf]['Text'] for template in template_element_dict.keys()):
            inv_data_dict[pdf]['Provider'] = template_element_dict[template][0].pattern
            # Iterate the text through regex in matched template
            for element in template_element_dict[template][1:]:
                inv_data_dict[pdf][element.name] = element.get_result(inv_data_dict[pdf].get('Text'))
            break
        else:
            inv_data_dict[pdf]['Provider'] = 'Irrecognizable'

### Write invoice data list into a csv
## Get header for csv
csv_header = ['File Name','Path','Text']
for element in template_element_dict[template]:
    csv_header.append(element.name)

## Get CSV name at time created
csv_name_dt = datetime.datetime.now().strftime('%Y%m%d %H.%M.%S')

## Write CSV and save it at user selected folder
with open(f'{userSelected_folder_path}/output {csv_name_dt}.csv','w',newline='',encoding="utf-16") as output_csv:
    w = csv.DictWriter(output_csv, csv_header, delimiter = '\t')
    w.writeheader()
    for key,val in sorted(inv_data_dict.items()):
        row = {'File Name':key}
        row.update(val)
        w.writerow(row)
output_csv.close()

logging.debug('End of program')
