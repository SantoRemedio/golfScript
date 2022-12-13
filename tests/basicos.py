import unittest
from compiler import evaluate, reset, tokenizador

class TestBasico(unittest.TestCase):

    def test_assign(self):
        reset()
        source = "1:a a"

        resultado = evaluate(source)
        self.assertEqual("[1 1]", str(resultado))

    def test_definir_operador(self):
        reset()
        source = "{.}{*}+:square;2 square"

        resultado = evaluate(source)
        self.assertEqual("[4]", str(resultado))

    def test_block(self):
        reset()
        source = "2 {2*} 5*"

        resultado = evaluate(source)
        self.assertEqual("[64]", str(resultado))
