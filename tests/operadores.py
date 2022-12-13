import unittest
from compiler import evaluate, reset

class TestBasico(unittest.TestCase):
    def test_add(self):
        reset()
        source = "1 2+"
        resultado = evaluate(source)
        self.assertEqual("[3]", str(resultado))


    def test_concat(self):
        reset()
        source = "'a' 'b'+"
        resultado = evaluate(source)
        self.assertEqual('["ab"]', str(resultado))

    def test_tail(self):
        reset()
        source = "'abc')"
        resultado = evaluate(source)
        self.assertEqual('["ab" 99]', str(resultado))

    def test_subtract(self):
        reset()
        source = "5 2-"
        resultado = evaluate(source)
        self.assertEqual("[3]", str(resultado))

    def test_multiplyt(self):
        reset()
        source = "5 2*"
        resultado = evaluate(source)
        self.assertEqual("[10]", str(resultado))

    def test_div(self):
        reset()
        source = "5 2/"
        resultado = evaluate(source)
        self.assertEqual("[2]", str(resultado))

    def test_power(self):
        reset()
        source = "5 2?"
        resultado = evaluate(source)
        self.assertEqual("[25]", str(resultado))

    def test_dec_1(self):
        reset()
        source = "5("
        resultado = evaluate(source)
        self.assertEqual("[4]", str(resultado))

    def test_dinc_1(self):
        reset()
        source = "5)"
        resultado = evaluate(source)
        self.assertEqual("[6]", str(resultado))

    def test_swap(self):
        reset()
        source = "1 2 3 4\\"
        resultado = evaluate(source)
        self.assertEqual("[1 2 4 3]", str(resultado))

    def test_dup_n(self):
        reset()
        source = "1 2 3 4 1$"
        resultado = evaluate(source)
        self.assertEqual("[1 2 3 4 3]", str(resultado))

    def test_dup_n_string(self):
        reset()
        source = "'asdf'$"
        resultado = evaluate(source)
        self.assertEqual('["adfs"]', str(resultado))


    def test_rotate(self):
        reset()
        source = "1 2 3 4@"
        resultado = evaluate(source)
        self.assertEqual("[1 3 4 2]", str(resultado))

    def test_cola(self):
        reset()
        source = "'123 45'~"
        resultado = evaluate(source)
        self.assertEqual("[123 45]", str(resultado))

    def test_module(self):
        reset()
        source = "10 3%"

        resultado = evaluate(source)
        self.assertEqual("[1]", str(resultado))

    def test_dup(self):
        reset()
        source = "10."

        resultado = evaluate(source)
        self.assertEqual("[10 10]", str(resultado))


    def test_chancho_integer(self):
        reset()
        source = "5~"
        resultado = evaluate(source)
        self.assertEqual("[-6]", str(resultado))


    def test_chancho_string(self):
        reset()
        source = "'1 2+'~"
        resultado = evaluate(source)
        self.assertEqual("[3]", str(resultado))

    def test_chancho_block(self):
        reset()
        source = "{1 2+}~"
        resultado = evaluate(source)
        self.assertEqual("[3]", str(resultado))

    def test_chancho_list(self):
        reset()
        source = "[1 2 3]~"
        resultado = evaluate(source)
        self.assertEqual("[1 2 3]", str(resultado))

    def test_suma_list(self):
        reset()
        source = "[1 2 3]~++"
        resultado = evaluate(source)
        self.assertEqual("[6]", str(resultado))

    def test_concatena_bloques(self):
        reset()
        source = "{a}{b}+"
        resultado = evaluate(source)
        self.assertEqual("[{a b}]", str(resultado))

    def test_not_Integer_1(self):
        reset()
        source = "1!"
        resultado = evaluate(source)
        self.assertEqual("[0]", str(resultado))

    def test_not_Integer_0(self):
        reset()
        source = "0!"
        resultado = evaluate(source)
        self.assertEqual("[1]", str(resultado))

    def test_not_List(self):
        reset()
        source = "[1]!"
        resultado = evaluate(source)
        self.assertEqual("[0]", str(resultado))

    def test_not_List_empty(self):
        reset()
        source = "[]!"
        resultado = evaluate(source)
        self.assertEqual("[1]", str(resultado))

    def test_List_empty(self):
        reset()
        source = "[]"
        resultado = evaluate(source)
        self.assertEqual("[[]]", str(resultado))

    def test_repr(self):
        reset()
        source = "1`"
        resultado = evaluate(source)
        self.assertEqual('["1"]', str(resultado))

    def test_coerce(self):
        reset()
        source = "'asdf'{1234}+"
        resultado = evaluate(source)
        self.assertEqual('[{asdf 1234}]', str(resultado))

    def test_negativos(self):
        reset()
        source = "1 -3"
        resultado = evaluate(source)
        self.assertEqual('[1 -3]', str(resultado))

    def test_negativos2(self):
        reset()
        source = "1 2-3+"
        resultado = evaluate(source)
        self.assertEqual('[1 -1]', str(resultado))

    def test_negativos3(self):
        reset()
        source = "1 2 -3+"
        resultado = evaluate(source)
        self.assertEqual('[1 -1]', str(resultado))


    def test_resta_block(self):
        reset()
        source = "[5 2 5 4 1 1][1 2]-"
        resultado = evaluate(source)
        self.assertEqual('[[5 5 4]]', str(resultado))

    def test_mult_string(self):
        reset()
        source = "'abc'3*"
        resultado = evaluate(source)
        self.assertEqual('["abcabcabc"]', str(resultado))

    def test_mult_string2(self):
        reset()
        source = "3'abc'*"
        resultado = evaluate(source)
        self.assertEqual('["abcabcabc"]', str(resultado))

    def test_mult_list(self):
        reset()
        source = "[1 2 3]3*"
        resultado = evaluate(source)
        self.assertEqual('[[1 2 3 1 2 3 1 2 3]]', str(resultado))

    def test_mult_list_string(self):
        reset()
        source = "[1 2 3]','*"
        resultado = evaluate(source)
        self.assertEqual('["1,2,3"]', str(resultado))

    def test_mult_list_list(self):
        reset()
        source = "[1 2 3][4]*"
        resultado = evaluate(source)
        self.assertEqual('[[1 4 2 4 3]]', str(resultado))

    def test_mult_string_string(self):
        reset()
        source = "'asdf'' '*"
        resultado = evaluate(source)
        self.assertEqual('["a s d f"]', str(resultado))

    def test_mult_list_block(self):
        reset()
        source = "[1 2 3 4]{+}*"
        resultado = evaluate(source)
        self.assertEqual('[10]', str(resultado))


    def test_mult_list_block(self):
        reset()
        source = "'asdf'{+}*"
        resultado = evaluate(source)
        self.assertEqual('[414]', str(resultado))

    def test_inc_list(self):
        reset()
        source = "[1 2 3])"
        resultado = evaluate(source)
        self.assertEqual('[[1 2] 3]', str(resultado))

    def test_dec_list(self):
        reset()
        source = "[1 2 3]("
        resultado = evaluate(source)
        self.assertEqual('[[2 3] 1]', str(resultado))

    def test_power_list(self):
        reset()
        source = "4[5 5 4 1 2 3]?"
        resultado = evaluate(source)
        self.assertEqual('[2]', str(resultado))

    def test_power_list_s(self):
        reset()
        source = "'a' [5 5 'a' 1 2 3]?"
        resultado = evaluate(source)
        self.assertEqual('[2]', str(resultado))

    def test_power_list_list(self):
        reset()
        source = "[6 7] [5 5 'a' [6 7] 1 2 3]?"
        resultado = evaluate(source)
        self.assertEqual('[3]', str(resultado))

    def test_power_list_no(self):
        reset()
        source = "[6] [5 5 'a' [6 7] 1 2 3]?"
        resultado = evaluate(source)
        self.assertEqual('[-1]', str(resultado))

    def test_greater_int_int(self):
        reset()
        source = "1 2>"
        resultado = evaluate(source)
        self.assertEqual('[0]', str(resultado))

    def test_greater_int_int2(self):
        reset()
        source = "3 2>"
        resultado = evaluate(source)
        self.assertEqual('[1]', str(resultado))

    def test_greater_str_str(self):
        reset()
        source = "'def' 'abc'>"
        resultado = evaluate(source)
        self.assertEqual('[1]', str(resultado))

    def test_greater_str_str2(self):
        reset()
        source = "'abc' 'def' >"
        resultado = evaluate(source)
        self.assertEqual('[0]', str(resultado))

    def test_greater_list(self):
        reset()
        source = "[1 2 3 4 5] 2 >"
        resultado = evaluate(source)
        self.assertEqual('[[3 4 5]]', str(resultado))

    def test_greater_list_menos(self):
        reset()
        source = "[1 2 3 4 5] -2 >"
        resultado = evaluate(source)
        self.assertEqual('[[4 5]]', str(resultado))

    def test_greater_block(self):
        reset()
        source = "{abcd} 2 >"
        resultado = evaluate(source)
        self.assertEqual('[{cd}]', str(resultado))

    def test_xor_int(self):
        reset()
        source = "419 234^"
        resultado = evaluate(source)
        self.assertEqual('[329]', str(resultado))

    def test_if(self):
        reset()
        source = "1 2 3 if"
        resultado = evaluate(source)
        self.assertEqual('[2]', str(resultado))

    def test_if_false(self):
        reset()
        source = "0 2 3 if"
        resultado = evaluate(source)
        self.assertEqual('[3]', str(resultado))

    def test_do(self):
        reset()
        source = "5{1-..}do"
        resultado = evaluate(source)
        self.assertEqual('[4 3 2 1 0 0]', str(resultado))

    def test_while(self):
        reset()
        source = "5{.}{1-.}while"
        resultado = evaluate(source)
        self.assertEqual('[4 3 2 1 0 0]', str(resultado))

    def test_until(self):
        reset()
        source = "5{.}{1-.}until"
        resultado = evaluate(source)
        self.assertEqual('[5]', str(resultado))
