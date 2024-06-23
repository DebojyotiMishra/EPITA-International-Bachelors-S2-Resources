import sys
import os
import unittest

# this path insertion is needed for VS Code, and does no harm for PyCharm
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import_exception = None
try:
    from matrix.Matrix import Matrix
    from matrix.Vector import Vector
except Exception as e:
    print(e)
    import_exception = e

from tests.linalgtest import LinAlgTestCase
from common.utils import randomize_int, randomize_float

num_tests = 1000


class MatrixTestCase(LinAlgTestCase):
    def test_code_check(self):
        self.code_check(["Matrix"], import_exception)

    def test_randomizer(self):
        for rows in range(2, 7):
            for cols in range(2, 6):
                mats = set(Matrix.random(rows, cols).content for _k in range(num_tests))
                self.assertGreater(len(mats), num_tests // 2)

    def test_factory(self):
        m1 = Matrix(((1, 2),
                     (2, -1)))
        m2 = Matrix(((1, 1, 2, 3),
                     (0, 1, -1, 4)))
        m12 = m1 * m2
        self.assertEqual(m12.rows, 2)
        self.assertEqual(m12.cols, 4)
        self.assertEqual(m12, Matrix(((1, 3, 0, 11),
                                      (2, 1, 5, 2))))

    def test_zero(self):
        for rows in range(1, 5):
            for cols in range(1, 5):
                z = Matrix.zero(rows, cols)
                for row in range(rows):
                    for col in range(cols):
                        self.assertEqual(z[row][col], 0)

    def test_add(self):
        for _ in range(num_tests):
            for rows in range(1, 6):
                for cols in range(1, 6):
                    z = Matrix.zero(rows, cols)
                    m1 = Matrix.random(rows, cols)
                    m2 = Matrix.random(rows, cols)
                    m12 = m1 + m2
                    self.assertTrue(m12.rows, rows)
                    self.assertTrue(m12.cols, cols)
                    self.assertEqual(m1 + z, m1)

    def test_subtract(self):
        for _ in range(num_tests):
            for rows in range(1, 6):
                for cols in range(1, 6):
                    z = Matrix.zero(rows, cols)
                    m1 = Matrix.random(rows, cols)
                    m2 = Matrix.random(rows, cols)
                    m12 = m1 - m2
                    self.assertTrue(m12.rows, rows)
                    self.assertTrue(m12.cols, cols)
                    self.assertEqual(m1 - m1, z)

    def test_multiply(self):
        randint = randomize_int(-10, 10)
        for r in range(num_tests):
            for k in range(1, 4):
                for rows in range(1, 4):
                    for cols in range(1, 4):
                        m1 = Matrix.tabulate(rows, k, lambda _r, _c: randint())
                        m2 = Matrix.tabulate(k, cols, lambda _r, _c: randint())
                        prod = m1 * m2
                        self.assertEqual(prod.rows, rows)
                        self.assertEqual(prod.cols, cols)
                        if rows != cols:
                            with self.assertRaises(Exception) as _cm:
                                # this should raise an exception because cannot multiply
                                # k x rows by cols x k, when rows!=cols
                                m2 * m1

    def test_transpose(self):
        randint = randomize_int(-10, 10)
        for rows in range(2, 5):
            for cols in range(2, 5):
                m = Matrix.tabulate(rows, cols, lambda _r, _c: randint())
                self.assertTrue(isinstance(m, Matrix))
                mt = m.transpose()
                self.assertTrue(isinstance(mt, Matrix))
                self.assertEqual(mt.rows, m.cols, f"m={m} mt={mt}")
                self.assertEqual(mt.cols, m.rows)
                self.assertEqual(m, mt.transpose())
                for r in range(rows):
                    for c in range(cols):
                        self.assertEqual(m[r][c], mt[c][r])

    def test_scale_random(self):
        choose_int = randomize_int(-10, 10)
        for rows in range(2, 5):
            for cols in range(2, 5):
                for r in range(num_tests):
                    m = Matrix.tabulate(rows, cols, lambda _r, _c: choose_int())
                    s1 = sum(m[r][c]
                             for r in range(rows)
                             for c in range(cols))
                    for s in range(-6, 6):
                        m2 = m.scale(s)
                        s2 = sum(m2[r][c]
                                 for r in range(rows)
                                 for c in range(cols))
                        self.assertEqual(s2, s * s1)

    def test_matrix_distance(self):
        choose_float = randomize_float(-10.0, 10.0)
        chose_epsilon = randomize_float(-0.0001, 0.0001)
        for rows in range(2, 5):
            for cols in range(2, 5):
                m = Matrix.random(rows, cols, choose_float)
                self.assertEqual(m.distance(m), 0)
                m2 = Matrix.tabulate(rows, cols, lambda r, c: m[r][c] + chose_epsilon())
                self.assertLess(m.distance(m2), 0.01)
                self.assertEqual(m.distance(m2), m2.distance(m))
                m3 = Matrix.tabulate(rows, cols,
                                     lambda r, c: m[r][c] if r < rows - 1 and c < cols - 1 else m[r][c] + 1.0)
                self.assertGreater(m.distance(m3), 0.1)

    def test_row_col_Matrix(self):
        for rows in range(2, 7):
            for cols in range(2, 6):
                mat = Matrix.random(rows, cols)
                self.assertEqual(mat.rows, rows)
                self.assertEqual(mat.cols, cols)

    def test_row_vec(self):
        for rows in range(5, 10):
            for cols in range(5, 10):
                mat = Matrix.random(rows, cols)
                for r in range(rows):
                    v = mat.row_vec(r)
                    self.assertTrue(isinstance(v, Vector))
                    self.assertIs(v.content, mat[r])

    def test_col_vec(self):
        for rows in range(5, 10):
            for cols in range(5, 10):
                mat = Matrix.random(rows, cols)
                for c in range(cols):
                    v = mat.col_vec(c)
                    self.assertTrue(isinstance(v, Vector))
                    for r in range(rows):
                        self.assertEqual(v[r], mat[r][c])


if __name__ == '__main__':
    unittest.main()
