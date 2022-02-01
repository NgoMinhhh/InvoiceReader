import logging
from re import compile

# For logging and debugging
logging.basicConfig(level=logging.DEBUG,format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of program')

# A class for invoice elements
class inv_element():
    inv_element_list = []
    def __init__(self, name,pattern):
        self.name   = name
        self.pattern  = pattern
        self.__class__.inv_element_list.append(self)

    # Compile regex object and return group 1 in matching result
    def getResult(self,text):
        regex = compile(self.pattern)
        match = regex.match(text)
        return  match.group(1)
    
invNumber = inv_element('InvNumber' ,r'Invoice Number\:(\d*)')
invDate = inv_element('Inv date' ,r'(.*)')
#print(invNumber.getResult('Invoice Number:200138384'))

for element in inv_element.inv_element_list:
    print(element.name)
    print(element.pattern)

#TODO: A loop to iterate through list of text and list of regex
logging.debug('End of program')