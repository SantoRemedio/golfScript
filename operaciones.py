# vars.py
# Implementa operadores y variables
# Los operadores se consideran variables asignadas
# con código ejecutable.
# Se recuperan mediante el diccionario `variables`

from tipos import Block, String, Integer, Var, Array, cero, uno, menos_uno


def evaluar(source):
    raise ValueError(f"Función no importa correctamente la función evaluar en {source}")


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
    elif isinstance(a, Array):
        lista = []
        for elemento in b:
            if elemento not in a:
                lista.append(elemento)
        resta = Array(lista)
    else:
        raise ValueError("gs_subtract: Tipo de dato erroneo")

    stack.append(resta)


def gs_multiply(stack):
    from evaluador import evaluar
    top = stack.pop()
    sig = stack.pop()

    if isinstance(top, Integer) and isinstance(sig, Integer):
        resultado = top * sig
        stack.append(resultado)
    elif isinstance(top, Integer) and isinstance(sig, Block):
        for _ in range(int(top)):
            evaluar(sig.name)
    elif isinstance(top, Integer) and isinstance(sig, Array):
        lista = []
        for _ in range(int(top)):
            lista.extend(sig.name)
        stack.append(Array(lista))
    elif isinstance(top, Integer) and isinstance(sig, String):
        stack.append(String(sig.name * int(top)))
    elif isinstance(top, String) and isinstance(sig, Integer):
        stack.append(String(top.name * int(sig)))
    elif isinstance(top, String) and isinstance(sig, Array):
        lista = top.name.join(str(x) for x in sig.name)
        stack.append(String(lista))
    elif isinstance(top, Array) and isinstance(sig, Array):
        lista = []
        for x in sig:
            lista.append(x)
            lista.extend(top)
        stack.append(Array(lista[:-1]))
    elif isinstance(top, String) and isinstance(sig, String):
        nvo = top.name.join(sig.name)
        stack.append(String(nvo))
    elif isinstance(top, Block) and isinstance(sig, Array):
        stack.extend(sig.name)
        for _ in range(len(sig.name) - 1):  # Aplicar el bloque n - 1 veces
            evaluar(top)
    elif isinstance(top, Block) and isinstance(sig, String):
        for letra in sig.name:
            stack.append(Integer(ord(letra)))
        for _ in range(len(sig.name) - 1):
            evaluar(top)
    else:
        raise ValueError("gs_multiply: Tipo de dato erroneo")


def gs_div(stack):
    a = stack.pop()
    b = stack.pop()

    if isinstance(a, Integer) and isinstance(b, Integer):
        #   1 / 2
        div = b // a
        stack.append(div)
    elif isinstance(a, Integer) and isinstance(b, Array):
        #  [1 2 3 4 5] 2 / => [[1 2] [3 4] [5]]
        lista = b.name
        tamano = int(a)
        nva = []
        for i in range(0, len(lista), tamano):
            nva.append(Array(lista[i:i + tamano]))
        stack.append(Array(nva))
    elif isinstance(a, Block) and isinstance(b, Block):
        from evaluador import evaluar
        accion = a
        condicion = b
        lista = []
        while True:
            gs_dup(stack)
            evaluar(condicion)
            top = stack.pop()
            val = 1 if top else 0
            if top:
#                stack.append(top)
                evaluar(accion)
                top = stack.pop()
                lista.append(top)
            else:
                break
        nvo = Array(lista)
        stack.append(nvo)


def gs_power(stack):
    a = stack.pop()
    b = stack.pop()
    if isinstance(a, Integer) and isinstance(b, Integer):
        power = b ** a
        stack.append(power)
    elif isinstance(a, Array):
        try:
            index = a.name.index(b)
            stack.append(Integer(index))
        except ValueError:
            stack.append(menos_uno)

def gs_or(stack):
    a = stack.pop()
    b = stack.pop()

    if isinstance(a, Integer) and isinstance(b, Integer):
        c = int(a) | int(b)
        stack.append(Integer(c))
    else:
        raise ValueError("gs_or: Tipo de dato erroneo")

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
    elif isinstance(elemento, Array):
        stack.append(Array(elemento.name[1:]))
        stack.append(elemento.name[0])
    else:
        raise ValueError(f"Eror en gs_dec_1: Tipo de dato erroneo")


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
    elif isinstance(elemento, Array):
        stack.append(Array(elemento.name[:-1]))
        stack.append(elemento.name[-1])
    else:
        raise ValueError(f"Eror en gs_dec_1: Tipo de dato erroneo")


def gs_chancho(stack):
    from evaluador import evaluar
    elemento = stack.pop()
    if isinstance(elemento, Var):
        elemento = variables[elemento]

    if isinstance(elemento, Integer):
        stack.append(Integer(~elemento.name))
    elif isinstance(elemento, String):
        evaluar(elemento.name)
    elif isinstance(elemento, Block):
        evaluar(elemento.name)
    elif isinstance(elemento, Array):
        stack.extend(elemento.name)
    else:
        raise ValueError(f"gs_chancho: Tipo de dato erroneo")


def gs_pop(stack):
    if len(stack):
        stack.pop()
    else:
        raise ValueError("gs_pop: Stack vacio")


def gs_dup_n(stack):
    #   Duplica en n-esimo elemento del stack (index 0).
    #   n se saca del stack.
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


def gs_dup(stack):
    stack.append(stack[-1])


def gs_rotate(stack):
    #   Rota los tres elementos al tope del stack
    #   A B C @ -> B C A
    if len(stack) > 2:
        stack[-1], stack[-2], stack[-3] = stack[-3], stack[-1], stack[-2]
    else:
        raise ValueError("gs_rotate: stack tiene menos de 3 elementos")


def gs_swap(stack):
    #   Intercambia los dos elementos al tope del stack
    if len(stack) > 1:
        stack[-1], stack[-2] = stack[-2], stack[-1]
    else:
        raise ValueError("gs_swap: stack tiene menos de dos elementos")


def gs_module(stack):
    a = stack.pop()
    b = stack.pop()
    if isinstance(a, Integer) and isinstance(b, Integer):
        nvo = b % a
        stack.append(nvo)
    else:
        raise ValueError("gs_module: Tipo dato erroneo")


def gs_not(stack):
    a = stack.pop()
    stack.append(cero if a else uno)


def gs_repr(stack):
    elemento = stack.pop()
    a = String(str(elemento))
    stack.append(a)


def gs_greater(stack):
    top = stack.pop()
    sig = stack.pop()
    if type(top) == type(sig):
        stack.append(uno if sig > top else cero)
    elif isinstance(top, Integer) and isinstance(sig, String):
        st = String(sig.name[int(top):])
        stack.append(st)
    elif isinstance(top, Integer) and isinstance(sig, Array):
        lista = Array(sig.name[int(top):])
        stack.append(lista)
    elif isinstance(top, Integer) and isinstance(sig, Block):
        from evaluador import tokenizar
        source = str(sig)[1:-1][int(top):]
        for elemento in tokenizar('{' + source + '}'):
            stack.append(elemento)


def gs_less(stack):
    top = stack.pop()
    sig = stack.pop()
    if type(top) == type(sig):
        stack.append(uno if sig < top else cero)
    elif isinstance(top, Integer) and isinstance(sig, String):
        st = String(sig.name[:int(top)])
        stack.append(st)
    elif isinstance(top, Integer) and isinstance(sig, Array):
        lista = Array(sig.name[:int(top)])
        stack.append(lista)
    elif isinstance(top, Integer) and isinstance(sig, Block):
        from evaluador import tokenizar
        source = str(sig)[1:-1][:int(top)]
        for elemento in tokenizar('{' + source + '}'):
            stack.append(elemento)

def gs_equal(stack):
    a = stack.pop()
    b = stack.pop()

    if type(a) == type(b):
        val = uno if a == b else cero
        stack.append(val)
    elif isinstance(a, Integer) and isinstance(b, Array):
        try:
            val = b[int(a)]
            stack.append(val)
        except IndexError:
            #   Si el indice está fuera de rango, no
            #   poner nada en el stack.
            pass

def gs_bitwise_xor(stack):
    top = stack.pop()
    sig = stack.pop()
    if type(top) == type(sig):
        elemento = sig ^ top
        stack.append(elemento)


def gs_bitwise_and(stack):
    top = stack.pop()
    sig = stack.pop()
    if type(top) == type(sig):
        elemento = top & sig
        stack.append(elemento)


def gs_if(stack):
    #
    #     valor_if valor_true valor_false if
    #
    from evaluador import evaluar
    valor_false = stack.pop()
    valor_true = stack.pop()
    valor_if = stack.pop()

    if valor_if:
        evaluar(valor_true)
    else:
        evaluar(valor_false)


def gs_do(stack):
    #
    #   elemento bloque do
    #
    # Ejecuta el bloque, saca tope del stack; si
    # es true, sigue.
    from evaluador import evaluar

    bloque = stack.pop()
    while True:
        evaluar(bloque)
        valor_if = stack.pop()
        if not valor_if:
            break


def gs_while(stack):
    #
    #   elemento bloque-ejecutar bloque-condicion while
    #
    # Ejecuta el bloque-condicion y saca un valor del stack.
    # Si es True, ejecuta el bloque-ejecutar.
    # Si es False, reinserta valor y termina
    from evaluador import evaluar

    bloque_condicion = stack.pop()
    bloque_ejecutar = stack.pop()
    while True:
        evaluar(bloque_condicion)
        valor_if = stack.pop()
        if valor_if:
            evaluar(bloque_ejecutar)
        else:
            stack.append(valor_if)
            break


def gs_until(stack):
    #
    #   elemento bloque-ejecutar bloque-condicion until
    #
    # Ejecuta el bloque-condicion y saca un valor del stack.
    # Si es True, ejecuta el bloque-ejecutar.
    # Si es False, reinserta valor y termina
    from evaluador import evaluar

    bloque_condicion = stack.pop()
    bloque_ejecutar = stack.pop()
    while True:
        evaluar(bloque_condicion)
        valor_if = stack.pop()
        if valor_if:
            stack.append(valor_if)
            break
        else:
            evaluar(bloque_ejecutar)


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


# El diccionario variables contiene las definiciones de
# operadores y los valores de las variables.
variables = {}


def reset_variables():
    global variables

    variables = {
        Var('+'): gs_sum,
        Var(';'): gs_pop,
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
        Var('>'): gs_greater,
        Var('<'): gs_less,
        Var('='): gs_equal,
        Var('^'): gs_bitwise_xor,
        Var('&'): gs_bitwise_and,
        Var(','): gs_size,
        Var('|'): gs_or,
        Var('if'): gs_if,
        Var('do'): gs_do,
        Var('while'): gs_while,
        Var('until'): gs_until,
    }


reset_variables()
