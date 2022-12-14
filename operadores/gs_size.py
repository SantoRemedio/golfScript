# Operator ,
# args: 1 or 2
# Create an array of n elements starting at 0.
#
#  10, -> [0 1 2 3 4 5 6 7 8 9]
#
# Get the size of an array
#
#  10,, -> 10
#
# If the argument is a block, take another argument and perform a map, select all original elements in the array whose result was true.
#
#  10,{3%}, -> [1 2 4 5 7 8]
from tipos import Integer, Block, Array, String


def gs_size(stack):
    from evaluador import evaluar
    a = stack.pop()

    if isinstance(a, Integer):
        lista = [Integer(x) for x in range(int(a))]
        nvo = Array(lista)
        stack.append(nvo)
    elif isinstance(a, Array):
        nvo = Integer(len(a))
        stack.append(nvo)
    elif isinstance(a, Block):
        b = stack.pop()
        lista = []
        for elemento in b:
            stack.append(elemento)
            evaluar(a)
            val = stack.pop()
            if val:
                lista.append(elemento)
        nvo = Array(lista)
        stack.append(nvo)
    else:
        raise ValueError("gs_size: Tipo de datos erroneo")
