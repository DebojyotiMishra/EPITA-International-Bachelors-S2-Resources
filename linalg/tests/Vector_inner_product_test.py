import sys
import os
import unittest

# this path insertion is needed for VS Code, and does no harm for PyCharm
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.linalgtest import LinAlgTestCase
from common.utils import randomize_float, trace
from matrix.randmat import random_invertible

import_exception = None
try:
    from matrix.SqMatrix import SqMatrix
    from structure.VectorSpace import is_inner_product
    from matrix.Vector import Vector
except Exception as e:
    print(e)
    import_exception = e

num_tests = 1000
default_rand_float = randomize_float(-100.0, 100.0)


class VectorInnerProductTestCase(LinAlgTestCase):
    def test_code_check(self):
        self.code_check(["Vector", "VectorSpace", "SqMatrix", "Matrix"], import_exception)

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

            def inner_product(v, u) -> float:
                nonlocal n3
                n3 += 1
                return v.inner_product(u)

            def gen():
                return Vector.random(4, default_rand_float)

            is_inner_product(inner_product,
                             add,
                             scale,
                             gen,
                             k)
            self.assertGreaterEqual(n1, k)
            self.assertGreaterEqual(n2, k)
            self.assertGreaterEqual(n3, k)

    def test_is_not_inner_product(self):
        for dim in range(2, 7):
            def gen():
                return Vector.random(dim, default_rand_float)

            self.assertFalse(is_inner_product(lambda u, v: 1,  # never zero
                                              lambda u, v: u + v,
                                              lambda s, v: v.scale(s),
                                              gen, 1))

            self.assertFalse(is_inner_product(lambda u, v: 0,  # always zero
                                              lambda u, v: u + v,
                                              lambda s, v: v.scale(s),
                                              gen, 1))

            self.assertFalse(is_inner_product(lambda u, v: u.inner_product(v),
                                              lambda u, v: u + v * 2,  # not linear
                                              lambda s, v: v.scale(s),
                                              gen, 1))

            self.assertFalse(is_inner_product(lambda u, v: u.inner_product(v),
                                              lambda u, v: u + v,
                                              lambda s, v: v.scale(2 * s),
                                              gen, num_tests))

            self.assertFalse(is_inner_product(lambda u, v: -1 * u.inner_product(v),
                                              lambda u, v: u + v,
                                              lambda s, v: v.scale(s),
                                              gen, num_tests))

            self.assertFalse(is_inner_product(lambda u, v: max([abs(u[k] * v[k]) for k in range(u.dim)]),
                                              lambda u, v: u + v,
                                              lambda s, v: v.scale(s),
                                              gen, num_tests))

    def test_is_inner_product(self):
        from math import isnan
        choose_float = randomize_float(0.5, 1.5)

        def scale(s, v):
            return v.scale(s)

        def add(u, v):
            return u + v

        for dim in range(2, 6):
            def gen():
                return Vector.random(dim, default_rand_float)

            for k in range(100):
                # here we construct a symmetric positive definite matrix.
                #  q is invertible, so qq is invertible and has determinate > 0
                #  so qq * qq.transpose() is symmetric, det > 0.

                p = random_invertible(dim)
                _, det = p.gauss_jordan_inverse()
                if isnan(det):
                    continue
                if det <= 0:
                    continue
                d = SqMatrix.diagonal([f for k in range(dim) for f in [choose_float()]])
                # now we create a matrix whose eigen values > 0
                #  and multiply on left and right by p and p.transpose()
                a = p * d * p.transpose()

                def inner_product(v, u) -> float:
                    # this is a valid inner product, see
                    # see https: //en.wikipedia.org/wiki/Inner_product_space
                    return v.inner_product(a * u)

                self.assertTrue(is_inner_product(inner_product, add, scale, gen, k, 1),
                                f"is_inner_product failed when \n{k=} \n{dim=}\n{d=}\n{p=}\n{a=}")
        pass


if __name__ == '__main__':
    unittest.main()
