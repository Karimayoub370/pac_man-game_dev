try:
    import sys
except BaseException as e:
    print(e)
    sys.exit()



class Parser():
    def __init__(self,path_file:str):
        self.path_file = path_file
    def parse(self):
        try:
            res = ""
            with open(self.path_file) as f:
                for line in f:
                    line = line.strip()
                    if line == "" or line.startswith('#'):
                        continue
                    res = res+'\n' + line
                    
            print(res[1:])
        except Exception as e:
            print(e)
            sys.exit()