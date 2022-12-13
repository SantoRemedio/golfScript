import unittest
from evaluador import evaluar, reset, tokenizar

class TestBasico(unittest.TestCase):

    def test_assign(self):
        reset()
        source = "1:a a"

        resultado = evaluar(source)
        self.assertEqual("[1 1]", str(resultado))

    def test_definir_operador(self):
        reset()
        source = "{.}{*}+:square;2 square"

        resultado = evaluar(source)
        self.assertEqual("[4]", str(resultado))

    def test_block(self):
        reset()
        source = "2 {2*} 5*"

        resultado = evaluar(source)
        self.assertEqual("[64]", str(resultado))

    def test_block(self):
        reset()
        source = "10{.(}3*"

        resultado = evaluar(source)
        self.assertEqual("[10 9 8 7]", str(resultado))
