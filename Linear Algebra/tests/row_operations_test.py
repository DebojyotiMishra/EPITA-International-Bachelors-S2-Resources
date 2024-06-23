import sys
import os
import unittest

# this path insertion is needed for VS Code, and does no harm for PyCharm
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.linalgtest import LinAlgTestCase
from common.utils import randomize_int

import_exception = None
try:
    from matrix.Matrix import Matrix
    from matrix.SqMatrix import SqMatrix
    from matrix.Vector import Vector
except Exception as e:
    print(e)
    import_exception = e

num_tests = 10000


class RowOperationsTestCase(LinAlgTestCase):
    def test_code_check(self):
        self.code_check(["Matrix", "SqMatrix", "Vector"], import_exception)

    def test_replace_col(self):
        for rows in range(2, 8):
            for cols in range(2, 8):
                m1 = Matrix.random(rows, cols)

                v1 = Vector.random(rows)
                v2 = Vector.random(rows + 1)
                v3 = Vector.random(rows - 1)
                for k in range(cols):
                    with self.assertRaises(Exception) as _cm:
                        m1.replace_col(k, v2)  # should raise exception because size not compatible
                    with self.assertRaises(Exception) as _cm:
                        m1.replace_col(k, v3)  # should raise exception because size not compatible
                    m2 = m1.replace_col(k, v1)
                    for r in range(rows):
                        for c in range(cols):
                            if c == k:
                                self.assertEqual(m2[r][c], v1[r])
                            else:
                                self.assertEqual(m2[r][c], m1[r][c])

    def test_row_operation1(self):
        m1 = SqMatrix(((-5, 0, 0, 0, 3),
                       (0, 0, 0, 1, 0),
                       (1, 0, 0, 0, 0),
                       (-25820, 27400, 400, -13700, 0),
                       (5465, -5800, -85, 2900, 0)))
        s1 = -5
        r1 = 3
        s2 = 3
        r2 = 4
        m2 = m1.row_operation(s1, r1, s2, r2)
        self.assertEqual(m2, SqMatrix(((-5, 0, 0, 0, 3),
                                       (0, 0, 0, 1, 0),
                                       (1, 0, 0, 0, 0),
                                       (-25820, 27400, 400, -13700, 0),
                                       (145495, -154400, -2255, 77200, 0))))

    def test_row_operation2(self):
        m1 = SqMatrix(((0, -3, -6, -9, -12),
                       (2, -1, -4, -7, -10),
                       (4, 1, -2, -5, -8),
                       (6, 3, 0, -3, -6),
                       (8, 5, 2, -1, -4)))
        m2 = m1.row_operation(-1, 1, 2, 3)
        self.assertEqual(m2,
                         SqMatrix(((0, -3, -6, -9, -12),
                                   (2, -1, -4, -7, -10),
                                   (4, 1, -2, -5, -8),
                                   (10, 7, 4, 1, -2),
                                   (8, 5, 2, -1, -4)))
                         )

    def test_extract_rows(self):
        m1 = Matrix(((0, -3, -6, -9, -12),
                     (2, -1, -4, -7, -10),
                     (4, 1, -2, -5, -8),
                     (6, 3, 0, -3, -6),
                     (8, 5, 2, -1, -4)))
        self.assertEqual(m1.extract_rows((2, 4)),
                         Matrix((  # (0, -3, -6, -9, -12),
                             # (2, -1, -4, -7, -10),
                             (4, 1, -2, -5, -8),
                             # (6, 3, 0, -3, -6),
                             (8, 5, 2, -1, -4))))

    def test_extract_cols(self):
        m1 = Matrix(((0, -3, -6, -9, -12),
                     (2, -1, -4, -7, -10),
                     (4, 1, -2, -5, -8),
                     (6, 3, 0, -3, -6),
                     (8, 5, 2, -1, -4)))
        self.assertEqual(m1.extract_cols((2, 4)),
                         Matrix(((-6, -12),
                                 (-4, -10),
                                 (-2, -8),
                                 (0, -6),
                                 (2, -4))))

    def test_adjoin_rows(self):
        m1 = Matrix(((0, -3, -6, -9, -12),
                     (2, -1, -4, -7, -10),
                     (4, 1, -2, -5, -8)))
        m2 = Matrix(((6, 3, 0, -3, -6),
                     (8, 5, 2, -1, -4)))
        self.assertEqual(m1.adjoin_rows(m2),
                         Matrix(((0, -3, -6, -9, -12),
                                 (2, -1, -4, -7, -10),
                                 (4, 1, -2, -5, -8),
                                 (6, 3, 0, -3, -6),
                                 (8, 5, 2, -1, -4))))

    def test_rows_to_matrix(self):
        rows1 = [Vector((0, -3, -6, -9, -12)),
                 Vector((2, -1, -4, -7, -10)),
                 Vector((4, 1, -2, -5, -8))]
        rows2 = [Vector((6, 3, 0, -3, -6)),
                 Vector((8, 5, 2, -1, -4))]
        print(Matrix.rows_to_matrix(rows1).content)
        self.assertEqual(Matrix.rows_to_matrix(rows1).content, tuple(v.content for v in rows1))
        self.assertEqual(Matrix.rows_to_matrix(rows2).content, tuple(v.content for v in rows2))
        self.assertTrue(isinstance(Matrix.rows_to_matrix([Vector((1, 2)),
                                                          Vector((3, 4))]), SqMatrix))

    def test_cols_to_matrix(self):
        cols1 = (Vector((0, -3, -6, -9, -12)),
                 Vector((2, -1, -4, -7, -10)),
                 Vector((4, 1, -2, -5, -8)))
        cols2 = (Vector((6, 3, 0, -3, -6)),
                 Vector((8, 5, 2, -1, -4)))
        self.assertEqual(Matrix.cols_to_matrix(cols1).content, ((0, 2, 4),
                                                                (-3, -1, 1),
                                                                (-6, -4, -2),
                                                                (-9, -7, -5),
                                                                (-12, -10, -8)))
        self.assertEqual(Matrix.cols_to_matrix(cols2).content, ((6, 8),
                                                                (3, 5),
                                                                (0, 2),
                                                                (-3, -1),
                                                                (-6, -4)))
        self.assertTrue(isinstance(Matrix.cols_to_matrix([Vector((1, 2)),
                                                          Vector((3, 4))]), SqMatrix))

    def test_adjoin_rows_b(self):
        for rows1 in range(1, 4):
            for rows2 in range(1, 4):
                for cols in range(1, 4):
                    m1 = Matrix.random(rows1, cols)
                    m2 = Matrix.random(rows2, cols)
                    m12 = m1.adjoin_rows(m2)
                    for c in range(cols):
                        for r in range(rows1):
                            self.assertEqual(m1[r][c], m12[r][c])
                        for r in range(rows2):
                            self.assertEqual(m2[r][c], m12[r + rows1][c])

    def test_adjoin_cols(self):
        self.assertEqual(Matrix(((1, 2),
                                 (2, 3),
                                 (4, 5))).adjoin_cols(Matrix(((10, 20, 30),
                                                              (20, 30, 40),
                                                              (40, 50, 60)))),
                         Matrix(((1, 2, 10, 20, 30),
                                 (2, 3, 20, 30, 40),
                                 (4, 5, 40, 50, 60))))

    def test_adjoin_cols_b(self):
        for cols1 in range(1, 4):
            for cols2 in range(1, 4):
                for rows in range(1, 4):
                    m1 = Matrix.random(rows, cols1)
                    m2 = Matrix.random(rows, cols2)
                    m12 = m1.adjoin_cols(m2)
                    for r in range(rows):
                        for c in range(cols1):
                            self.assertEqual(m1[r][c], m12[r][c])
                        for c in range(cols2):
                            self.assertEqual(m2[r][c], m12[r][c + cols1])

    def test_adjoin_extract_cols_cols(self):
        for _ in range(num_tests):
            for rows in range(3, 5):
                for cols in range(3, 5):
                    z = Matrix.zero(rows, cols)
                    self.assertEqual(z.extract_rows(range(2)),
                                     Matrix.zero(2, cols))
                    self.assertEqual(z.extract_cols(range(2)),
                                     Matrix.zero(rows, 2))
                    r = Matrix.random(rows, cols)
                    for k in range(1, rows - 1):
                        top = r.extract_rows(range(k))
                        bottom = r.extract_rows(range(k, rows))
                        self.assertEqual(top.cols, cols)
                        self.assertEqual(top.rows, k)
                        self.assertEqual(bottom.cols, cols)
                        self.assertEqual(bottom.rows, rows - k)
                        self.assertEqual(top.adjoin_rows(bottom), r)
                    for k in range(1, cols - 1):
                        left = r.extract_cols(range(k))
                        right = r.extract_cols(range(k, cols))
                        self.assertEqual(left.rows, rows)
                        self.assertEqual(left.cols, k)
                        self.assertEqual(right.rows, rows)
                        self.assertEqual(right.cols, cols - k)
                        self.assertEqual(left.adjoin_cols(right), r)

    def test_determinant_swapping(self):
        rand = randomize_int(-10, 10)
        for dim in range(2, 7):
            for r in range(100):
                m = SqMatrix.random(dim, rand)
                det1 = m.laplacian_expansion()
                m2 = m.swap_rows(0, dim - 1)
                det2 = m2.laplacian_expansion()
                self.assertEqual(det1, -det2)

                m3 = m.swap_cols(0, dim - 1)
                det3 = m3.laplacian_expansion()
                self.assertEqual(det1, -det3)

                m4 = m.scale_row(2, dim - 1)
                det4 = m4.laplacian_expansion()
                self.assertEqual(det1 * 2, det4)

    def test_row_operation_eq(self):
        import random
        for rows in range(5, 10):
            for cols in range(2, 8):
                m1 = Matrix.random(rows, cols)

                r1 = random.randint(0, rows - 1)
                r2 = random.randint(0, rows - 1)

                a = random.randint(1, 10)
                b = random.randint(1, 10)

                m2 = m1.row_operation(a, r1, b, r2)
                for r in range(rows):
                    if r2 == r:
                        for c in range(cols):
                            self.assertEqual(m2[r2][c], a * m1[r1][c] + b * m1[r2][c])
                    else:
                        # m2[r] and m1[r] should be the same tuple, not a copies
                        self.assertIs(m2[r], m1[r], f"unaffected rows should not be copied")


if __name__ == '__main__':
    unittest.main()
