from tipos import Array


class Stack(Array):
    def __init__(self, lista):
        super().__init__(lista)

    def pop(self):
        obj = self.name.pop()
        if self.name and obj.marked:
            self.name[-1].marked = True
        return obj
