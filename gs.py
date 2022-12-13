import sys
from compiler import evaluate, reset

if __name__ == '__main__':
    if len(sys.argv) == 2:
        print(evaluate(sys.argv[1]))
    else:
        print("Interprete golfScript 0.1 - Dic/2022 - Candid Moe")
        print("Esta versión acepta el código en http://golfscript.com/golfscript/builtin.html")
        while True:
            try:
                pgma = input(">")
                reset()
                print(evaluate(pgma))
            except:
                pass

