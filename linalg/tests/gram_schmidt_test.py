import sys
import os
import unittest

# this path insertion is needed for VS Code, and does no harm for PyCharm
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.linalgtest import LinAlgTestCase
from matrix.randmat import random_invertible

import_exception = None
try:
    from structure.VectorSpace import gram_schmidt
    from matrix.Vector import Vector
    from matrix.SqMatrix import SqMatrix
except Exception as e:
    print(e)
    import_exception = e

num_tests = 1000


class GramSchmidtTestCase(LinAlgTestCase):
    def test_code_check(self):
        self.code_check(["SqMatrix", "Matrix", "Vector"], import_exception)

    def test_GramSchmidt_correct_count(self):
        for dim in range(2, 7):
            for _rep in range(num_tests):
                m = random_invertible(dim)
                v = [Vector(m[k]) for k in range(dim)]
                gs = gram_schmidt(v)
                # the correct number of vectors produced
                self.assertEqual(len(gs), dim)

    def test_GramSchmidt_first_parallel(self):
        for dim in range(2, 7):
            for _rep in range(num_tests):
                m = random_invertible(dim)
                v = [Vector(m[k]) for k in range(dim)]
                gs = gram_schmidt(v)

                # the first vector given and returned are parallel
                self.assertAlmostEqual(gs[0].angle(v[0]), 0.0, 3)

    def test_GramSchmidt_normal(self):
        for dim in range(2, 7):
            for _rep in range(num_tests):
                m = random_invertible(dim)
                v = [Vector(m[k]) for k in range(dim)]
                gs = gram_schmidt(v)

                for j in range(dim):
                    # every vector is unit length
                    self.assertAlmostEqual(gs[j].norm(), 1.0, 3)

    def test_GramSchmidt_orthogonal(self):
        epsilon = 0.0001
        for dim in range(2, 7):
            for _rep in range(num_tests):
                m = random_invertible(dim)
                v = [Vector(m[k]) for k in range(dim)]
                gs = gram_schmidt(v)

                # all the vectors returned are pairwise orthogonal
                for j in range(dim):
                    for k in range(j + 1, dim):
                        # every pair in gs is orthogonal
                        self.assertTrue(gs[j].inner_product(gs[k]) < epsilon)


if __name__ == '__main__':
    unittest.main()
