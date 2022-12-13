import re

from tipos import Block, Var, Integer, String, List, colon
from operaciones import variables, reset_variables
import types
import typing

patron = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*|;|'(?:\\.|[^'])*'?|[~@\\%\.{};+]|-?[0-9]+|#[^\n\r]*|\S")
                    #|"(?:\\.|[^"])*"?|-?[0-9]+|)

#
# El stack del script.
# El tope del stack está a la derecha (indice mayor).
# En todas las representaciones del stack, el tope estará a la derecha
#
stack = List([])

def evaluar(source_code):
    #   Recibe un código a ejecutar:
    #   - Codigo fuente.
    #   - Iterables
    #   - Escalares
    #   El código puede venir como string (formato fuente)
    #   o ya tokenizado.
    #   El stack global de golfScript.
    #   Solo contiene elementos inmutables

    if isinstance(source_code, str):
        source = tokenizador(source_code)
    elif hasattr(source_code, '__iter__'):
        source = source_code
    else:
        source = [source_code]

    elemento_prev = None
    for elemento in source:
        if elemento is not None:
            try:
                if elemento == colon:
                    pass    # Esperar lo que viene después
                elif elemento in variables:
                    if elemento_prev == colon:
                        variables[elemento] = stack[-1]    # Extraer valor del stack sin modificarlo
                    elif isinstance(variables[elemento], types.FunctionType):
                        variables[elemento](stack)
                    elif isinstance(variables[elemento], Block):
                        evaluar(variables[elemento].name)
                    else:
                        #  el valor al stack
                        stack.append(variables[elemento])
                else:
                    stack.append(elemento)

                elemento_prev = elemento
            except Exception as e:
                print(f"Error en evaluar: {e}")
                print(type(elemento))
                print(elemento)
                print(source_code)
                print(elemento.__hash__())
    return stack

def lexer(source):
    #   Divide el programa fuente en lexemas
    #   Funcion generadora; marca de fin es None
    for linea in source.split('\n'):
        for parte in patron.findall(linea):
            if parte[0] == "#":  # El resto es comentario
                continue
            elif parte[0] == "'":
                word = String(parte[1:-1])
            elif parte.isdecimal() or (parte[0] in '+-' and parte[1:].isdecimal()):
                word = Integer(int(parte))
            elif parte[0] not in '[]{}':
                word = Var(parte)
                if word not in variables:
                    variables[word] = None
            else:
                #   Algunos lexemas se entregan como texto, ya
                #   que son entidades complejas.
                #   Incluyen los []{}
                word = parte

            yield word
    yield None

def tokenizador(pgma):
    #  Recibe las partes elementales del pgma y los
    #  convierte a los tipos adecuados

    stack_listas = []
    source = lexer(pgma)
    word = next(source)
    while word is not None:
        # Examina un word e intenta convertirlo en
        # un token.
        token = None

        if word == '{':
            #   Comienza un bloque;
            #   Bloque se lee completo aquí
            block = []
            word = next(source)
            while word != '}':
                block.append(word)
                word = next(source)
            token = Block(block)
        elif word == '[':
            #   Comienza una nueva lista, posiblemente anidad
            #   Partimos con una lista vacia agregada en el stack
            stack_listas.append([])
        elif word == ']':
            #   Se termino la lista, que quedó al tope del stack
            if len(stack_listas) == 1:
                #   Esta es una lista de primer nivel.
                token = List(stack_listas.pop())
            else:
                #   Esta es una sublista.
                #   Agregarla como elemento en la lista superior.
                sublista = stack_listas.pop()
                stack_listas[-1].append(List(sublista))
        elif stack_listas:
            #   Si el stack_lista no está vacio, entonces
            #   estamos leyendo elementos de una lista.
            stack_listas[-1].append(word)
        else:
            #   Fuera de una lista.
            token = word

        if token is not None:
            yield token
        word = next(source)



def reset():
    #
    #   Reinicia el estado para permitir la correcta
    #   ejecución de los tests unitarios.
    #
    global stack
    stack.reset()
    reset_variables()
