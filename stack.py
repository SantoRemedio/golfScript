from tipos import Array, String, start_list, end_list
#
#   Implementación del stack golfScript
#
#   Es un stack común y corriente, excepto que puede
#   contener elementos que no "popeables".
#
#   En concreto, los "[" no cuentan como elementos del stack;
#   cualquier pop() se los salta sin eliminarlos.
#
#   OJO: stack.push(stack.pop()) no está garantizado dejar
#   todo igual. Si quieres "mirar" un elemento, usa peek()

class Stack(Array):
    def __init__(self, lista):
        super().__init__(lista)

    def pop(self, pos=0):
        #
        #   Retorna el primer objeto disponible que no
        #   sea una marca "["
        #
        #   El parámetro pos indica la posición del elemento
        #   a extraer:
        #       pos = 0 -> top del stack.
        #       pos = -1 -> segundo elemento
        #
        #   Comenzamos la búsqueda por el último elemento
        buscado = self.buscar_n(pos)
        obj = self.name.pop(buscado)
        return obj

    def push(self, elemento):
        self.name.append(elemento)

    def peek(self, pos=0):
        #
        #   Busca el enesimo elemento en el stack
        #   y lo retorna sin extraerlo
        #
        buscado = self.buscar_n(pos)
        return self.name[buscado]

    def buscar_n(self, pos):
        #
        #   Busca el enesimo elemento en el stack,
        #   sin contar los "["
        #
        buscado = len(self.name) - 1

        for buscado in range(buscado, -1, -1):
            if self.name[buscado] != start_list:
                if pos == 0:
                    break
                pos -= 1
        else:
            raise IndexError("Error, stack vacio")

        return buscado

    def extraer(self):
        #
        #   Extrae todos los elementos desde el tope
        #   hasta la marca "[" o fondo del stack. Los
        #   elementos se devuelven en una lista y la
        #   marca se descarta.
        lista = []
        try:
            while self.name[-1] != start_list:
                elemento = self.name.pop()
                lista.append(elemento)
            self.name.pop()
        except IndexError:
            #   No es problema si se acaba el stack
            #   sin encontrar un "["
            pass

        return Array(lista[::-1])

    def __contains__(self, item):
        return item in self.name

    def __getitem__(self, item):
        raise ValueError("Acceso inválido al stack.")