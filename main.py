import sys
from compiler import evaluate

if __name__ == '__main__':
    if len(sys.argv) == 2:
        try:
            with open(sys.argv[1], "r") as fuente:
                evaluate(fuente.read())
        except:
            print("Archivo no existe")
    else:
        print("Formato: golfscript archivo.fuente")

