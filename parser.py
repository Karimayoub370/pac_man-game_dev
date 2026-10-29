import sys
from typing import Any

class Parser():
    def __init__(self,path_file:str)->None:
        self.path_file = path_file

    def init_parse(self)->dict[int:str]:
        try:
            res:dict[int:str] = {}
            i:int = 1
            with open(self.path_file) as f:
                for line in f:
                    line = line.strip()
                    if line == "" or line.startswith('#'):
                        continue
                    if  line:
                        res[i] = line
                        i += 1
            return res
        except Exception as e:
            print(e)
            sys.exit()