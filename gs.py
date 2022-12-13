#
#   REPL del interprete de golfScript
#
import sys
from evaluador import evaluar, reset, variables, modo_debug
from tipos import Var

if __name__ == '__main__':
    print("Interprete golfScript 0.1 - Dic/2022 - Candid Moe")
    print("Esta versión acepta el código en http://golfscript.com/golfscript/builtin.html")
    print("REPL sin historia ni editor. CTRL-C para terminar. help para ayuda")
    print("Operadores: ", list(variables.keys()))

    if len(sys.argv) == 2:
        pgma = sys.argv[1]
        print(f">{pgma}")
    else:
        pgma = input(">")

    while True:
        try:
            if pgma == "help":
                print("reset: reinicia el interprete")
                print("vars: muestra la tabla de variables")
                print("inspect x: muestra valor de x")
                print("quit: termina la ejecución")
                print("debug: entra/sale de debug")
                print("CTRL-C para terminar")
            elif pgma == "reset":
                reset()
            elif pgma == "quit":
                break
            elif pgma == "debug":
                modo_debug = not modo_debug
            elif pgma == "vars":
                for k, v in variables.items():
                    print(k, v)
            elif pgma.startswith("inspect "):
                _, nombre = pgma.split()
                print(f"{nombre}={variables[Var(nombre)]}")
            else:
                print(evaluar(pgma))
            pgma = input(">")
        except KeyboardInterrupt:
            break;
        except:
            pass

