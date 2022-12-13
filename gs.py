import sys
from compiler import evaluate

if __name__ == '__main__':
    if len(sys.argv) == 2:
        print(evaluate(sys.argv[1]))
    else:
        print('Formato: python gs.py "archivo.fuente"')

