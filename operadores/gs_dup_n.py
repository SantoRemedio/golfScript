# Operator $
# args: 1 or 2
# If arg is an integer, copys nth item from top of $tack.
#
# 1 2 3 4 5  1$ -> 1 2 3 4 5 4
#
# For arrays (including strings) a $ort is performed.
#
# 'asdf'$ -> "adfs"
#
# For blocks, sort by some mapping.
#
#  [5 4 3 1 2]{-1*}$ -> [5 4 3 2 1]
from tipos import Integer, Block, Array, String

def gs_dup_n(stack):
    #   Duplica en n-esimo elemento del divisor (index 0).
    #   n se saca del divisor.
    top = stack.pop()

    if isinstance(top, Integer):
        stack.append(stack[-int(top) - 1])
    elif isinstance(top, String):
        #   Para strings, hace un sort de los caracteres.
        nvo = String(''.join(sorted(top.name)))
        stack.append(nvo)
    elif isinstance(top, Block):
        from evaluador import evaluar
        #   Los elementos deben ordenarse aplicando
        #   a cada elemento el bloque en top
        lista = stack.pop()
        to_sort = []
        for elemento in lista:
            stack.append(elemento)
            evaluar(top)
            valor = stack.pop()
            to_sort.append((valor, elemento))
        nvo = [original for _, original in sorted(to_sort)]
        stack.append(Array(nvo))
    elif isinstance(top, Array):
        try:
            nvo = sorted(top.name)
            stack.append(Array(nvo))
        except Exception as e:
            print(f"Error: {e}")
    else:
        raise ValueError("gs_dup_n: Tipo de dato erroneo")

