# Operator *
# args: order
# * can mean many things, the choice of behavior is determined by the type.
# Multiplication
#
#  2 4* -> 8
#
# Execute a block a certain number of times, note the order of operands does
# not matter because these are automatically ordered first.
#
#  2 {2*} 5* -> 64
#
# Array/string repeat
#
# [1 2 3]2* -> [1 2 3 1 2 3]
# 3'asdf'* -> "asdfasdfasdf"
#
# Join
#
# [1 2 3]','* -> "1,2,3"
# [1 2 3][4]* -> [1 4 2 4 3]
# 'asdf'' '* -> "a s d f"
# [1 [2] [3 [4 [5]]]]'-'* -> "1-\002-\003\004\005"
# [1 [2] [3 [4 [5]]]][6 7]* -> [1 6 7 2 6 7 3 [4 [5]]]
#
# Fold. Symbol choice for fold comes from ruby golf trick: eval [1,2,3,4,5]*"+".
#
# [1 2 3 4]{+}* -> 10
# 'asdf'{+}* -> 414

from tipos import Integer, Block, Array, String, GSType


def gs_multiply(stack):
    from evaluador import evaluar
    top = stack.pop()
    sig = stack.pop()

    valido = True

    if isinstance(top, Integer):
        if isinstance(sig, Integer):
            resultado = top * sig
            stack.append(resultado)
        elif isinstance(sig, Block):
            for _ in range(int(top)):
                evaluar(sig.name)
        elif isinstance(sig, Array):
            lista = []
            for _ in range(int(top)):
                lista.extend(sig.name)
            stack.append(Array(lista))
        elif isinstance(sig, String):
            stack.append(String(sig.name * int(top)))
        else:
            valido = False

    elif isinstance(top, String):
        if isinstance(sig, Integer):
            stack.append(String(top.name * int(sig)))
        elif isinstance(sig, Array):
            lista = top.name.join(str(x) for x in sig.name)
            stack.append(String(lista))
        elif isinstance(sig, String):
            nvo = top.name.join(sig.name)
            stack.append(String(nvo))
        else:
            valido = False

    elif isinstance(top, Array):
        if isinstance(sig, Integer):
            lista = top.name * int(sig)
            stack.append(Array(lista))
        elif isinstance(sig, String):
            car = sig.name
            lista = car.join(str(x) for x in top.name)
            stack.append(String(lista))
        elif isinstance(sig, Array):
            lista = []
            for x in sig:
                lista.append(x)
                lista.extend(top)
            stack.append(Array(lista[:-1]))
        else:
            valido = False

    elif isinstance(top, Block):
        if isinstance(sig, Array):
            stack.extend(sig.name)
            for _ in range(len(sig.name) - 1):  # Aplicar el bloque n - 1 veces
                evaluar(top)
        elif isinstance(sig, String):
            for letra in sig.name:
                stack.append(Integer(ord(letra)))
            for _ in range(len(sig.name) - 1):
                evaluar(top)
        elif issubclass(type(sig), GSType):
            # Para Integer y String, aplicar el bloque.
            evaluar(top)
        else:
            valido = False
    else:
        valido = False

    if not valido:
        raise ValueError("gs_multiply: Tipo de dato erroneo")
