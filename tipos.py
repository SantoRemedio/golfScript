#
#   golfScript maneja cuatro tipos de datos:
#   - Integer
#   - Array
#   - String
#   - Block
#   que son basicamente wrappers alrededor de los
#   tipos basicos.
#
#   Cada tipo tiene un orden de precedencia que controla
#   las conversiones en operadores que mezclan tipos.
#   El método coerce(precedencia) convierte tipos.
#
#   El quinto tipo, Var, sirve para manejar las
#   llaves del diccionario de variables.
#
import uuid

#  Debido a la naturaleza del problema, los métodos mágicos resultan
#  simples considerando que solo interactuan entre si cuatro clases
#  distintas.

#  Aunque las operaciones de suma, resta, etc deberían estar implementadas
#  en la misma clase, algunas operaciones no producen resultados, sólo
#  manipulan el divisor, que es externo, y necesitarian llamar al evaluador().
#  En resumen: las operaciones se implementan afuera.

class GSType:
    #   Tipo base, no se usa por si solo.
    def __init__(self, name):
        self.name = name

    def coerse(self, precedence):
        #   Cada tipo de dato debe ser capaz de
        #   autoconvertirse en otro vía este
        #   metodo.
        raise ValueError("Método coerce() no implementado")

    def __eq__(self, other):
        return self.name == other.name if type(self) == type(other) else False

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)

    def __hash__(self):
        return hash(self.name)

    def __bool__(self):
        raise ValueError("Tipo de dato no tiene __bool__()")


class Var(GSType):
    #   Contiene el nombre de una variable.
    #   El nombre de una variable puede ser cualquier
    #   tipo de objeto.
    def __init__(self, name):
        #   name es el string con el nombre de la variable
        super().__init__(name)


class Integer(GSType):
    # Representa enteros.
    def __init__(self, name):
        #   name es la representación del entero como string
        super().__init__(name)
        self.precedence = 0

    def coerce(self, precedence):
        # convierte este objeto a uno del
        # tipo con la precedencia adecuada:
        if precedence == 0:
            return self
        if precedence == 1:
            return Array([self])
        if precedence == 2:
            return String(str(self.name))
        if precedence == 3:
            return Block([self])
        raise ValueError(f"Error en Integer.coerse: precedencia invalida {precedence}")

    def __str__(self):
        return str(self.name)

    def __add__(self, other):
        suma = self.name + other.name
        return Integer(suma)

    def __sub__(self, other):
        resta = self.name - other.name
        return Integer(resta)

    def __mul__(self, other):
        resultado = self.name * other.name
        return Integer(resultado)

    def __divmod__(self, other):
        resultado = self.name // other.name
        return Integer(resultado)

    def __truediv__(self, other):
        resultado = self.name // other.name
        return Integer(resultado)

    def __floordiv__(self, other):
        resultado = self.name // other.name
        return Integer(resultado)

    def __mod__(self, other):
        resultado = self.name % other.name
        return Integer(resultado)

    def __pow__(self, power, modulo=None):
        resultado = self.name ** power.name
        return Integer(resultado)

    def __neg__(self):
        return Integer(-self.name)

    def __int__(self):
        return self.name

    def __bool__(self):
        return self.name != 0

    def __repr__(self):
        return str(self.name)

    def __gt__(self, other):
        return self.name > other.name

    def __xor__(self, other):
        return Integer(self.name ^ other.name)

    def __and__(self, other):
        return Integer(self.name & other.name)


class String(GSType):
    def __init__(self, name):
        super().__init__(name)
        self.precedence = 2

    def coerce(self, precedence):
        if precedence == 3:
            return Block([self.name])
        elif precedence < 3:
            return self

        raise ValueError(f"Error en String.coerse: precedencia invalida {precedence}")

    def __add__(self, other):
        return String(self.name + other.name)

    def __str__(self):
        var = self.name.replace('"', '\\"')
        return f'"{var}"'

    def __repr__(self):
        return f"'{self.name}'"

    def __bool__(self):
        return self.name != ''

    def __gt__(self, other):
        return self.name > other.name

    def __xor__(self, other):
        faltantes = []
        for letra in other.name:
            if letra not in self.name and letra not in faltantes:
                faltantes.append(letra)
        lista = [letra for letra in self.name if letra not in other.name]
        return String(''.join(lista + faltantes))

    def __and__(self, other):
        lista = [letra for letra in self.name if letra in other.name]
        return String(''.join(lista))


class Block(GSType):
    #  Bloques de código como "{..-}"
    #  Son inmutables.
    def __init__(self, block):
        super().__init__(block)
        self.hash = uuid.uuid1().int
        self.precedence = 3

    # noinspection PyUnusedLocal
    def coerce(self, precedence):
        return self

    def append(self, elemento):
        self.name.append(elemento)

    def __add__(self, other):
        block = self.name + other.name
        return Block(block)

    def __hash__(self):
        return self.hash

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "{" + ' '.join(str(x) for x in self.name) + "}"

    def __bool__(self):
        return len(self.name) > 0

    def __iter__(self):
        return iter(self.name)


class Array(GSType):
    def __init__(self, lista=None):
        if None:
            lista = []
        super().__init__(lista)
        self.hash = uuid.uuid1().int
        self.precedence = 1

    def coerce(self, precedence):
        if precedence == 0:
            return self
        if precedence == 1:
            return self
        if precedence == 2:
            # Para transformar un array en string,
            # se convierten los enteros en el caracter
            # del mismo valor y se concatenan con otros
            # contenidos para formar un string
            #
            # [51 52 'x']'23'+ => "34x23"
            lista = []
            for elemento in self.name:
                if isinstance(elemento, Integer):
                    lista.append(chr(int(elemento)))
                elif isinstance(elemento, String):
                    # Necesitamos el string sin editar
                    lista.append(elemento.name)
                else:
                    raise ValueError(f"Error en Array.coerce(): elemento desconocido {type(elemento)}")

            st = ''.join(lista)
            return String(st)
        if precedence == 3:
            #   Convertir el array en un bloque
            lista = []
            for elemento in self.name:
                if isinstance(elemento, Integer):
                    lista.append(elemento)
                elif isinstance(elemento, String):
                    # Los string se convierten en variables.
                    # Necesitamos el nombre sin editar
                    lista.append(Var(elemento.name))
                else:
                    raise ValueError(f"Error en Array.coerce(): elemento desconocido {type(elemento)}")

            return Block(lista)

        raise ValueError(f"Error en Array.coerse: precedencia invalida {precedence}")

    def append(self, elemento):
        if issubclass(type(elemento), GSType):
            self.name.append(elemento)
        else:
            raise ValueError("append: Tipo no valido")

    def extend(self, lista):
        self.name.extend(lista)

    def pop(self):
        return self.name.pop()

    def reset(self):
        self.name = []

    def __add__(self, other):
        return Array([*self.name, *other.name])

    def __hash__(self):
        return self.hash

    def __bool__(self):
        return len(self.name) > 0

    def __getitem__(self, item):
        return self.name[item]

    def __setitem__(self, key, value):
        self.name[key] = value

    def __len__(self):
        return len(self.name)

    def __contains__(self, item):
        return item in self.name

    def __str__(self):
        return '[' + ' '.join(str(x) for x in self.name) + ']'

    def __repr__(self):
        return str(self)

    def __xor__(self, other):
        faltantes = []
        #   Extraer del otro operando todos los elementos que
        #   no estan en éste (sin duplicados)
        for elemento in other.name:
            if elemento not in self.name and elemento not in faltantes:
                faltantes.append(elemento)

        #   Extraer todos los elementos de este Array que no están
        #   en el otro operando (sin duplicados).

        lista = []
        for elemento in self.name:
            if elemento not in other.name and elemento not in lista:
                lista.append(elemento)
        #lista = [elemento for elemento in self.name if elemento not in other.name]
        return Array(lista + faltantes)

    def __and__(self, other):
        lista = [elemento for elemento in self.name if elemento in other.name]
        return Array(lista)


cero = Integer(0)
uno = Integer(1)
menos_uno = Integer(-1)
colon = Var(':')
start_block = Var('{')
end_block = Var('}')
start_list = Var('[')
end_list = Var(']')
