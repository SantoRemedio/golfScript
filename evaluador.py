#
#   evaluador.py
#
#   Este es el módulo principal del interprete.

#   La función evaluar() recibe un programa en código
#   fuente u otro formato, y lo ejecuta contra un divisor
#   y tabla de valores permanentes, para poder ejecutar
#   programas en sucesión
#
#   Un programa en código fuente es divididoo en un stream
#   de palabras por la función lexer(). La función tokenizar()
#   procesa el stream produciendo elementos del lenguaje:
#   - Integer
#   - String
#   - Block
#   - Array
#   Todos los elementos son inmutables.

import re

from tipos import Block, Var, Integer, String, colon, GSType, start_list
from stack import Stack
from operaciones import variables, reset_variables, gs_close
import types

#   Este es el patrón oficial para reconoce golfScript
patron = re.compile(
    r"([a-zA-Z_][a-zA-Z0-9_]*|;|'(?:\\.|[^'])*'?|\"(?:\\.|[^\"])*\"?|[~@\\%\.{};+]|-?[0-9]+|#[^\n\r]*|\S)")


#
# El stack del script.
# El tope del stack está a la derecha (indice mayor).
# En todas las representaciones del stack, el tope estará a la derecha
# El stack siempre contendra exclusivamente Integer, String, Array y Block.
#
stack = Stack([])

def evaluar(source_code, modo_debug=False):
    #   Recibe un código a ejecutar:
    #   - Codigo fuente.
    #   - Iterables
    #   - Escalares
    #   El código puede venir como string (formato fuente)
    #   o ya tokenizado.

    if isinstance(source_code, str):
        source = tokenizar(source_code)
    elif hasattr(source_code, '__iter__'):
        source = source_code
    else:
        source = [source_code]

    elemento_prev = None
    for elemento in source:
        if modo_debug:
            print(stack, elemento)

        #   Un elemento None marca el fin del código.
        if elemento is None:
            #   Cerrar todos los "[" que hayan quedado abiertos.
            try:
                while start_list in stack:
                    gs_close(stack)
            except IndexError:
                pass
            break

        try:
            if elemento == colon:  # 1:a  Asigna el valor 1 a la variable a
                pass  # Esperar lo que viene después
            elif elemento_prev == colon:
                #   elemento es el nombre de la variable.
                variables[elemento] = stack.peek(0)  # Extraer valor del stack sin modificarlo
            elif elemento in variables:
                if isinstance(variables[elemento], types.FunctionType):
                    variables[elemento](stack)  # Ejecutar un operador definido por una función
                elif isinstance(variables[elemento], Block):
                    evaluar(variables[elemento].name)  # Ejecutar el bloque completo.
                else:
                    #  Colocar en el stack el valor de la variable.
                    stack.append(variables[elemento])
            else:
                #   Cualquier otra cosa, al stack
                stack.append(elemento)

            elemento_prev = elemento
        except Exception as e:
            print(f"Error en evaluar: {e}")
            print(f"Tipo del elemento: {type(elemento)}")
            print(f"Elemento: {elemento}")
            print(f"Fuente:  {source_code}")
    return stack


def tokenizar(pgma):
    #  Recibe las partes elementales del pgma y los
    #  convierte a los tipos adecuados

    stack_contenedores = []

    source = lexer(pgma)
    word = next(source)

    while word is not None:
        # Examina un word e intenta convertirlo en
        # un token.
        token = None

        if word == '{': # Inicio de un bloque
            stack_contenedores.append(Block([]))
        elif not issubclass(type(word), GSType) and word == '}':
            #   Se termino el contenedor, que quedó al tope del stack
            if len(stack_contenedores) == 1:
                #   Esta es contenedor de primer nivel
                token = stack_contenedores.pop()
            else:
                #   Este es un subcontenedor.
                #   Agregarlo como elemento en el contenedor superior.
                sub = stack_contenedores.pop()
                stack_contenedores[-1].append(sub)
        elif stack_contenedores:
            #   Si el stack_lista no está vacio, entonces
            #   estamos leyendo elementos de una lista.
            stack_contenedores[-1].append(word)
        else:
            #   Fuera de un contenedor
            token = word

        if token is not None:
            yield token

        word = next(source)

    yield None


def lexer(source):
    #   Divide el programa fuente en palabras.
    #   Funcion generadora; marca de fin es None
    for linea in source.split('\n'):
        for parte in patron.findall(linea):
            if parte[0] == "#":  # El resto es comentario
                continue
            elif parte[0] in "'\"":  # Acepta string delimitados con comillas simples y dobles
                #   Convierte enteros y strings a medida
                #   que los encuentra.
                #   No he logrado refactorizar esta parte para moverla
                #   a tokenizar().
                if parte[0] == "'":
                    texto = parte[1:-1].replace(r"\'", "'")
                else:
                    texto = bytes(parte[1:-1], "utf-8").decode("unicode_escape")
                word = String(texto)
            elif parte.isdecimal() or (parte[0] in '+-' and parte[1:].isdecimal()):
                word = Integer(int(parte))
            elif parte[0] not in '{}':
                #   Los nombres de variable se registran de inmediato.
                word = Var(parte)
                if word not in variables:
                    variables[word] = None
            else:
                #   Algunos palabras se entregan como texto, ya
                #   que son entidades complejas.
                #   Incluyen los {}
                word = parte

            yield word
    yield None

def reset():
    #
    #   Reinicia el estado para permitir la correcta
    #   ejecución de los tests unitarios.
    #
    global stack

    stack.reset()
    reset_variables()

    #   Operadores definidos en base a golfScript
    #   (mejor sería cargarlos de un archivo ...)
    #evaluar("1 2 [\]")
    evaluar(r"{\!!{!}*}:xor;")
    evaluar(r"{1$if}:and;")
    evaluar(r"{1$\if }:or;")
    evaluar(r"{print n print}:puts;")
    evaluar(r"{`puts}:p;")
    evaluar(r'{"\n"}:n;')
