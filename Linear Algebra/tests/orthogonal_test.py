import sys
import os
import unittest

# this path insertion is needed for VS Code, and does no harm for PyCharm
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.linalgtest import LinAlgTestCase
from common.utils import randomize_float

import_exception = None
try:
    from matrix.Vector import Vector, is_orthogonal
except Exception as e:
    print(e)
    import_exception = e

num_tests = 10000


class OrthogonalTestCase(LinAlgTestCase):
    def test_code_check(self):
        self.code_check(["Vector"], import_exception)

    def test_not_orthogonal(self):
        self.assertFalse(is_orthogonal([Vector((1, 0)), Vector((2, 0))]))
        self.assertFalse(is_orthogonal([Vector((1, 1, 1)), Vector((1, 1, 1)), Vector((1, 1, 1))]))
        self.assertFalse(is_orthogonal([Vector((1, 2, 3)),
                                        Vector((4, 5, 6)),
                                        Vector((7, 8, 9))]))
        self.assertFalse(is_orthogonal([Vector((1, 0, 0)),
                                        Vector((0, 1))]))

    def test_orthogonal(self):
        rand_float = randomize_float(1.0, 2.0)
        for dim in range(2, 6):
            for j in range(dim):
                vectors = [Vector.tabulate(dim, lambda i: rand_float() if i == j else 0.0)] + \
                          [Vector.tabulate(dim, lambda i: rand_float() if i == k else 0.0)
                           for k in range(j + 1, dim)]
                self.assertTrue(is_orthogonal(vectors))

    def test_empty_vector_list(self):
        self.assertTrue(is_orthogonal([]))

    def test_singleton_vector_list(self):
        self.assertTrue(is_orthogonal([Vector((0, 1))]))


if __name__ == '__main__':
    unittest.main()
