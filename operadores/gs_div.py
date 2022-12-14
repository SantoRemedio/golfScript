# Operator /
# args: order
# / can also mean many things based on operand types, usually the opposite of *
# Division
#
# 7 3 / -> 2
#
# Split around matches with a second array
#
# [1 2 3 4 2 3 5][2 3]/ -> [[1] [4] [5]]
# 'a s d f'' '/ -> ["a" "s" "d" "f"]
#
# Split into groups of a specified size
#
# [1 2 3 4 5] 2/ -> [[1 2] [3 4] [5]]
#
# Unfold, a slightly complicated function. It is pretty much a while loop except
# that before each condition test, the top of stack is duplicated, and if that
# condition check passes the current top of stack is collected into an array.
#
# 0 1 {100<} { .@+ } / -> 89 [1 1 2 3 5 8 13 21 34 55 89]
#
# Each. Execute a block over all elements.
#
# [1 2 3]{1+}/ -> 2 3 4

from operadores.gs_dup import gs_dup
from tipos import Integer, Block, Array


def gs_div(stack):
    a = stack.pop()
    b = stack.pop()

    if isinstance(a, Integer):
        if isinstance(b, Integer):
            #   1 / 2
            div = b // a
            stack.append(div)
        elif isinstance(b, Array):
            #  [1 2 3 4 5] 2 / => [[1 2] [3 4] [5]]
            lista = b.name
            tamano = int(a)
            nva = []
            for i in range(0, len(lista), tamano):
                nva.append(Array(lista[i:i + tamano]))
            stack.append(Array(nva))
    elif isinstance(a, Array):
        if isinstance(b, Array):
            # b a /
            # [ 0 1 2 3 4 5 3 2 3 6] [2 3]/ -> [[0 1] [4 5 3] [6]]
            # Corta la lista en donde se encuentra la sublista
            ancho = len (a)
            lista = []
            i = idx_prev = 0
            while i < len(b):
                #   Compara lista python
                if b[i:i+ancho] == a.name:
                    lista.append(Array(b[idx_prev:i]))
                    i = i + ancho
                    idx_prev = i
                else:
                    i += 1
            if idx_prev < len(b):
                lista.append(Array(b[idx_prev:i]))
            stack.append(Array(lista))
    elif isinstance(a, Block) and isinstance(b, Block):
        from evaluador import evaluar
        accion = a
        condicion = b
        lista = []
        while True:
            gs_dup(stack)
            evaluar(condicion)
            top = stack.pop()
            if top:
                #                stack.append(top)
                evaluar(accion)
                top = stack.pop()
                lista.append(top)
            else:
                break
        nvo = Array(lista)
        stack.append(nvo)


