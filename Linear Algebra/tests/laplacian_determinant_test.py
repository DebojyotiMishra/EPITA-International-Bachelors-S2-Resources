import sys
import os
import unittest

# this path insertion is needed for VS Code, and does no harm for PyCharm
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.linalgtest import LinAlgTestCase
from common.utils import randomize_int

import_exception = None
try:
    from matrix.SqMatrix import SqMatrix
    from matrix.Matrix import Matrix
except Exception as e:
    print(e)
    import_exception = e

num_tests = 10000


class SqMatrixDeterminantTestCase(LinAlgTestCase):
    def test_code_check(self):
        self.code_check(["SqMatrix", "Matrix"], import_exception)

    def test_suppress_rc(self):
        m1 = SqMatrix(((0, -3, -6, -9, -12),
                       (2, -1, -5, -7, -10),
                       (4, 1, -2, -5, -8),
                       (6, 3, 0, -3, -6),
                       (8, 5, 2, -1, -4)))
        m2 = m1.suppress_rc(1, 2)  # supress row=2, col=1
        m3 = SqMatrix(((0, -3, -9, -12),
                       (4, 1, -5, -8),
                       (6, 3, -3, -6),
                       (8, 5, -1, -4)))
        for r in range(4):
            for c in range(4):
                self.assertEqual(m2[r][c], m3[r][c])

    def test_laplacian_expansion(self):
        self.assertEqual(SqMatrix([[3]]).laplacian_expansion(), 3)
        self.assertEqual(SqMatrix([[1, 2],
                                   [3, 4]]).laplacian_expansion(), 4 - 6)
        self.assertEqual(SqMatrix([[1, 2, 3],
                                   [0, 1, -1],
                                   [1, 0, 1]]).laplacian_expansion(), -4)
        self.assertEqual(SqMatrix([[1, 2, 3],
                                   [4, 5, 6],
                                   [7, 8, 9]]).laplacian_expansion(), 0)

        self.assertEqual(SqMatrix([[1, 2, 3],
                                   [-1, 2, -1],
                                   [2, 1, 5]]).laplacian_expansion(), 2)
        self.assertEqual(SqMatrix([[5, 2, 3],
                                   [0, 2, -1],
                                   [11, 1, 5]]).laplacian_expansion(), -33)
        self.assertEqual(SqMatrix([[1, 5, 3],
                                   [-1, 0, -1],
                                   [2, 11, 5]]).laplacian_expansion(), -7)
        self.assertEqual(SqMatrix([[1, 2, 5],
                                   [-1, 2, 0],
                                   [2, 1, 11]]).laplacian_expansion(), 19)

        for dim in range(1, 7):
            for factor in [1, 2, -3]:
                self.assertEqual(SqMatrix.identity(dim).scale(factor).laplacian_expansion(),
                                 factor ** dim,
                                 f"dim={dim} factor={factor}")

    def test_determinant_diagonal(self):
        # the determinant of a diagonal matrix should be the product
        # along the diagonal
        import functools
        r = randomize_int(-10, 10)
        for dim in range(2, 7):
            tup = tuple(r() for _k in range(dim))
            m = SqMatrix.diagonal(tup)
            prod = functools.reduce(lambda a, b: a * b, tup, 1)
            self.assertAlmostEqual(prod, m.laplacian_expansion(), 3)

    def test_determinant_swapping_b(self):
        rand = randomize_int(-10, 10)
        for dim in range(2, 7):
            for r in range(100):
                m1 = SqMatrix.random(dim, rand)
                m2 = SqMatrix.random(dim, rand)
                det1 = m1.laplacian_expansion()
                det2 = m2.laplacian_expansion()
                self.assertEqual(det1 * det2, (m1 * m2).laplacian_expansion(),
                                 f"failed for \nm1={m1}\nm2={m2}")


if __name__ == '__main__':
    unittest.main()
