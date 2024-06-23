import sys
import os
import unittest

# this path insertion is needed for VS Code, and does no harm for PyCharm
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.linalgtest import LinAlgTestCase
from common.utils import randomize_float

import_exception = None
try:
    from structure.VectorSpace import is_norm
    from matrix.Vector import Vector
except Exception as e:
    print(e)
    import_exception = e

num_tests = 1000

default_rand_float = randomize_float(-100.0, 100.0)


class VectorNormTestCase(LinAlgTestCase):
    def test_code_check(self):
        self.code_check(["Vector", "VectorSpace"], import_exception)

    def test_num_iterations(self):
        for k in range(1000, 1010):
            n1 = 1
            n2 = 1
            n3 = 1

            def scale(s, v):
                nonlocal n1
                n1 += 1
                return v.scale(s)

            def add(u, v):
                nonlocal n2
                n2 += 1
                return u + v

            def norm(v) -> float:
                nonlocal n3
                n3 += 1
                return v.norm()

            def gen():
                return Vector.random(4, default_rand_float)

            is_norm(norm,
                    add,
                    scale,
                    Vector.zero(4),
                    gen,
                    k)
            self.assertGreaterEqual(n1, k)
            self.assertGreaterEqual(n2, k)
            self.assertGreaterEqual(n3, k)

    def test_is_norm(self):
        for dim in range(2, 7):
            def gen():
                return Vector.random(dim, default_rand_float)

            self.assertTrue(is_norm(lambda v: v.norm(),
                                    lambda u, v: u + v,
                                    lambda s, v: v.scale(s),
                                    Vector.zero(dim),
                                    gen,
                                    num_tests
                                    ))

    def test_is_norm_b(self):
        for dim in range(2, 7):
            def gen():
                return Vector.random(dim, default_rand_float)

            zero = Vector.zero(dim)
            for p in range(1, 5):
                self.assertTrue(is_norm(lambda v: sum(abs(v[k]) ** p for k in range(dim)) ** (1 / p),
                                        lambda u, v: u + v,
                                        lambda s, v: v.scale(s),
                                        zero,
                                        gen,
                                        num_tests
                                        ))

    def test_is_norm_c(self):
        for dim in range(2, 7):
            def gen():
                return Vector.random(dim, default_rand_float)

            zero = Vector.zero(dim)
            self.assertTrue(is_norm(lambda v: sum(abs(v[k]) for k in range(dim)),
                                    lambda u, v: u + v,
                                    lambda s, v: v.scale(s),
                                    zero,
                                    gen,
                                    num_tests
                                    ))


if __name__ == '__main__':
    unittest.main()
