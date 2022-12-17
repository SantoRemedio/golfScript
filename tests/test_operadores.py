import unittest
from evaluador import evaluar, reset


class TestBasico(unittest.TestCase):
    def test_add(self):
        reset()
        source = "1 2+"
        resultado = evaluar(source)
        self.assertEqual("[3]", str(resultado))

    def test_concat(self):
        reset()
        source = "'a' 'b'+"
        resultado = evaluar(source)
        self.assertEqual('["ab"]', str(resultado))

    def test_tail(self):
        reset()
        source = "'abc')"
        resultado = evaluar(source)
        self.assertEqual('["ab" 99]', str(resultado))

    def test_subtract(self):
        reset()
        source = "5 2-"
        resultado = evaluar(source)
        self.assertEqual("[3]", str(resultado))

    def test_multiplyt(self):
        reset()
        source = "5 2*"
        resultado = evaluar(source)
        self.assertEqual("[10]", str(resultado))

    def test_div(self):
        reset()
        source = "5 2/"
        resultado = evaluar(source)
        self.assertEqual("[2]", str(resultado))

    def test_power(self):
        reset()
        source = "5 2?"
        resultado = evaluar(source)
        self.assertEqual("[25]", str(resultado))

    def test_dec_1(self):
        reset()
        source = "5("
        resultado = evaluar(source)
        self.assertEqual("[4]", str(resultado))

    def test_dinc_1(self):
        reset()
        source = "5)"
        resultado = evaluar(source)
        self.assertEqual("[6]", str(resultado))

    def test_swap(self):
        reset()
        source = "1 2 3 4\\"
        resultado = evaluar(source)
        self.assertEqual("[1 2 4 3]", str(resultado))

    def test_dup_n(self):
        reset()
        source = "1 2 3 4 1$"
        resultado = evaluar(source)
        self.assertEqual("[1 2 3 4 3]", str(resultado))

    def test_dup_n_string(self):
        reset()
        source = "'asdf'$"
        resultado = evaluar(source)
        self.assertEqual('["adfs"]', str(resultado))

    def test_rotate(self):
        reset()
        source = "1 2 3 4@"
        resultado = evaluar(source)
        self.assertEqual("[1 3 4 2]", str(resultado))

    def test_cola(self):
        reset()
        source = "'123 45'~"
        resultado = evaluar(source)
        self.assertEqual("[123 45]", str(resultado))

    def test_module(self):
        reset()
        source = "10 3%"

        resultado = evaluar(source)
        self.assertEqual("[1]", str(resultado))

    def test_dup(self):
        reset()
        source = "10."

        resultado = evaluar(source)
        self.assertEqual("[10 10]", str(resultado))

    def test_chancho_integer(self):
        reset()
        source = "5~"
        resultado = evaluar(source)
        self.assertEqual("[-6]", str(resultado))

    def test_chancho_string(self):
        reset()
        source = "'1 2+'~"
        resultado = evaluar(source)
        self.assertEqual("[3]", str(resultado))

    def test_chancho_block(self):
        reset()
        source = "{1 2+}~"
        resultado = evaluar(source)
        self.assertEqual("[3]", str(resultado))

    def test_chancho_list(self):
        reset()
        source = "[1 2 3]~"
        resultado = evaluar(source)
        self.assertEqual("[1 2 3]", str(resultado))

    def test_suma_list(self):
        reset()
        source = "[1 2 3]~++"
        resultado = evaluar(source)
        self.assertEqual("[6]", str(resultado))

    def test_concatena_bloques(self):
        reset()
        source = "{a}{b}+"
        resultado = evaluar(source)
        self.assertEqual("[{a b}]", str(resultado))

    def test_not_Integer_1(self):
        reset()
        source = "1!"
        resultado = evaluar(source)
        self.assertEqual("[0]", str(resultado))

    def test_not_Integer_0(self):
        reset()
        source = "0!"
        resultado = evaluar(source)
        self.assertEqual("[1]", str(resultado))

    def test_not_List(self):
        reset()
        source = "[1]!"
        resultado = evaluar(source)
        self.assertEqual("[0]", str(resultado))

    def test_not_List_empty(self):
        reset()
        source = "[]!"
        resultado = evaluar(source)
        self.assertEqual("[1]", str(resultado))

    def test_List_empty(self):
        reset()
        source = "[]"
        resultado = evaluar(source)
        self.assertEqual("[[]]", str(resultado))

    def test_repr(self):
        reset()
        source = "1`"
        resultado = evaluar(source)
        self.assertEqual('["1"]', str(resultado))

    def test_coerce(self):
        reset()
        source = "'asdf'{1234}+"
        resultado = evaluar(source)
        self.assertEqual('[{asdf 1234}]', str(resultado))

    def test_negativos(self):
        reset()
        source = "1 -3"
        resultado = evaluar(source)
        self.assertEqual('[1 -3]', str(resultado))

    def test_negativos2(self):
        reset()
        source = "1 2-3+"
        resultado = evaluar(source)
        self.assertEqual('[1 -1]', str(resultado))

    def test_negativos3(self):
        reset()
        source = "1 2 -3+"
        resultado = evaluar(source)
        self.assertEqual('[1 -1]', str(resultado))

    def test_resta_block(self):
        reset()
        source = "[5 2 5 4 1 1][1 2]-"
        resultado = evaluar(source)
        self.assertEqual('[[5 5 4]]', str(resultado))

    def test_mult_string(self):
        reset()
        source = "'abc'3*"
        resultado = evaluar(source)
        self.assertEqual('["abcabcabc"]', str(resultado))

    def test_mult_string2(self):
        reset()
        source = "3'abc'*"
        resultado = evaluar(source)
        self.assertEqual('["abcabcabc"]', str(resultado))

    def test_mult_list(self):
        reset()
        source = "[1 2 3]3*"
        resultado = evaluar(source)
        self.assertEqual('[[1 2 3 1 2 3 1 2 3]]', str(resultado))

    def test_mult_list_string(self):
        reset()
        source = "[1 2 3]','*"
        resultado = evaluar(source)
        self.assertEqual('["1,2,3"]', str(resultado))

    def test_mult_list_list(self):
        reset()
        source = "[1 2 3][4]*"
        resultado = evaluar(source)
        self.assertEqual('[[1 4 2 4 3]]', str(resultado))

    def test_mult_int_list(self):
        reset()
        source = "3 [4]*"
        resultado = evaluar(source)
        self.assertEqual('[[4 4 4]]', str(resultado))

    def test_xor_logico_true(self):
        reset()
        source = "0 [3] xor"

        resultado = evaluar(source)
        self.assertEqual('[[3]]', str(resultado))

    def test_xor_logico_false(self):
        reset()
        source = "1 [3] xor"

        resultado = evaluar(source)
        self.assertEqual('[0]', str(resultado))

    def test_mult_string_string(self):
        reset()
        source = "'asdf'' '*"
        resultado = evaluar(source)
        self.assertEqual('["a s d f"]', str(resultado))

    def test_mult_list_block(self):
        reset()
        source = "[1 2 3 4]{+}*"
        resultado = evaluar(source)
        self.assertEqual('[10]', str(resultado))

    def test_mult_list_block(self):
        reset()
        source = "'asdf'{+}*"
        resultado = evaluar(source)
        self.assertEqual('[414]', str(resultado))

    def test_inc_list(self):
        reset()
        source = "[1 2 3])"
        resultado = evaluar(source)
        self.assertEqual('[[1 2] 3]', str(resultado))

    def test_dec_list(self):
        reset()
        source = "[1 2 3]("
        resultado = evaluar(source)
        self.assertEqual('[[2 3] 1]', str(resultado))

    def test_power_list(self):
        reset()
        source = "4[5 5 4 1 2 3]?"
        resultado = evaluar(source)
        self.assertEqual('[2]', str(resultado))

    def test_power_list_s(self):
        reset()
        source = "'a' [5 5 'a' 1 2 3]?"
        resultado = evaluar(source)
        self.assertEqual('[2]', str(resultado))

    def test_power_list_list(self):
        reset()
        source = "[6 7] [5 5 'a' [6 7] 1 2 3]?"
        resultado = evaluar(source)
        self.assertEqual('[3]', str(resultado))

    def test_power_list_no(self):
        reset()
        source = "[6] [5 5 'a' [6 7] 1 2 3]?"
        resultado = evaluar(source)
        self.assertEqual('[-1]', str(resultado))

    def test_greater_int_int(self):
        reset()
        source = "1 2>"
        resultado = evaluar(source)
        self.assertEqual('[0]', str(resultado))

    def test_greater_int_int2(self):
        reset()
        source = "3 2>"
        resultado = evaluar(source)
        self.assertEqual('[1]', str(resultado))

    def test_greater_str_str(self):
        reset()
        source = "'def' 'abc'>"
        resultado = evaluar(source)
        self.assertEqual('[1]', str(resultado))

    def test_greater_str_str2(self):
        reset()
        source = "'abc' 'def' >"
        resultado = evaluar(source)
        self.assertEqual('[0]', str(resultado))

    def test_greater_list(self):
        reset()
        source = "[1 2 3 4 5] 2 >"
        resultado = evaluar(source)
        self.assertEqual('[[3 4 5]]', str(resultado))

    def test_greater_list_menos(self):
        reset()
        source = "[1 2 3 4 5] -2 >"
        resultado = evaluar(source)
        self.assertEqual('[[4 5]]', str(resultado))

    def test_greater_block(self):
        reset()
        source = "{abcd} 2 >"
        resultado = evaluar(source)
        self.assertEqual('[{cd}]', str(resultado))

    def test_xor_int(self):
        reset()
        source = "419 234^"
        resultado = evaluar(source)
        self.assertEqual('[329]', str(resultado))

    def test_xor_array(self):
        reset()
        source = "[1 1 2 2][1 3]^"
        resultado = evaluar(source)
        self.assertEqual('[[2 3]]', str(resultado))

    def test_if(self):
        reset()
        source = "1 2 3 if"
        resultado = evaluar(source)
        self.assertEqual('[2]', str(resultado))

    def test_if_false(self):
        reset()
        source = "0 2 3 if"
        resultado = evaluar(source)
        self.assertEqual('[3]', str(resultado))

    def test_do(self):
        reset()
        source = "5{1-..}do"
        resultado = evaluar(source)
        self.assertEqual('[4 3 2 1 0 0]', str(resultado))

    def test_while(self):
        reset()
        source = "5{.}{1-.}while"
        resultado = evaluar(source)
        self.assertEqual('[4 3 2 1 0 0]', str(resultado))

    def test_until(self):
        reset()
        source = "5{.}{1-.}until"
        resultado = evaluar(source)
        self.assertEqual('[5]', str(resultado))

    def test_list_str_sum(self):
        reset()
        source = "[50]'23'+"
        resultado = evaluar(source)
        self.assertEqual('["223"]', str(resultado))

    def test_array_str(self):
        reset()
        source = "[50 'a']'23'+"
        resultado = evaluar(source)
        self.assertEqual('["2a23"]', str(resultado))

    def test_array_block(self):
        reset()
        source = "[50 'x']{3}+"
        resultado = evaluar(source)
        self.assertEqual("[{50 x 3}]", str(resultado))

    def test_array_sort(self):
        reset()
        source = '[3 2 1]$'
        resultado = evaluar(source)
        self.assertEqual('[[1 2 3]]', str(resultado))

    def test_block_sort(self):
        reset()
        source = "[1 2 3 4 5]{-1*}$"
        resultado = evaluar(source)
        self.assertEqual('[[5 4 3 2 1]]', str(resultado))

    def test_array_extraccion(self):
        reset()
        source = "[1 2 3 4 5]2/"
        resultado = evaluar(source)
        self.assertEqual('[[[1 2] [3 4] [5]]]', str(resultado))

    def test_evaluar_condicion(self):
        reset()
        source = "1 100 <"
        resultado = evaluar(source)
        self.assertEqual("[1]", str(resultado))

    def test_op_coma_int(self):
        reset()
        source = "10,"
        resultado = evaluar(source)
        self.assertEqual("[[0 1 2 3 4 5 6 7 8 9]]", str(resultado))

    def test_op_coma_array(self):
        reset()
        source = "10,,"
        resultado = evaluar(source)
        self.assertEqual("[10]", str(resultado))

    def test_op_coma_map(self):
        reset()
        source = "10,{3%},"
        resultado = evaluar(source)
        self.assertEqual("[[1 2 4 5 7 8]]", str(resultado))

    def test_or(self):
        reset()
        source = "5 3|"
        resultado = evaluar(source)
        self.assertEqual("[7]", str(resultado))

    def test_equal_array(self):
        reset()
        source = "[10 20 30]2="
        resultado = evaluar(source)
        self.assertEqual("[30]", str(resultado))

    def test_equal_array_out(self):
        reset()
        source = "[10 20 30]4="
        resultado = evaluar(source)
        self.assertEqual("[]", str(resultado))

    def test_div_array_array(self):
        reset()
        source = "[ 0 1 2 3 4 5 3 2 3 6] [2 3]/"
        resultado = evaluar(source)
        self.assertEqual("[[[0 1] [4 5 3] [6]]]", str(resultado))

    def test_zip(self):
        reset()
        source = "[[1 2 3][4 5 6][7 8 9]]zip"
        resultado = evaluar(source)
        self.assertEqual("[[[1 4 7] [2 5 8] [3 6 9]]]", str(resultado))

    def test_div_array_bloque(self):
        reset()
        source = "[1 2 3]{1+}/"
        resultado = evaluar(source)
        self.assertEqual("[2 3 4]", str(resultado))

    def test_mod_str_str(self):
        reset()
        source = "'assdfs' 's'% "
        resultado = evaluar(source)
        self.assertEqual('[["a" "df"]]', str(resultado))

    def test_redefinir(self):
        reset()
        source = "1:0;0"

        resultado = evaluar(source)
        self.assertEqual("[1]", str(resultado))

    def test_zip_strings(self):
        reset()
        source = "['asdf''1234']zip"

        resultado = evaluar(source)
        self.assertEqual('[["a1" "s2" "d3" "f4"]]', str(resultado))

    def test_zip_strings3(self):
        reset()
        source = "['abcd' 'efgh' 'klkd']zip"

        resultado = evaluar(source)
        self.assertEqual('[["aek" "bfl" "cgk" "dhd"]]', str(resultado))

    def test_zip_arrays(self):
        reset()
        source = "[[1 2 3][4 5 6][7 8 9]]zip"

        resultado = evaluar(source)
        self.assertEqual('[[[1 4 7] [2 5 8] [3 6 9]]]', str(resultado))

    def test_random(self):
        reset()
        source = "10rand"

        resultado = evaluar(source)
        print(resultado)

    def test_array_formation(self):
        reset()
        source = r"1 2 [\]"

        resultado = evaluar(source)
        self.assertEqual("[[2 1]]", str(resultado))

    def test_repr2(self):
        reset()
        source = r'"a\nb"'

        resultado = evaluar(source)
        self.assertEqual(r'["a\nb"]', str(resultado))

    def test_repr3(self):
        reset()
        source = r"[1 [2] 'asdf']`"

        resultado = evaluar(source)
        self.assertEqual(r'["[1 [2] \"asdf\"]"]', str(resultado))

    def test_repr4(self):
        reset()
        source = r'"1"`'

        resultado = evaluar(source)
        self.assertEqual(r'["\"1\""]', str(resultado))

    def test_n(self):
        reset()
        source = "n"
        resultado = evaluar(source)
        self.assertEqual(r'["\n"]', str(resultado))

    def test_slash_n(self):
        reset()
        source = r"'\n'"
        resultado = evaluar(source)
        res = str(resultado)
        self.assertEqual(r'["\\n"]', res)

    def test_slash_n_doble(self):
        reset()
        source = r'"\n"'
        resultado = evaluar(source)
        self.assertEqual(r'["\n"]', str(resultado))

    def test_int_bloque_mult(self):
        reset()
        source = r'1 2 3 {!}*'

        resultado = evaluar(source)
        res = str(resultado)
        self.assertEqual("[1 0]", res)

    def test_int_bloque_mult2(self):
        reset()
        source = r'1 2 3 4 5 {!}*'

        resultado = evaluar(source)
        res = str(resultado)
        self.assertEqual("[1 2 3 0]", res)

    def test_array_string_mult(self):
        reset()
        source = "[1 [2] [3 [4 [5]]]]'-'*"
        resultado = evaluar(source)
        res = str(resultado)
        self.assertEqual(r'["1-\x02-\x03\x04\x05"]', res)

    def test_multilinea(self):
        reset()
        source = "1\n2\n+"
        resultado = evaluar(source)
        self.assertEqual("[3]", str(resultado))
