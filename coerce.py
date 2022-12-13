import unittest
from compiler import evaluate, reset


class TestBasico(unittest.TestCase):

    def test_integer_list(self):
        reset()
        source = "1[2]+"
        resultado = evaluate(source)
        self.assertEqual("[[1 2]]", str(resultado))

    def test_integer_string(self):
        reset()
        source = "1'2'+"
        resultado = evaluate(source)
        self.assertEqual("['12']", str(resultado))


