from tipos import Array


class Stack(Array):
    def __init__(self, lista):
        super().__init__(lista)

    def pop(self):
        obj = self.name.pop()
        return obj
