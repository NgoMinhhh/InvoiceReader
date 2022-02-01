import fitz  # this is pymupdf
import re    # working with regex
import openpyxl # working with excel
import xlsxwriter
__all__ = [fitz,openpyxl,re]

# TODO: Loop through pdf in Folder
    # Open PDF
    # Extract text from all pages
with fitz.open(r'C:\Users\USER\Documents\Coding\Practice\InvoiceReader - legacy\inv-0200138518.pdf') as doc: 
    text = ""
    for page in doc:
        text += page.get_text()

#TODO: paste all matching results into workbook
# Create a blank workbook
wb = openpyxl.Workbook()
sheet = wb.active


#TODO: Map all header and data into Dictionay
#TODO - Done: Loop in list to return all match 

    # Pattern matching with Regex       
invNumbRegex = re.compile(r'Invoice Number\:(\d+)') #Inv Number
invDateRegex = re.compile(r'Invoice Date\:(.+)')    #Inv Date
invPORegex = re.compile(r'PO Number\:(.+)')         #PO Number
invDescRegex = re.compile(r'Amount\(VND\)\n(.*)\n(.*)')   #Description & amount
buyerNameRegex = re.compile(r'To\n(.+)')            #Buyer Name
invTaxRegex = re.compile(r'Output Tax\n(.*)\n(.*)') #Tax amount & Tax rate
invTotalRegex = re.compile(r'Total Amount in\(VND\)\n(.*)') #Total amount

    # Group regex into 2 group
group1Regex = [invDateRegex,invNumbRegex,invPORegex,invTotalRegex,buyerNameRegex] 
group2Regex = [invDescRegex,invTaxRegex]    # Results are in two groups

    # Match string and return result
for regex in group1Regex:
    a = re.search(regex,text)
    print(a.group(1))

for regex in group2Regex:
    b = re.search(regex,text)
    print(b.group(1))
    print(b.group(2))

wb.save(r'C:\Users\USER\Documents\Coding\Practice\InvoiceReader - legacy\Test.xlsx')