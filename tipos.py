import uuid

class GS_Type:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name if type(self) == type(other) else False
    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)

    def __hash__(self):
        return hash(self.name);

class Var(GS_Type):
    #   Variables
    def __init__(self, name):
        #   name es el string con el nombre de la variable
        super().__init__(name)

class Integer(GS_Type):
    # Enteros
    def __init__(self, name):
        #   name es la representación del entero como string
        super().__init__(name)
        self.precedence = 0;

    def coerce(self, precedence):
        # convierte este objeto a uno del
        # tipo con la precedencia adecuada:
        if precedence == 0:
            return self
        if precedence == 1:
            return List([self])
        if precedence == 2:
            return String(str(self.name))
        if precedence == 3:
            return Block([self])
        raise ValueError(f"Error en Integer.coerse: precedencia invalida {precedence}")
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
        valor = f'"{self.name}"'
        return valor

class String(GS_Type):
    def __init__(self, name):
        super().__init__(name)
        self.precedence = 2

    def coerce(self, precedence):
        if precedence == 3:
            return Block([self.name])
        else:
            return self

    def __add__(self, other):
        return String(self.name + other.name)

    def __str__(self):
        var = self.name.replace('"',  '\\"')
        return f'"{var}"'

    def __repr__(self):
        return f"'{self.name}'"

    def __bool__(self):
        return self.name != ''

class Block(GS_Type):
    #  Bloques de código como "{..-}"
    #  Son inmutables.
    def __init__(self, block):
        super().__init__(block)
        self.hash = uuid.uuid1().int
        self.precedence = 3

    def coerce(self, precedence):
        return self

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

class List(GS_Type):
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
            return String(str(self.name))
        if precedence == 3:
            return Block([self])


    def append(self, elemento):
        self.name.append(elemento)

    def extend(self, lista):
        self.name.extend(lista)

    def pop(self):
        return self.name.pop()

    def reset(self):
        self.name = []

    def __add__(self, other):
        return List([*self.name, *other.name])

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




cero = Var(0)
uno = Var(1)
colon = Var(':')
start_block = Var('{')
end_block = Var('}')
start_list = Var('[')
end_list = Var(']')
