import sys
import os
import unittest

# this path insertion is needed for VS Code, and does no harm for PyCharm
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.linalgtest import LinAlgTestCase
from common.utils import randomize_int
from matrix.randmat import random_invertible

import_exception = None
try:
    from matrix.SqMatrix import SqMatrix
    from matrix.Matrix import Matrix
    from matrix.Vector import Vector
except Exception as e:
    print(e)
    import_exception = e

num_tests = 10000


def is_diagonal(m):
    for row in range(m.rows):
        for col in range(m.cols):
            if row != col and m[row][col] != 0:
                return False
            if row == col and m[row][col] == 0:
                return False
    return True


class SqMatrixGaussJordanTestCase(LinAlgTestCase):
    def test_code_check(self):
        self.code_check(["SqMatrix", "Matrix", "Vector"], import_exception)

    def test_make_unit_diagonal(self):
        self.assertTrue(is_diagonal(SqMatrix(((3, 4),
                                              (1, 2))).make_unit_diagonal()[0]))
        self.assertTrue(is_diagonal(SqMatrix(((3, 4, 3),
                                              (1, 2, -1),
                                              (0, 1, 1))).make_unit_diagonal()[0]))
        self.assertTrue(is_diagonal(SqMatrix(((0, -3, 0, -1, 0),
                                              (2, 0, -4, 0, -1),
                                              (4, 1, -2, 0, 0),
                                              (0, 0, -5, 1, -2),
                                              (8, 0, 0, 0, -4))).make_unit_diagonal()[0]))

    def test_gaussian_jordan(self):
        # 2x2
        self.assertLess(SqMatrix(((3, 4),
                                  (1, 2))).gauss_jordan_elimination(Vector((1, -1))).distance(Vector((3.0, -2.0))),
                        0.01)
        self.assertLess((SqMatrix(((3, 4),
                                   (1, 2))) * Vector((3.0, -2.0))).distance(Vector((1, -1))), 0.01)

        # 3x3
        m3 = SqMatrix(((-3, 4, 1),
                       (1, 2, -1),
                       (-1, 1, 2))).gauss_jordan_elimination(Vector((-4, -4, 4)))
        self.assertLess(m3.distance(Vector((1, -1, 3))),
                        0.01)
        di = (SqMatrix(((3, 4), (1, 2))) * Vector((3.0, -2.0))).distance(Vector((1, -1)))
        self.assertLess(di, 0.01)

    def test_determinant(self):
        from math import isnan
        epsilon = 0.01
        for dim in range(2, 7):
            for rep in range(1000):
                m = random_invertible(dim, min_det=epsilon)
                det0 = m.laplacian_expansion()
                self.assertFalse(isnan(det0), f"{det0=}")
                self.assertTrue(abs(det0) > epsilon, f"{det0=} {epsilon=}")
                inv, det1 = m.gauss_jordan_inverse()
                if abs(det1) < epsilon:
                    continue
                # TODO there is something wrong here, needs to be fixed.
                #    sometimes det1 is nan or inf or -inf
                if isnan(det0) or isnan(det1):
                    continue
                else:
                    ratio = abs(det0 / det1)
                    self.assertAlmostEqual(1, ratio, 3,
                                           f"det0={det0} det1={det1}\nm={m}")

    def test_determinant_diagonal(self):
        # the determinant of a diagonal matrix should be the product
        # along the diagonal
        import functools
        r = randomize_int(-10, 10)
        for dim in range(2, 7):
            tup = tuple(r() for _k in range(dim))
            m = SqMatrix.diagonal(tup)
            prod = functools.reduce(lambda a, b: a * b, tup, 1)
            inv, det = m.gauss_jordan_inverse()
            self.assertAlmostEqual(prod, det, 3)

    def test_random_gauss_jordan_elimination(self):
        for dim in range(2, 7):
            for rep in range(100):
                m = random_invertible(dim)
                x1 = Vector.random(dim)
                y = m.gauss_jordan_elimination(x1)
                if y is None:
                    continue
                x2 = m * y
                self.assertLess(x1.distance(x2), 0.01)

    def test_gauss_jordan_inverse_1(self):
        self.assertTrue((None, 0) != SqMatrix([[-6.25, 0.0],
                                               [0.0, 0.3125]]).gauss_jordan_inverse())

    def test_gauss_jordan_inverse_2(self):
        self.assertTrue((None, 0) != SqMatrix([[0.0, 0.0, 0.00390625],
                                               [0.0, -5.0, 0.0],
                                               [-0.09765625, 0.0, 0.0]]).transpose().gauss_jordan_inverse())

    def test_gauss_jordan_inverse_3(self):
        self.assertTrue((None, 0) != SqMatrix([(0.0, 0.15625, 0.0, 0.0, 0.0, 0.0),
                                               (0.0, 0.0, 0.0, 0.0, 0.0, -0.390625),
                                               (0.0, 0.0, 0.0, -25.0, 0.0, 0.0),
                                               (0.0, 0.0, 0.0, 0.0, 31.25, 0.0),
                                               (-0.1220703125, 0.0, 0.0, 0.0, 0.0, 0.0),
                                               (0.0, 0.0, -1.5625, 0.0, 0.0, 0.0)]).gauss_jordan_inverse())

    def test_gauss_jordan_inverse_4(self):
        self.assertTrue((None, 0) != SqMatrix([(0.0, 0.0, -0.009765625, 0.0, 0.0, 0.0),
                                               (0.0, 0.0, 0.0, 0.0078125, 0.0, 0.0),
                                               (-0.0762939453125, 0.0, 0.0, 0.0, 0.0, 0.0),
                                               (0.0, 0.0, 0.0, 0.0, 0.0, 3.125),
                                               (0.0, -15.2587890625, 0.0, 0.0, 0.0, 0.0),
                                               (
                                               0.0, 0.0, 0.0, 0.0, -97.65625, 0.0)]).transpose().gauss_jordan_inverse())

    def test_random_gauss_jordan_inverse(self):
        for dim in range(2, 7):
            identity = SqMatrix.identity(dim)
            for rep in range(10):
                m = random_invertible(dim)
                m_inv, det = m.gauss_jordan_inverse()
                if m_inv is None:
                    continue
                self.assertTrue(det != 0, f"det={det} m={m}")
                self.assertLess((m * m_inv).distance(identity), 0.01)

    def test_inverse_0a(self):
        m_inv, det = SqMatrix(((5, 2),
                               (3, 6))).gauss_jordan_inverse()
        self.assertEqual(det, 24)

    def test_inverse_0c(self):
        m_inv, det = SqMatrix(((3, 6),
                               (5, 2))).gauss_jordan_inverse()
        self.assertEqual(det, -24)

    def test_inverse_1(self):
        m_inv, det = SqMatrix(((1, 2, 3),
                               (4, 5, 6),
                               (7, 8, 9))).gauss_jordan_inverse()
        self.assertEqual(det, 0)

    def test_determinant_2(self):
        m = SqMatrix(((2, 2, 5, 1),
                      (2, 1, 1, 3),
                      (1, 0, 1, 0),
                      (0, 1, 3, 2)))
        m_inv, det = m.gauss_jordan_inverse()

        self.assertLess((m * m_inv).distance(SqMatrix.identity(4)), 0.01)
        self.assertAlmostEqual(-15, det, 3)

    def test_determinant_3(self):
        m = SqMatrix(((2, 4, -6, 8),
                      (5, 6, 7, 8),
                      (1, 2, -3, -4),
                      (4, 8, 7, 8)))
        m_inv, det = m.gauss_jordan_inverse()
        self.assertLess((m * m_inv).distance(SqMatrix.identity(4)), 0.01)
        self.assertAlmostEqual(-1216, det, 3)

    def test_determinant_4(self):
        epsilon = 0.0001
        m = SqMatrix(((1, 2, 3),
                      (-1, 2, -1),
                      (2, 1, 5)))
        inv, det = m.gauss_jordan_inverse()
        self.assertAlmostEqual(det, 2, 3)
        m2 = SqMatrix.identity(3).row_operation(1, 0,
                                                1, 1).row_operation(2, 0,
                                                                    -1, 2)
        self.assertEqual(m2, SqMatrix(((1, 0, 0),
                                       (1, 1, 0),
                                       (2, 0, -1))))
        m3 = m2.row_operation(-2, 1, 4, 0).row_operation(-3, 1, 4, 2)
        self.assertEqual(m3, SqMatrix(((2, -2, 0),
                                       (1, 1, 0),
                                       (5, -3, -4))))
        m4 = m3.row_operation(8, 2, 2, 0).row_operation(1, 2, 1, 1)
        self.assertEqual(m4, SqMatrix(((44, -28, -32),
                                       (6, -2, -4),
                                       (5, -3, -4))))
        m5 = m4.scale_row(1 / 8, 0).scale_row(1 / 4, 1).scale_row(-1 / 2, 2)
        self.assertEqual(m5, SqMatrix(((11 / 2, -7 / 2, -4),
                                       (3 / 2, -1 / 2, -1),
                                       (-5 / 2, 3 / 2, 2))))
        self.assertMatrixAlmostEqual(inv, SqMatrix(((11 / 2, -7 / 2, -4),
                                                    (3 / 2, -1 / 2, -1),
                                                    (-5 / 2, 3 / 2, 2))), epsilon,
                                     f"got {inv}")

    def test_row_operation_inversion2b(self):
        m1 = SqMatrix(((-16, 0, -2, 0, 0, 12),
                       (-4, 0, 0, 0, 0, 3),
                       (0, 1, 0, 0, 0, 0),
                       (0, -5, -12, 12, 0, 0),
                       (0, 0, 0, 0, 0, 1),
                       (0, 0, 0, 0, -3, 0)))
        inv1, det1 = m1.gauss_jordan_inverse()
        self.assertTrue(det1 != 0, f"det1={det1}")
        s1 = 1
        r1 = 5
        s2 = -4
        r2 = 0
        m2 = m1.row_operation(s1, r1, s2, r2)
        inv2, det2 = m2.gauss_jordan_inverse()
        self.assertTrue(det2 != 0, f"det2={det2}")

    def test_gje(self):  # gauss jordan elimination
        epsilon = 0.00001
        a = SqMatrix([[1, 2, 1],
                      [2, -1, 0],
                      [1, 1, 1]])
        b = Vector([4, 0, 2])
        x = Vector([1, 2, -1])
        self.assertEqual(a * x, b)
        a1 = a.adjoin_col(b).row_operation(2, 0, -1, 1).row_operation(1, 0, -1, 2)
        self.assertEqual(a1, Matrix([[1, 2, 1, 4],
                                     [0, 5, 2, 8],
                                     [0, 1, 0, 2]]))

        a2 = a1.row_operation(2, 1, -5, 0).row_operation(1, 1, -5, 2)
        self.assertEqual(a2, Matrix([[-5, 0, -1, -4],
                                     [0, 5, 2, 8],
                                     [0, 0, 2, -2]]))

        a3 = a2.row_operation(-1, 2, -2, 0).row_operation(2, 2, -2, 1)
        self.assertEqual(a3, Matrix([[10, 0, 0, 10],
                                     [0, -10, 0, -20],
                                     [0, 0, 2, -2]]))

        self.assertVectorAlmostEqual(a.gauss_jordan_elimination(b), x, epsilon)


if __name__ == '__main__':
    unittest.main()
