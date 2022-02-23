# InvoiceReader

Script to read invoice pdf infos from a specific Issuer
Purpose: Extract text from all PDFs in folders then use regex to return data and write it into csv
Process: 1. Prompt USER to Select folder -> get list of PDFs 2. Create a nested dict to save pdf name, path, text 3. Create a list of regex through a special class 4. Run loop to get matching group and update it into the nested dict 5. Write the nested dict to a csv file at selected folder

TODO list: 1. Seperate unique inv in 1 pdf
