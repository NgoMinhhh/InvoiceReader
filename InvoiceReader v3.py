from tkinter import Tk, filedialog
from invoice2data.main import extract_data
from invoice2data.extract.loader import read_templates
from invoice2data.input import pdfminer_wrapper
from pathlib import Path
import sys
from datetime import datetime
import csv

def main():
    """ USE INVOICE2DATA TO EXTRACT DATA FROM PDF INVOICE 
   
    """
    # Prompt User for folder selection
    Tk().withdraw()
    selected_folder = Path(filedialog.askdirectory())
    if not Path.is_dir(selected_folder):   # Exit if cancel selection
        sys.exit()

    templates = []
    # Load templates from external folder if set.
    templates += read_templates(Path(r"C:\Users\PC41.VNPC41\Documents\Workspace\InvoiceReader\v3\Templates"))

    # Load pdfs and extract data
    output = []
    for f in selected_folder.glob('*.pdf'):
        res = extract_data(f, templates=templates, input_module=pdfminer_wrapper)
        if res:
            output.append(res) 
        # f.close()
    
    # Write result to CSV file, saved at selected folder
    output_created_time = datetime.now().strftime('%Y%m%d %H%M%S')
    output_file = Path.joinpath(selected_folder,f'Output {output_created_time}.csv')
    
    with open(output_file, 'w',newline='',encoding='utf-16') as f:
        w = csv.writer(f,delimiter="\t")
        # Write header
        for line in output:
            first_row = []
            for k, v in line.items():
                first_row.append(k)
        w.writerow(first_row)
       
       # Write content
        for line in output:
            csv_items = []
            for k, v in line.items():
                csv_items.append(v)
            w.writerow(csv_items)


if __name__ == "__main__":
    main()
