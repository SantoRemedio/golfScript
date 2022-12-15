#
#   Lee un archivo con expresiones y resultados del interprete oficial
#   y las compara contra resultados propios
#
#   Formato de cada línea:
#
#       pgma -> resultado
#
import sys
from evaluador import evaluar, stack, reset

archivo = sys.argv[1]
with open(archivo, "r") as tests:
    i = 0
    exitos = 0
    for linea in tests:
        if linea.startswith('#'):
            continue

        i += 1
        pgma, resultado = linea.strip().split("->")
        resultado = resultado.strip()
        reset()
        evaluar(pgma)
        oficial = str(stack)[1:-1]
        if oficial == resultado:
            exitos += 1
        else:
            print()
            print(f"{i}. {pgma} ")
            print("  R: ", oficial)
            print("  C: ", resultado)

    print(f"{exitos} exitos en {i} problemas ({int(100 * exitos / i)}%)")
