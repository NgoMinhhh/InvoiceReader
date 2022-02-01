# InvoiceReader
Script to read invoice pdf infos from a specific Issuer
Purpose: Extract text from all PDFs in folders then use regex to return data and write it into csv
Process:
    1. Prompt USER to Select folder -> get list of PDFs
    2. Create a nested dict to save pdf name, path, text
    3. Create a list of regex through a special class
    4. Run loop to get matching group and update it into the nested dict
    5. Write the nested dict to a csv file at selected folder

Class inv Element:
    1. attribute (name, regex)
    2. method(getResult)

TODO list:
    1. Save list of inv Element and its custom made regex into a yml file
    2. Read yml template into Main Process
