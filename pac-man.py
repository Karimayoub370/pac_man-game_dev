try:
    import sys
    from parser import Parser
    
except BaseException as e:
    print(e)
    sys.exit()

class ParsingError(Exception):
    ...
class Runner():
    def main(self):
        if len(sys.argv) != 2:
            raise ParsingError("Must 2 argument")
        parser = Parser(sys.argv[1])
        parser.parse()
if __name__=="__main__":
    try:
        run = Runner()
        run.main()
    except ParsingError as e:
        print(e)