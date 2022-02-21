import re

class inv_element:
    def __init__(self, name, pattern=None, flag=None):
        self.name   = name
        self.pattern  = pattern
        self.flag = flag

    def get_regex(self):
        if self.flag == 're.IGNORECASE':
            regex = re.compile(self.pattern,re.I)
        elif self.flag == 're.DOTALL':
            regex = re.compile(self.pattern,re.DOTALL)
        else:
            regex = re.compile(self.pattern)
        return regex

    # Compile regex object and return the first non-null group in matching result
    def get_result(self,text):
        if self.pattern != None:
            group_count = self.pattern.count('|') + 1
            try:
                match = self.get_regex().search(text)
                for i in range(group_count):
                    if match.group(i+1) != None:
                        return  match.group(i+1)
            except AttributeError:
                return None 
        else:
            return None
