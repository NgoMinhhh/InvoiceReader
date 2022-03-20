# InvoiceReader

Script to read invoice pdf infos from a specific Issuer

Purpose: Extract text from all PDFs in folders then use regex to return data and write it into csv

Process:

1. Prompt USER to Select folder -> get list of PDFs
2. Extract text from pdfs with fitz module
3. Seperate text into valid invoices incase there are multiple invoices in 1 pdf
4. Match inv text with existing template and return data
5. Write r a csv file at selected folder
