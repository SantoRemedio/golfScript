#
#   Revisa el correcto parsing del lenguaje.
#
import unittest
from compiler import reset, tokenizador, lexer
from tipos import Var, List, String

class TestBasico(unittest.TestCase):
    def test_parse(self):
        reset()
        source = "1 2 3"
        resultado = List([x for x in tokenizador(source)])
        self.assertEqual("[1 2 3]", str(resultado))

    def test_parse_block(self):
        reset()
        source = "1 {1 3 4} 2"
        resultado = List([x for x in tokenizador(source)])
        self.assertEqual("[1 {1 3 4} 2]", str(resultado))
        self.assertEqual("<class 'tipos.Block'>", str(type(resultado[1])))

    def test_lista(self):
        reset()
        source = "[1 2 3]"
        resultado = [x for x in tokenizador(source)]
        self.assertEqual("[[1 2 3]]", str(resultado))

    def test_listas(self):
        reset()
        source = "[1 2 [4 5] 3]"
        resultado = [x for x in tokenizador(source)]
        self.assertEqual("[[1 2 [4 5] 3]]", str(resultado))

    def test_variables(self):
        reset()
        source = "1:a a"
        resultado = List([x for x in tokenizador(source)])
        self.assertEqual("[1 : a a]", str(resultado))

    def test_variable(self):
        reset()
        source = 'a'
        resultado = [x for x in tokenizador(source)]
        self.assertEqual("[a]", str(resultado))
        self.assertTrue(isinstance(resultado[0], Var), "No es instacia de Var")

    def test_block_str(self):
        reset()
        source = "{ab}"
        resultado = [x for x in tokenizador(source)]
        self.assertEqual("[{ab}]", str(resultado))

    def test_lista(self):
        reset()
        source = "[1 2 3]"
        resultado = [x for x in tokenizador(source)]
        self.assertEqual("[[1, 2, 3]]", str(resultado))

    def test_lista(self):
        reset()
        source = "[1 2 3]~"
        resultado = [x for x in tokenizador(source)]
        self.assertEqual("[[1 2 3], ~]", str(resultado))

    def test_lista2(self):
        reset()
        source = "[1 2 3]~"
        resultado = List([x for x in lexer(source)])
        self.assertEqual("[[ 1 2 3 ] ~ None]", str(resultado))

    def test_list_empty(self):
        reset()
        source = "[]!"
        resultado = List([x for x in tokenizador(source)])
        self.assertEqual("[[] !]", str(resultado))

    def test_cero(self):
        reset()
        source = "0"
        resultado = List([x for x in tokenizador(source)])
        self.assertEqual("[0]", str(resultado))

    def test_str_list(self):
        reset()
        a = List([1, 2, 3])
        resultado = str(a)
        self.assertEqual("[1 2 3]", str(resultado))

    def test_str_repr(self):
        reset()
        a = String("abc")
        self.assertEqual("'abc'", repr(a))

    def test_str_str(self):
        reset()
        a = String("abc")
        self.assertEqual('"abc"', str(a))

    def test_str_s(self):
        reset()
        source = "'asdf'$"
        resultado = List([x for x in tokenizador(source)])
        self.assertEqual('["asdf" $]', str(resultado))

    def test_comment(self):
        reset()
        source = "1 1+ # comentario"
        resultado = List([x for x in tokenizador(source)])
        self.assertEqual('[1 1 +]', str(resultado))

    def test_negativo(self):
        reset()
        source = "1 -1"
        resultado = List([x for x in tokenizador(source)])
        self.assertEqual('[1 -1]', str(resultado))
