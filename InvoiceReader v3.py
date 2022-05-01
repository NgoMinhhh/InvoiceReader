from tkinter import Tk, filedialog
from invoice2data.main import extract_data
from invoice2data.extract.loader import read_templates
from invoice2data.input import pdfminer_wrapper
from pathlib import Path
import sys
from datetime import datetime
import csv


def main():
    """ USE INVOICE2DATA TO EXTRACT DATA FROM PDF INVOICE  """

    # Prompt User for folder selection
    Tk().withdraw()
    selected_folder = Path(filedialog.askdirectory())
    if not Path.is_dir(selected_folder):   # Exit if cancel selection
        sys.exit()
    print('Script starts')

    templates = []
    # Load templates from external folder if set.
    templates += read_templates(
        Path.joinpath(Path.cwd(), 'Template'))

    # get a list of valid pdf
    valid_pdfs = list(selected_folder.glob('*.pdf' or '*.PDF'))
    # Initilize an empty progress bar in terminal
    progress_bar(0, len(valid_pdfs))
    # Extract data
    output = []
    for i, f in enumerate(valid_pdfs):
        res = extract_data(f, templates=templates,
                           input_module=pdfminer_wrapper)
        if res:
            output.append(res)
            progress_bar(i+1, len(valid_pdfs))

    # Write result to CSV file, saved at selected folder
    output_created_time = datetime.now().strftime('%Y%m%d %H%M%S')
    output_file = Path.joinpath(
        selected_folder, f'Output {output_created_time}.csv')

    with open(output_file, 'w', newline='', encoding='utf-16') as f:
        w = csv.writer(f, delimiter="\t")
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
    print(
        f'\n Script Finished. Please head into {selected_folder} for output file.')


def progress_bar(progress, total):
    percent = 100 * (progress / float(total))
    bar = '█' * int(percent) + '-' * (100 - int(percent))
    print(f'\r|{bar}| {percent:.2f}%', end='\r')


if __name__ == "__main__":
    main()
