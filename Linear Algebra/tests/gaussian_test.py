import sys
import os
import unittest

# this path insertion is needed for VS Code, and does no harm for PyCharm
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.linalgtest import LinAlgTestCase
from matrix.randmat import random_invertible

import_exception = None
try:
    from matrix.Matrix import Matrix
    from matrix.SqMatrix import SqMatrix
    from matrix.Vector import Vector
except Exception as e:
    print(e)
    import_exception = e

num_tests = 10000


def is_row_echelon(m):
    k = 0
    for row in range(m.rows):
        first_non_zero = next((c for c in range(m.cols) if m[row][c] != 0),
                              m.cols)
        if k > first_non_zero:
            return False
        elif first_non_zero < row:
            return False
    return True


class SqMatrixGaussianTestCase(LinAlgTestCase):
    def test_code_check(self):
        self.code_check(["SqMatrix", "Matrix", "Vector"], import_exception)

    def test_make_row_echelon(self):
        self.assertTrue(is_row_echelon(SqMatrix(((3, 4),
                                                 (1, 2))).make_row_echelon()))

        self.assertTrue(is_row_echelon(SqMatrix(((3, 4, 3),
                                                 (1, 2, -1),
                                                 (0, 1, 1))).make_row_echelon()))
        self.assertTrue(is_row_echelon(SqMatrix(((0, -3, 0, -1, 0),
                                                 (2, 0, -4, 0, -1),
                                                 (4, 1, -2, 0, 0),
                                                 (0, 0, -4, 1, -2),
                                                 (8, 0, 0, 0, -4))).make_row_echelon()))

    def test_zeroize_singular(self):
        # an attempt to make row echelon from a non-invertible matrix should return None
        #  because it is impossible to put zeros below the diagonal without putting
        #  at least one zero on the diagonal
        self.assertIs(SqMatrix(((1, 1, 2, 3, 4),
                                (2, 0, -4, 0, -1),
                                (-2, 0, 4, 0, 1),
                                (2, 2, 4, 6, 8),
                                (8, 0, 0, 0, -4))).make_row_echelon(), None)

    def test_gaussian_elimination_back_substitution(self):
        # 2x2
        self.assertEqual(SqMatrix(((3, 4),
                                   (1, 2))).gaussian_elimination_back_substitution(Vector((1, -1))),
                         Vector((3.0, -2.0)))
        self.assertEqual(SqMatrix(((3, 4),
                                   (1, 2))) * Vector((3.0, -2.0)),
                         Vector((1, -1)))

        # 3x3
        self.assertEqual(SqMatrix(((-3, 4, 1),
                                   (1, 2, -1),
                                   (-1, 1, 2))).gaussian_elimination_back_substitution(Vector((-4, -4, 4))),
                         Vector((1, -1, 3)))
        self.assertEqual(SqMatrix(((3, 4),
                                   (1, 2))) * Vector((3.0, -2.0)),
                         Vector((1, -1)))

    def test_random_gaussian_elimination(self):
        for dim in range(2, 7):
            for rep in range(100):
                m = random_invertible(dim)
                while m.gauss_jordan_inverse() == (None, 0):
                    m = random_invertible(dim)
                x1 = Vector.random(dim)
                y = m.gaussian_elimination_back_substitution(x1)
                if y is None:
                    self.assertEqual(m.laplacian_expansion(), 0,
                                     f"gaussian_elimination_back_substitution failed on \n  x1={x1},\n  m={m},\n  y={y}")
                else:
                    x2 = m * y
                    self.assertLess(x1.distance(x2), 0.01)

    def test_cramers_rule(self):
        a = SqMatrix([[1, 2, 1],
                      [2, -1, 0],
                      [1, 1, 1]])
        b = Vector([4, 0, 2])
        x = Vector([1, 2, -1])
        self.assertEqual(a * x, b)
        a0 = a.replace_col(0, b)
        self.assertEqual(a0, SqMatrix([[4, 2, 1],
                                       [0, -1, 0],
                                       [2, 1, 1]]))
        a1 = a.replace_col(1, b)
        self.assertEqual(a1, SqMatrix([[1, 4, 1],
                                       [2, 0, 0],
                                       [1, 2, 1]]))
        a2 = a.replace_col(2, b)
        self.assertEqual(a2, SqMatrix([[1, 2, 4],
                                       [2, -1, 0],
                                       [1, 1, 2]]))
        self.assertEqual(a.laplacian_expansion(), -2)
        self.assertEqual(a0.laplacian_expansion(), -2)
        self.assertEqual(a1.laplacian_expansion(), -4)
        self.assertEqual(a2.laplacian_expansion(), 2)
        self.assertEqual(a.cramers_rule(b), x)

    def test_random_cramers_rule(self):
        for dim in range(2, 7):
            for rep in range(100):
                m = random_invertible(dim)
                x1 = Vector.random(dim)
                y = m.cramers_rule(x1)
                x2 = m * y
                self.assertLess(x1.distance(x2), 0.01)

    def test_sample_1(self):
        m = SqMatrix(((1, 2, 3),
                      (-1, 2, -1),
                      (2, 1, 5)))
        self.assertEqual(m.gaussian_elimination_back_substitution(Vector((5, 0, 11))),
                         Vector((-33 / 2, -7 / 2, 19 / 2)))

    def test_find_pivot_row(self):
        m = Matrix([[100, 100, 100],
                    [4, 5, 8],
                    [1, 1, 0]])
        self.assertEqual(m.find_pivot_row(0), 0)
        self.assertEqual(m.find_pivot_row(1), 1)

        m = Matrix([[0, -7, -4],
                    [1, 1, 0],
                    [4, -5, 8]])
        self.assertEqual(m.find_pivot_row(0), 2)
        self.assertEqual(m.find_pivot_row(1), 2)
        self.assertEqual(m.find_pivot_row(2), 2)

        m = Matrix([[0, 0, 100],
                    [1, 0, 0],
                    [-4, 0, 8]])
        self.assertEqual(m.find_pivot_row(0), 2)
        self.assertEqual(m.find_pivot_row(1), None)
        self.assertEqual(m.find_pivot_row(2), 2)

    def test_make_row_echelon_float(self):
        def is_row_echelon(m):
            k = 0
            for row in range(m.rows):
                first_non_zero = next((c for c in range(m.cols) if m[row][c] != 0),
                                      m.cols)
                if k > first_non_zero:
                    return False
                elif first_non_zero < row:
                    return False
            return True

        for alpha in [1.0, 0.5, -0.5, 0.75, -0.75]:
            self.assertTrue(is_row_echelon(SqMatrix(((3, 4),
                                                     (1, 2))).scale(alpha).make_row_echelon()))

            self.assertTrue(is_row_echelon(SqMatrix(((3, 4, 3),
                                                     (1, 2, -1),
                                                     (0, 1, 1))).scale(alpha).make_row_echelon()))
            self.assertTrue(is_row_echelon(SqMatrix(((0, -3, 0, -1, 0),
                                                     (2, 0, -4, 0, -1),
                                                     (4, 1, -2, 0, 0),
                                                     (0, 0, -4, 1, -2),
                                                     (8, 0, 0, 0, -4))).scale(alpha).make_row_echelon()))

    def test_random_gaussian_elimination_float(self):
        for dim in range(2, 7):
            for rep in range(25):
                for alpha in [1.0, 0.5, -0.5, 0.75, -0.75]:
                    m = random_invertible(dim).scale(alpha)
                    while m.gauss_jordan_inverse() == (None, 0):
                        m = random_invertible(dim)
                    if abs(m.laplacian_expansion()) < 0.001:
                        continue
                    x1 = Vector.random(dim).scale(alpha)
                    b = m * x1
                    x2 = m.gaussian_elimination_back_substitution(b)
                    self.assertLess(x1.distance(x2), 0.01)

    def test_random_cramers_rule_float(self):
        for alpha in [1.0, 0.5, -0.5, 0.75, -0.75]:
            for dim in range(2, 7):
                for rep in range(100):
                    m = random_invertible(dim).scale(alpha)
                    if abs(m.laplacian_expansion() < 0.001):
                        continue
                    x1 = Vector.random(dim)
                    y = m.cramers_rule(x1)
                    x2 = m * y
                    self.assertLess(x1.distance(x2), 0.01)


if __name__ == '__main__':
    unittest.main()
