#
#   Procesa un string con escapes
#
def raw_string(texto):
    #
    # Recibe un string y escapa solo los \ y '
    #
    lista = []
    escape = False
    for car in texto:
        if car == "\\" and not escape:
            escape = True
            continue
        if escape:
            escape = False
            if car != "'":
                lista.append("\\\\")
        lista.append(car)

    st = ''.join(lista)
    return st

def escaped_string(texto):
    #
    # Recibe un string y escapa todo
    #
    st = texto.replace(r"\n", "\n")
    st = st.replace(r"\t", "\t")
    st = bytes(st, "utf-8").decode("unicode_escape")
    return st

