# vars.py
# Implementa operadores y variables
# Los operadores se consideran variables asignadas
# con código ejecutable.
# Se recuperan mediante el diccionario `variables`
import random

from tipos import Block, String, Integer, Var, Array, cero, uno, menos_uno
from operadores.gs_multiply import gs_multiply
from operadores.gs_div import gs_div
from operadores.gs_dup import gs_dup
from operadores.gs_dup_n import gs_dup_n
from operadores.gs_size import gs_size


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


def gs_power(stack):
    potencia = stack.pop()
    base = stack.pop()

    valido = True

    if isinstance(potencia, Integer) and isinstance(base, Integer):
        power = base ** potencia
        stack.append(power)
    elif isinstance(potencia, Array):
        #   [6 7][1 2 3 [6 7]]? No parece estar bien implementado
        #   en el interprete original, que retorna -1 en lugar de 4.
        try:
            index = potencia.name.index(base)
            stack.append(Integer(index))
        except ValueError:
            stack.append(menos_uno)
    elif isinstance(potencia, Block) and isinstance(base, Array):
        from evaluador import evaluar
        #   Buscar el primer indice que satisface la
        #   condición dada en el bloque
        idx = 1  # Indices son base 1 en golfScript
        for elemento in base.name:
            stack.append(elemento)
            evaluar(potencia)
            cond = stack.pop()
            if cond:
                break
            idx += 1
        #   Si se encontro, colocar el indice en el stack.
        #   Si no, no dejar nada
        if idx < len(base.name):
            stack.append(Integer(idx))
    else:
        valido = False

    if not valido:
        raise ValueError("Error en gs_module: Tipo de dato erroneo")

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


def gs_rotate(stack):
    #   Rota los tres elementos al tope del divisor
    #   A B C @ -> B C A
    if len(stack) > 2:
        stack[-1], stack[-2], stack[-3] = stack[-3], stack[-1], stack[-2]
    else:
        raise ValueError("gs_rotate: divisor tiene menos de 3 elementos")


def gs_swap(stack):
    #   Intercambia los dos elementos al tope del divisor
    if len(stack) > 1:
        stack[-1], stack[-2] = stack[-2], stack[-1]
    else:
        raise ValueError("gs_swap: divisor tiene menos de dos elementos")


def gs_module(stack):
    base = stack.pop()
    valor = stack.pop()

    valido = True

    if isinstance(base, Integer):
        if isinstance(valor, Integer):
            nvo = valor % base
            stack.append(nvo)
        elif isinstance(valor, Array):
            paso = int(base)
            nvo = Array(valor.name[::paso])
            stack.append(nvo)
        else:
            valido = False
    elif isinstance(base, String) and isinstance(valor, String):
        lista = [String(x) for x in valor.name.split(base.name) if x]
        stack.append(Array(lista))
    elif isinstance(base, Block) and isinstance(valor, Array):
        from evaluador import evaluar
        stack_start = len(stack.name)
        for elemento in valor.name:
            stack.append(elemento)
            evaluar(base)
        resultado = Array(stack.name[stack_start:])
        stack.name = stack.name[:stack_start]
        stack.append(resultado)

    if not valido:
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
            #   poner nada en el divisor.
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
    # Ejecuta el bloque, saca tope del divisor; si
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
    # Ejecuta el bloque-condicion y saca un valor del divisor.
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
    # Ejecuta el bloque-condicion y saca un valor del divisor.
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


def gs_print(stack):
    a = stack.pop()
    print(a, end='')


def gs_random(stack):
    a = stack.pop()
    valor = random.randint(0, int(a) - 1)
    stack.append(Integer(valor))


def gs_abs(stack):
    a = int(stack.pop())
    if a < 0:
        a = -a
    stack.append(Integer(a))

def gs_base(stack):
    #
    #   valor_a_convertir base_ocupar base
    #
    #   Produce una lista de valores enteros B[]
    #   con la representación del valor en el sistema
    #   posicional de base_ocupar.
    #
    #   lista base_ocupar base
    #
    #   Convierte lista a decimal
    #
    top = stack.pop()
    sig = stack.pop()

    base = int(top)
    if isinstance(sig, Integer):
        #   Convertir un entero en una lista de factores
        valor = int(sig)

        lista = []
        while valor >= base:
            valor, resto = divmod(valor, base)
            lista.append(resto)
        if valor:
            lista.append(valor)
        stack.append(Array(lista[::-1]))
    elif isinstance(sig, Array):
        #   Convertir una lista de factores a decimal
        dec = 0
        potencia = 1
        for factor in sig.name[::-1]:
            dec += int(factor) * potencia
            potencia *= base
        stack.append(Integer(dec))

def gs_zip(stack):
    original = stack.pop()
    matriz = []
    tipo = original.name[0]
    for fila in original.name:
        matriz.append(fila.name)

    final = Array([])

    if isinstance(tipo, String):
        transpose = [''.join(a) for a in zip(*matriz)]
        for sublista in transpose:
            final.append(String(sublista))

    elif isinstance(tipo, Array):
        transpose = [a for a in zip(*matriz)]
        for sublista in transpose:
            final.append(Array(sublista))
    else:
        raise ValueError("Error: tipo de dato erroneo")

    stack.append(final)

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
        Var('print'): gs_print,
        Var('random'): gs_random,
        Var('abs'): gs_abs,
        Var('base'): gs_base,
        Var('zip'): gs_zip,
    }


reset_variables()
