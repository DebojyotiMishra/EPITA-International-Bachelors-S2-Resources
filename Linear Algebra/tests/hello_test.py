import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.linalgtest import LinAlgTestCase

import_exception = None
try:
    from matrix.hello import *
except Exception as e:
    print(e)
    import_exception = e


num_repetitions = 50
test_size = 10


class HelloTestCase(LinAlgTestCase):
    def test_code_check(self):
        self.code_check(["hello"], import_exception)

    def test_hello_0(self):
        self.assertEqual(hello("jim"), "Hello, jim.")

    def test_hello_1(self):
        for k in range(100):
            name = f"{k}"
            h = hello(name)
            self.assertTrue(h.startswith("Hello,"))
            self.assertTrue(h.endswith(name + "."))
            self.assertEqual(h, "Hello, " + name + ".")


if __name__ == '__main__':
    import unittest

    unittest.main()
