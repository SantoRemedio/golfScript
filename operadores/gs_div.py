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
# condition check passes the current top of divisor is collected into an array.
#
# 0 1 {100<} { .@+ } / -> 89 [1 1 2 3 5 8 13 21 34 55 89]
#
# Each. Execute a block over all elements.
#
# [1 2 3]{1+}/ -> 2 3 4

from operadores.gs_dup import gs_dup
from tipos import Integer, Block, Array, String


def gs_div_int_array(stack, valor, divisor):
    #  [1 2 3 4 5] 2 / => [[1 2] [3 4] [5]]
    lista = valor.name
    tamano = int(divisor)
    nva = []
    for i in range(0, len(lista), tamano):
        nva.append(Array(lista[i:i + tamano]))
    stack.append(Array(nva))

def gs_div_array_array(stack, valor, divisor):
    # valor divisor /
    # [ 0 1 2 3 4 5 3 2 3 6] [2 3]/ -> [[0 1] [4 5 3] [6]]
    # Corta la lista en donde se encuentra la sublista
    ancho = len(divisor)
    lista = []
    i = idx_prev = 0
    while i < len(valor):
        #   Compara lista python
        if valor[i:i + ancho] == divisor.name:
            lista.append(Array(valor[idx_prev:i]))
            i = i + ancho
            idx_prev = i
        else:
            i += 1
    if idx_prev < len(valor):
        lista.append(Array(valor[idx_prev:i]))
    stack.append(Array(lista))

def gs_div_block_block(stack, valor, divisor):
    from evaluador import evaluar
    accion = divisor
    condicion = valor
    lista = []
    while True:
        gs_dup(stack)
        evaluar(condicion)
        cond = stack.pop()
        if cond:
            gs_dup(stack)
            divisor = stack.pop()
            lista.append(divisor)
            evaluar(accion)
        else:
            _ = stack.pop()
            break
    nvo = Array(lista)
    stack.append(nvo)


def gs_div(stack):
    divisor = stack.pop()
    valor = stack.pop()

    if isinstance(divisor, Integer):
        if isinstance(valor, Integer):
            #   1 / 2
            div = valor // divisor
            stack.append(div)
        elif isinstance(valor, Array):
            gs_div_int_array(stack, valor, divisor)
    elif isinstance(divisor, String):
        if isinstance(valor, String):
            #   Es tan simple como un split()
            lista = valor.name.split(divisor.name)
            lista = [String(x) for x in lista]
            stack.append(Array(lista))
    elif isinstance(divisor, Array):
        if isinstance(valor, Array):
            gs_div_array_array(stack, valor, divisor)
    elif isinstance(divisor, Block):
        if isinstance(valor, Block):
            gs_div_block_block(stack, valor, divisor)
        elif isinstance(valor, Array):
            from evaluador import evaluar
            accion = divisor
            for elemento in valor.name:
                stack.append(elemento)
                evaluar(accion)
    else:
        raise ValueError("Error en gs_div: Tipo de dato erroneo")

