#
#   Revisa el correcto parsing del lenguaje.
#
import unittest
from evaluador import reset, tokenizar, lexer
from tipos import Var, Array, String, Block, Integer


class TestBasico(unittest.TestCase):
    def test_parse(self):
        reset()
        source = "1 2 3"
        resultado = Array([x for x in tokenizar(source)])
        self.assertEqual("[1 2 3 None]", str(resultado))

    def test_parse_block(self):
        reset()
        source = "1 {1 3 4} 2"
        resultado = Array([x for x in tokenizar(source)])
        self.assertEqual("[1 {1 3 4} 2 None]", str(resultado))
        self.assertEqual("<class 'tipos.Block'>", str(type(resultado[1])))

    def test_lista(self):
        reset()
        source = "[1 2 3]"
        resultado = [x for x in tokenizar(source)]
        self.assertEqual("[[, 1, 2, 3, ], None]", str(resultado))

    def test_listas(self):
        reset()
        source = "[1 2 [4 5] 3]"
        resultado = [x for x in tokenizar(source)]
        self.assertEqual("[[, 1, 2, [, 4, 5, ], 3, ], None]", str(resultado))

    def test_variables(self):
        reset()
        source = "1:a a"
        resultado = Array([x for x in tokenizar(source)])
        self.assertEqual("[1 : a a None]", str(resultado))

    def test_variable(self):
        reset()
        source = 'a'
        resultado = [x for x in tokenizar(source)]
        self.assertEqual("[a, None]", str(resultado))
        self.assertTrue(isinstance(resultado[0], Var), "No es instacia de Var")

    def test_block_str(self):
        reset()
        source = "{ab}"
        resultado = [x for x in tokenizar(source)]
        self.assertEqual("[{ab}, None]", str(resultado))

    def test_lista2(self):
        reset()
        source = "[1 2 3]"
        resultado = [x for x in tokenizar(source)]
        self.assertEqual("[[, 1, 2, 3, ], None]", str(resultado))

    def test_lista3(self):
        reset()
        source = "[1 2 3]~"
        resultado = [x for x in tokenizar(source)]
        self.assertEqual("[[, 1, 2, 3, ], ~, None]", str(resultado))

    def test_lista1(self):
        reset()
        source = "[1 2 3]~"
        resultado = [x for x in lexer(source)]
        self.assertEqual("[[, 1, 2, 3, ], ~, None]", str(resultado))

    def test_list_empty(self):
        reset()
        source = "[]!"
        resultado = [x for x in tokenizar(source)]
        self.assertEqual("[[, ], !, None]", str(resultado))

    def test_cero(self):
        reset()
        source = "0"
        resultado = Array([x for x in tokenizar(source)])
        self.assertEqual("[0 None]", str(resultado))

    def test_str_list(self):
        reset()
        a = Array([1, 2, 3])
        resultado = str(a)
        self.assertEqual("[1 2 3]", str(resultado))

    def test_str_repr(self):
        reset()
        a = String("abc")
        self.assertEqual(r'\"abc\"', repr(a))

    def test_str_str(self):
        reset()
        a = String("abc")
        self.assertEqual('"abc"', str(a))

    def test_str_s(self):
        reset()
        source = "'asdf'$"
        resultado = Array([x for x in tokenizar(source)])
        self.assertEqual('["asdf" $ None]', str(resultado))

    def test_comment(self):
        reset()
        source = "1 1+ # comentario"
        resultado = Array([x for x in tokenizar(source)])
        self.assertEqual('[1 1 + None]', str(resultado))

    def test_negativo(self):
        reset()
        source = "1 -1"
        resultado = Array([x for x in tokenizar(source)])
        self.assertEqual('[1 -1 None]', str(resultado))

    def test_block(self):
        reset()
        source = "{abcd  efg}"
        resultado = Array([x for x in tokenizar(source)])
        b = Block(resultado)
        self.assertEqual('[{abcd efg} None]', str(resultado))

    def test_xor_string(self):
        reset()
        a = String("abcdef")
        b = String("a112")
        c = a ^ b
        self.assertEqual('"bcdef12"', str(c))

    def test_xor_List(self):
        reset()
        a = Array(['a', 'b', 'c'])
        b = Array(['a', 1, 2])
        c = a ^ b
        self.assertEqual('[b c 1 2]', str(Array(c)))

    def test_and_List(self):
        reset()
        a = Array([String('a'), String('b'), String('c')])
        b = Array([String('a'), Integer(1), Integer(2)])
        c = a & b
        self.assertEqual('["a"]', str(c))

    def test_refactoring(self):
        reset()
        source = "1 2 3"
        lista = Array([x for x in tokenizar(source)])
        print(lista)
