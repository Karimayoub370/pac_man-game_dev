import sys
from typing import Any

class Parser():
    def __init__(self,path_file:str)->None:
        self.path_file = path_file
    def parse(self)->dict[Any:Any]:
        try:
            res:dict[] = {}
            val:str = ""
            i:int = 1
            with open(self.path_file) as f:
                for line in f:
                    line = line.strip()
                    if line == "" or line.startswith('#'):
                        continue
                    val = val+'\n' + line
                    res[i] = val
                    i += 1
            print(res)
        except Exception as e:
            print(e)
            sys.exit()