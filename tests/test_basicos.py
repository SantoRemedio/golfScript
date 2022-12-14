import unittest
from evaluador import evaluar, reset

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

    def test_gcd(self):
        reset()
        source = r";'2706 410'~{.@\%.}do;"

        resultado = evaluar(source)
        self.assertEqual("[82]", str(resultado))

    def test_xx(self):
        reset()
        source = r"0 1 {100<} { .@+ } /"

        resultado = evaluar(source)
        self.assertEqual("[89 [1 1 2 3 5 8 13 21 34 55 89]]", str(resultado))

    def test_mod_array_block(self):
        reset()
        source = "[1 2 3]{.}%"

        resultado = evaluar(source)
        self.assertEqual("[[1 1 2 2 3 3]]", str(resultado))

    def test_pow(self):
        reset()
        source = "[1 2 3 4 5 6] {.* 20>} ?"

        resultado = evaluar(source)
        self.assertEqual("[5]", str(resultado))

    def test_if(self):
        reset()
        source = "0 2 {1.} if"

        resultado = evaluar(source)
        self.assertEqual("[1 1]", str(resultado))

    def test_debug_pi(self):
        reset()
        source = r";''6666, -2 % {2 + .2 / @ *\ / 10.3??2 * +} *`50 < ~\;"
        #source = r";''6666,-2%{" # 2+.2/@*\/10.3??2*+}*`50<~\;"

        resultado = evaluar(source)
        print(resultado)

    def test_until2(self):
        reset()
        source = r"0{.5=}{.1+}until"

        resultado = evaluar(source)
        self.assertEqual("[0 1 2 3 4 5]", str(resultado))

    def test_mult_array_array(self):
        reset()
        source = r"[1 [2] [3 [4 [5]]]][6 7]*"

        resultado = evaluar(source)
        self.assertEqual("[[1 6 7 2 6 7 3 [4 [5]]]]", str(resultado))

    def test_xor(self):
        reset()
        source = r"10 0xor"

        resultado = evaluar(source)
        self.assertEqual("[1]", str(resultado))

    def test_xor2(self):
        reset()
        source = r"0 10xor"

        resultado = evaluar(source)
        self.assertEqual("[10]", str(resultado))

    def test_xor_both(self):
        reset()
        source = r"10 20xor"

        resultado = evaluar(source)
        self.assertEqual("[0]", str(resultado))

    def test_xor_none(self):
        reset()
        source = r"0 0xor"

        resultado = evaluar(source)
        self.assertEqual("[0]", str(resultado))

    def test_mult_array_string(self):
        reset()
        source = "[1 [2] [3 [4 [5]]]]'-'*"

        resultado = evaluar(source)
        self.assertEqual(r'["1-\x02-\x03\x04\x05"]', str(resultado))