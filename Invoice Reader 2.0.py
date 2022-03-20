# Invoice Reader 2.0

import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from tkinter import Tk, filedialog
from datetime import datetime

import fitz
import yaml


def main():

    # Get user to select the folder containing pdf invoices
    Tk().withdraw()
    selected_folder = filedialog.askdirectory()
    if len(selected_folder) == 0:
        sys.exit()
    # Get a list of pdf files in selected folder
    pdf_list = Path(selected_folder).glob('*.pdf')
    # Get a list of invoices from all pdfs in folder
    inv_list = []
    for pdf in pdf_list:
        inv_list += get_inv_list(pdf)

    # Get a list of available templates 
    template_list = Path.joinpath(Path.cwd(),'Template').glob('*.yaml')
    # Parse yaml templates into a nested dict
    template_regex = {}
    default_template = Path(Path.cwd(),'Template','Default.yaml')
    for template in template_list:
        content = yaml.safe_load(open(template,encoding='utf-8'))
        if template != default_template:
            template_regex[template.name] = [inv_element(name=ele,**content[ele]) for ele in content.keys()]
        else:
            default_regex = [inv_element(name=ele,**content[ele]) for ele in content.keys()]

    # Loop invs list through template list to return a nested dict
    ## 1st loop: iterate through inv in inv list
    for inv in inv_list:
        ## 2nd loop: iterate through template list to find matching template
        for template in template_regex:
            if template_regex[template][0].pattern in inv.content:
                ## 3rd loop: iterate through invoice element regex and return match directly into invoice instance atribute
                setattr(inv,'template',template)
                for element in template_regex[template][1:]:
                    setattr(inv,element.name,element.get_result(inv.content))
            else: # Use default if no compatible template found
                setattr(inv,'template','Default')
                for element in default_regex[1:]:
                    setattr(inv,element.name,element.get_result(inv.content))

    # Write list of invoice to csv
    csv_header = (list(inv_list[0].__dict__.keys()))
    csv_created_time = datetime.now().strftime('%Y%m%d %H%M%S')
    csv_file = Path(selected_folder,f'Output {csv_created_time}.csv')

    with open(csv_file,'w',newline='',encoding='utf-16') as f:
        w = csv.writer(f,delimiter='\t')
        w.writerow(csv_header)
        for inv in inv_list:
            w.writerow(inv)
    f.close()


class inv_element:
    def __init__(self, name, pattern=None, flag=None) -> None:
        self.name = name
        self.pattern = pattern
        self.flag = flag

    def get_regex(self):
        if self.flag == 'IGNORECASE':
            regex_ = re.compile(self.pattern,re.I)
        elif self.flag == 'DOTALL':
            regex_ = re.compile(self.pattern,re.DOTALL)
        elif self.flag == 'IGNORECASE | DOTALL' or self.flag == 'DOTALL | IGNORECASE':
            regex_ = re.compile(self.pattern, re.I | re.DOTALL)
        else:
            regex_ = re.compile(self.pattern)
        return regex_

    def get_result(self,text):
        if self.pattern != None:
            regex = self.get_regex()
            tempo_results = regex.search(text)
            try:
                for result in tempo_results.groups():
                    if result != None:
                        return result 
                    break
            except:
                result = 'Not Found'
        else:
            result = ''
        return result

    def __repr__(self):
        return f'Invoice Element ({self.name})'

@dataclass
class invoice:
    pdf_name: str
    page_numbers : str
    content : str

    def __iter__(self):
        for each in self.__dict__.values():
            yield each

# Get a list of Invoice class instances by seacrching for valid invs in pdf text
def get_inv_list(path):
    good_path = Path(path)
    temp_inv_list = []
    page_numbers = ['1']
    
    # Load first page in to first item in temporary invoice list
    doc = fitz.open(path)
    temp_inv_list.append(doc.load_page(0).get_text())
    try:
        # Loop from 2nd page, get its text and check for valid invoice
        for i, page in enumerate(doc.pages(1)):
            tempo_page = page.get_text()
            # If it is invoice and not of part of a multi one, create a new item in temporary invoice list for its text
            if is_inv(tempo_page) and not(is_mulitpage(tempo_page)):
                temp_inv_list.append(tempo_page)
                page_numbers.append(i+2)
            # Else append its text to last item in invoie list
            else:
                temp_inv_list[-1] += tempo_page
                page_numbers[-1] += f',{i+2}'
    except:
        pass
    # Return final list with invoice class
    inv_list = [invoice(good_path.name,page_numbers[i], temp_inv_list[i]) for i,_ in enumerate(temp_inv_list)]
    return inv_list

# Check for inv by searching for more than 1 result from regex matching
def is_inv(page_text):
        regex = re.compile(r'''((Hóa đơn Giá Trị Gia Tăng|Hóa đơn Bán hàng)| #Inv type
                                (Mẫu số)|                                    #Inv Form       
                                (Ký hiệu)|                                   #Inv Serial
                                (Số\s*\d{1,7})                               #Inv number
                                )''',re.I|re.VERBOSE|re.DOTALL)
        result = regex.findall(page_text)
        if len(result) > 0:
            return True
        else:
            return False

# Check if inv is multipage by perform regex matching on individual page text
def is_mulitpage(page_text):
        regex = re.compile(r'trang\D*[0-9]+\s*[\/]\D*[0-9]+',re.IGNORECASE|re.VERBOSE|re.DOTALL)
        result = regex.search(page_text)
        if result != None:
            return True
        else:
            return False

main()
