import sys
import random
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
                    if line == "" or line.startswith('#') or line.startswith('//'):
                        continue
                    if  line:
                        res[i] = line
                        i += 1
            return res
        except Exception as e:
            print(e)
            sys.exit()
    def keys_parse(self, init_parse:dict[int:str])->dict[str:Any]:
        res:dict[str:Any] = {
                    "highscore_filename": "highscore.txt",
                    "levels": [
                        {
                            "width": random.randint(10, 30),
                            "height": random.randint(10, 30)
                        }
                        for _ in range(10)
                    ],
                    "lives": 3,
                    "pacgum": 42,
                    "points_per_pacgum": 10,
                    "points_per_super_pacgum": 50,
                    "points_per_ghost": 200,
                    "seed": 42,
                    "level_max_time": 90
                    }
        for k,v in init_parse.items():
            if v == '{' or v == '}':
                continue
            if ":" in v:
                v1,v2 = k.split(":",1)
                if v1 == "highscore_filename":
                    if v2.endswith(".txt"):
                        res[v1] = v2
                    else:
                        print(f"Format not accepted in line {k}: missing '.txt' in {v2}",file=sys.stderr)
                elif v1 == "lives" or v1 == "pacgum" or v1 == "points_per_pacgum" or v1 == "points_per_super_pacgum" or v1 == "points_per_ghost" or v1 == "seed" or v1 == "level_max_time":
                    try:
                        tmp:int = int(v2)
                        res[v1] = tmp
                    except ValueError:
                        print(f"Format not accepted in line {k}: missing 'int value' in {v2}",file=sys.stderr)
                elif v1 == "levels":
                    try:
                        tmp:list[dict[str:int]] = list(v2)
                    except ValueError:
                         print(f"Format not accepted in line {k}: missing valid levels",file=sys.stderr)
                else:
                    print(f"Format not accepted in line {k}: '{v1}' key is not accepted",file=sys.stderr)
            else:
                print(f"Format not accepted in line {k}: missing ':'",file=sys.stderr)
        return res