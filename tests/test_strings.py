import unittest
from strings import raw_string, escaped_string


class TestBasico(unittest.TestCase):
    def test_simple(self):
        source = r"abc"
        raw = raw_string(source)
        esc = escaped_string(source)
        self.assertEqual(raw, source)
        self.assertEqual(esc, source)

    def test_comilla(self):
        source = r"ab\'"
        raw = raw_string(source)
        esc = escaped_string(source)
        self.assertEqual(raw, "ab\'")
        self.assertEqual(esc, "ab\'")

    def test_tab(self):
        source = r"a\tb"
        raw = raw_string(source)
        esc = escaped_string(source)
        self.assertEqual(r"a\tb", raw)
        self.assertEqual("a\tb", esc)

    def test_integer(self):
        source = '"1"`'
        raw = raw_string(source)
        esc = escaped_string(source)
        self.assertEqual(r'"1"`', raw)
        self.assertEqual('"1"`', esc)
        print(repr(esc))

    def test_new_line(self):
        source = r'a\nb'
        raw = raw_string(source)
        esc = escaped_string(source)
        self.assertEqual(r'a\nb', raw)
        self.assertEqual('a\nb', esc)
        print(repr(esc))

    def test_integer_s(self):
        source = '"1"'
        raw = raw_string(source)
        esc = escaped_string(source)
        self.assertEqual(r'"1"', raw)
        self.assertEqual('"1"', esc)
        print(repr(esc))
