import unittest
from evaluador import evaluar, reset


class TestBasico(unittest.TestCase):

    def test_integer_list(self):
        reset()
        source = "1[2]+"
        resultado = evaluar(source)
        self.assertEqual("[[1 2]]", str(resultado))

    def test_integer_string(self):
        reset()
        source = "1'2'+"
        resultado = evaluar(source)
        self.assertEqual('["12"]', str(resultado))

    def test_string(self):
        reset()
        source = "'asdf'$"
        resultado = evaluar(source)
        self.assertEqual('["adfs"]', str(resultado))

    def test_coerce_string_block(self):
        reset()
        source = "'abcd'"
        resultado = evaluar(source)
        var = resultado.pop()
        st = var.coerce(3)
        print(resultado)
