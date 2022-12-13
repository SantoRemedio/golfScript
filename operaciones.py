# vars.py
# Implementa operadores y variables
# Los operadores se consideran variables asignadas
# con código ejecutable.
# Se recuperan mediante el diccionario `variables`

# Los string del fuente se representan internamente con cremillas
# incluidas.

from tipos import Block, String, Integer, Var, List, cero, uno

uno = Integer(1)

def evaluate(source):
    pass

def gs_coerce(a, b):
    mayor = max(a.precedence, b.precedence)
    a = a.coerce(mayor)
    b = b.coerce(mayor)
    return a, b

def gs_sum(stack):
    a = stack.pop()
    b = stack.pop()

    a, b = gs_coerce(a, b)
    if isinstance(a, Integer):
        stack.append(a + b)
    else:
        stack.append(b + a)


def gs_subtract(stack):
    a = stack.pop()
    b = stack.pop()
    a, b = gs_coerce(a, b)
    if isinstance(a, Integer):
        resta = b - a
    elif isinstance(a, List):
        lista = []
        for elemento in b:
            if elemento not in a:
                lista.append(elemento)
        resta = List(lista)

    stack.append(resta)

def gs_multiply(stack):
    from compiler import evaluate
    top = stack.pop()
    sig = stack.pop()

    if isinstance(top, Integer) and isinstance(sig, Integer):
        resultado = top * sig
        stack.append(resultado)
    elif isinstance(top, Integer) and isinstance(sig, Block):
        for _ in range(int(top)):
            evaluate(sig.name)
    elif isinstance(top, Integer) and isinstance(sig, List):
        lista = []
        for _ in range(int(top)):
            lista.extend(sig.name)
        stack.append(List(lista))
    elif isinstance(top, Integer) and isinstance(sig, String):
        stack.append(String(sig.name * int(top)))
    elif isinstance(top, String) and isinstance(sig, Integer):
        stack.append(String(top.name * int(sig)))
    elif isinstance(top, String) and isinstance(sig, List):
        lista = top.name.join(str(x) for x in sig.name)
        stack.append(String(lista))
    elif isinstance(top, List) and isinstance(sig, List):
        lista = []
        for x in sig:
            lista.append(x)
            lista.extend(top)
        stack.append(List(lista[:-1]))
    elif isinstance(top, String) and isinstance(sig, String):
        nvo = top.name.join(sig.name)
        stack.append(String(nvo))


def gs_div(stack):
    a = stack.pop()
    b = stack.pop()
    div = b // a
    stack.append(div)

def gs_power(stack):
    a = stack.pop()
    b = stack.pop()
    power = b ** a
    stack.append(power)

def gs_dec_1(stack):
    elemento = stack.pop()

    if isinstance(elemento, Integer):
        nvo = elemento - uno
        stack.append(nvo)
    elif isinstance(elemento, String):
        #  Caso concatenacion
        valor_byte = ord(elemento.pop(0))
        stack.append(elemento)
        stack.append(str(valor_byte))
    else:
        raise ValueError(f"Eror en gs_dec_1: Tipo desconocido {type(elemento)}")

def gs_inc_1(stack):
    elemento = stack.pop()

    if isinstance(elemento, Integer):
        stack.append(elemento + uno)
    elif isinstance(elemento, String):
        #  Caso concatenacion
        contenido = elemento.name
        valor_byte = ord(contenido[-1])
        stack.append(String(contenido[:-1]))
        stack.append(Integer(valor_byte))
    else:
        raise ValueError(f"Eror en gs_dec_1: Tipo desconocido {type(elemento)}")


def gs_chancho(stack):
    from compiler import evaluate
    elemento = stack.pop()
    if isinstance(elemento, Var):
        elemento = variables[elemento]

    if isinstance(elemento, Integer):
        stack.append(Integer(~elemento.name))
    elif isinstance(elemento, String):
        evaluate(elemento.name)
    elif isinstance(elemento, Block):
        evaluate(elemento.name)
    elif isinstance(elemento, List):
        stack.extend(elemento.name)
    else:
        raise ValueError(f"Error en gs_chancho: elemento desconocido {elemento}")

def gs_pop(stack):
    if stack:
        stack.pop()

def gs_dup_n(stack):
    #   Duplica en n-esimo elemento del stack (index 0).
    #   n se saca del stack.
    top = stack.pop()

    if isinstance(top, Integer):
        stack.append(stack[-int(top) - 1])
    elif isinstance(top, String):
        nvo = String(''.join(sorted(top.name)))
        stack.append(nvo)

def gs_dup(stack):
    stack.append(stack[-1])

def gs_rotate(stack):
    #   Rota los tres elementos al tope del stack
    #   A B C -> B C A
    3
    if len(stack) > 2:
        stack[-1], stack[-2], stack[-3] = stack[-3], stack[-1], stack[-2]
    else:
        raise ValueError("Error en rotate")


def gs_swap(stack):
    #   Intercambia los dos elementos al tope del stack
    if len(stack) > 1:
        stack[-1], stack[-2] = stack[-2], stack[-1]
    else:
        raise ValueError("Error en swap")

def gs_module(stack):
    a = stack.pop()
    b = stack.pop()
    stack.append(b % a)

def gs_not(stack):
    a = stack.pop()
    stack.append(cero if a else uno)

def gs_repr(stack):
    #TODO: cambiar cremillas simples por dobles
    a =  String(str(stack.pop()))
    stack.append(a)

# El diccionario variables contiene las definiciones de
# operadores y los valores de las variables.
variables = {
    Var('+'): gs_sum,
    Var(';'): gs_pop,
    Var('+'): gs_sum,
    Var('-'): gs_subtract,
    Var('*'): gs_multiply,
    Var('/'): gs_div,
    Var('?'): gs_power,
    Var(')'): gs_inc_1,
    Var('('): gs_dec_1,
    Var('~'): gs_chancho,
    Var('.'): gs_dup,
    Var('$'): gs_dup_n,
    Var('\\'): gs_swap,
    Var('@'): gs_rotate,
    Var('%'): gs_module,
    Var('!'): gs_not,
    Var('`'): gs_repr,
}

