#
#   Procesa un string con escapes
#
def raw_string(texto):
    #
    # Recibe un string y escapa solo los \ y '
    #
    lista = []
    escape = False
    for letra in texto:
        if not escape and letra == '\\':
            escape = True
        else:
            if escape:
                escape = False
                if letra not in "'":
                    lista.append('\\')
            lista.append(letra)
    return ''.join(lista)

escapes = {
    r'n': '\n',
    r't': '\t',
    r'r': '\r',
    r'\'': "'",
    r'\\': "\\",
}

def escaped_string(texto):
    #
    # Recibe un string y escapa todo
    #
    lista = []
    escape = False
    for letra in texto:
        if not escape and letra == '\\':
            escape = True
        else:
            if escape:
                letra = escapes.get(letra, letra)
                escape = False
            lista.append(letra)
    return ''.join(lista)

