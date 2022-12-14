#
#   REPL del interprete de golfScript
#
import sys
from evaluador import evaluar, reset, variables, stack
from tipos import Var

if __name__ == '__main__':
    modo_debug = False
    reset()
    
    print("Interprete golfScript 0.3 - Dic/2022 - Candid Moe")
    print("Esta versión acepta el código en http://golfscript.com/golfscript/builtin.html")
    print("REPL sin historia ni editor. CTRL-C para terminar. help para ayuda")
    print("Operadores: ", list(variables.keys()))

    if len(sys.argv) == 2:
        #pgma = sys.argv[1]
        #print(f">{pgma}")
        with open(sys.argv[1], "r") as inp:
            pgma = inp.read()
    else:
        pgma = input(">")

    while True:
        try:
            if pgma == "help":
                print("reset: reinicia el interprete")
                print("clear: limpia el divisor")
                print("vars: muestra la tabla de variables")
                print("inspect x: muestra valor de x")
                print("debug: entra/sale de debug")
                print("quit: termina la ejecución")
                print("CTRL-C para terminar")
            elif pgma == "reset":
                reset()
            elif pgma == "quit":
                break
            elif pgma == "clear":
                stack.reset()
            elif pgma == "debug":
                modo_debug = not modo_debug
            elif pgma == "vars":
                for k, v in variables.items():
                    print(k, v)
            elif pgma.startswith("inspect "):
                _, nombre = pgma.split()
                print(f"{nombre}={variables[Var(nombre)]}")
            else:
                print(evaluar(pgma, modo_debug))
            pgma = input(">")
        except KeyboardInterrupt:
            break
        except Exception:
            pass
