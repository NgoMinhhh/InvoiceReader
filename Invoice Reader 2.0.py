# Invoice Reader 2.0

import re
import sys
from pathlib import Path
from pprint import pprint
from tkinter import Tk, filedialog

import yaml
import fitz

def main():

    # Get user to select the folder containing pdf invoices
    Tk().withdraw()
    selected_folder = filedialog.askdirectory()
    if len(selected_folder) == 0:
        sys.exit()
    # Get a list of pdf files in selected folder
    pdf_list = Path(selected_folder).glob('*.pdf')

    # Get a list of available templates 
    template_list = Path.joinpath(Path.cwd(),'Template').glob('*.yaml')
    # Parse yaml templates into a nested dict
    regex_dict = {}
    for template in template_list:
        content = yaml.safe_load(open(template,encoding='utf-8'))
        regex_dict[template.name] = [inv_element(**content[ele]) for ele in content.keys()]


class inv_element:
    def __init__(self, pattern, flag=None) -> None:
        self.pattern = pattern
        self.flag = flag
    
class pdf_text: 
    def __init__(self,path) -> None:
        self.path = path
    ## TODO: Seperate each inv in 1 pdf

main()