import re

from tipos import Block, Var, Integer, String, List, colon
from operaciones import variables
import types
import typing

patron = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*|;|'(?:\\.|[^'])*'?|[~@\\%\.{};+]|-?[0-9]+|#[^\n\r]*|\S")
                    #|"(?:\\.|[^"])*"?|-?[0-9]+|)


def lexer(source):
    #   Divide el programa fuente en lexemas
    #   Funcion generadora; marca de fin es None
    for linea in source.split('\n'):
        for parte in patron.findall(linea):
            if parte[0] == "'":
                word = String(parte[1:-1])
            elif parte.isdecimal():
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
    lexema = next(source)
    while lexema is not None:
        # Examina un lexema e intenta convertirlo en
        # un token.
        token = None

        if lexema == '{':
            block = []
            lexema = next(source)
            while lexema != '}':
                block.append(lexema)
                lexema = next(source)
            token = Block(block)
        elif lexema == '[':
            stack_listas.append([])
        elif lexema == ']':
            if len(stack_listas) == 1:
                token = List(stack_listas.pop())
            else:
                sublista = stack_listas.pop()
                stack_listas[-1].append(List(sublista))
        elif stack_listas:
            stack_listas[-1].append(lexema)
        else:
            token = lexema

        if token is not None:
            yield token
        lexema = next(source)


stack = List([])

def evaluate(source_code):
    #   Recibe un código a ejecutar.
    #   El código puede venir como string (formato fuente)
    #   o ya tokenizado.
    #   El stack global de golfScript.
    #   Solo contiene elementos inmutables

    if isinstance(source_code, str):
        source = tokenizador(source_code)
    else:
        source = source_code


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
                        evaluate(variables[elemento].name)
                    else:
                        #  el valor al stack
                        stack.append(variables[elemento])
                else:
                    stack.append(elemento)

                elemento_prev = elemento
            except Exception as e:
                print(f"Error en evaluate: {e}")
                print(type(elemento))
                print(elemento)
                print(source_code)
                print(elemento.__hash__())
    return stack

def reset():
    global stack
    stack.reset()
