import sys
import os
import unittest

# this path insertion is needed for VS Code, and does no harm for PyCharm
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.linalgtest import LinAlgTestCase

import_exception = None
try:
    from matrix.SqMatrix import SqMatrix
    from matrix.Vector import Vector
except Exception as e:
    print(e)
    import_exception = e

from common.utils import randomize_int

m1 = SqMatrix(((1, 2, 3),
               (2, 3, 5),
               (-1, 0, 4)))
m2 = SqMatrix(((1, 2, 3),
               (2, -3, 5),
               (-1, 0, 4)))

num_tests = 4000


class SqMatrixTestCase(LinAlgTestCase):
    def test_code_check(self):
        self.code_check(["SqMatrix", "Matrix", "Vector"], import_exception)

    def test_tabulate(self):
        def f(row, col):
            return row + 2 * col

        for dim in range(3, 6):
            m = SqMatrix.tabulate(dim, f)
            for row in range(dim):
                for col in range(dim):
                    self.assertEqual(f(row, col), m[row][col])

    def test_init(self):
        def f(row, col):
            return row + 2 * col

        for dim in range(1, 10):
            m = SqMatrix.tabulate(dim, f)
            self.assertEqual(m.dim, dim)
            for row in range(dim):
                for col in range(dim):
                    self.assertEqual(m[row][col], f(row, col))

    def test_eq(self):
        self.assertEqual(m1, m1)
        self.assertEqual(m2, m2)
        self.assertNotEqual(m1, m2)
        self.assertNotEqual(m1, SqMatrix(((1, 2),
                                          (2, 3))))
        self.assertNotEqual(SqMatrix(((1, 2),
                                      (2, 3))),
                            m1)

    def test_scale(self):
        self.assertEqual(m1 * 2, SqMatrix(((2, 4, 6),
                                           (4, 6, 10),
                                           (-2, 0, 8))))

    def test_scale_random(self):
        randint = randomize_int(-10, 10)
        for dim in range(2, 5):
            for r in range(num_tests):
                m = SqMatrix.tabulate(dim, lambda _r, _c: randint())
                s1 = sum(m[r][c]
                         for r in range(dim)
                         for c in range(dim))
                for s in range(-5, 5):
                    m2 = m.scale(s)
                    s2 = sum(m2[r][c]
                             for r in range(dim)
                             for c in range(dim))
                    self.assertEqual(s2, s * s1)

    def test_matrix_multiply1(self):
        self.assertEqual(m1 * m2, SqMatrix(((2, -4, 25),
                                            (3, -5, 41),
                                            (-5, -2, 13))))

    def test_matrix_multiply2(self):
        for dim in range(1, 5):
            mid = SqMatrix.identity(dim)
            m1 = SqMatrix.random(dim)
            m2 = SqMatrix.random(dim)
            zero = SqMatrix.zero(dim)
            self.assertEqual(m1 * mid, m1)
            self.assertEqual(mid * m1, m1)
            self.assertEqual(m2 * mid, m2)
            self.assertEqual(mid * m2, m2)
            self.assertEqual(m1 * zero, zero)
            self.assertEqual(zero * m1, zero)
            self.assertEqual(m2 * zero, zero)
            self.assertEqual(zero * m2, zero)

    def test_matrix_mult_2(self):
        for _ in range(num_tests):
            for dim in range(3, 6):
                m = SqMatrix.random(dim)
                zero = SqMatrix.zero(dim)
                mid = SqMatrix.identity(dim)
                self.assertEqual(zero * m, zero)
                self.assertEqual(m * zero, zero)
                self.assertEqual(m * mid, m)
                self.assertEqual(mid * m, m)

    def test_matrix_sum(self):
        for _ in range(num_tests):
            for dim in range(3, 6):
                m1 = SqMatrix.random(dim)
                m2 = SqMatrix.random(dim)
                m3 = SqMatrix.random(dim)
                zero = SqMatrix.zero(dim)
                self.assertEqual(m1 + m2, m2 + m1)
                self.assertEqual(m1 + zero, m1)
                self.assertEqual(zero + m1, m1)
                self.assertEqual(m1 + (m2 + m3), (m1 + m2) + m3)

    def test_sub(self):
        mid = SqMatrix.identity(3)
        zero = SqMatrix.zero(3)
        self.assertEqual(zero - zero, zero, f"zero={zero}")
        self.assertEqual(mid + (zero * -1), mid)
        self.assertEqual(mid - zero, mid)
        self.assertEqual(m1 - zero, m1)
        self.assertEqual(m2 - zero, m2)
        self.assertEqual(zero - m2, m2 * -1)
        self.assertEqual(zero - m1, m1 * -1)
        self.assertEqual(m1 - m2, SqMatrix(((0, 0, 0),
                                            (0, 6, 0),
                                            (0, 0, 0))))
        for _ in range(num_tests):
            for dim in range(3, 6):
                m3 = SqMatrix.random(dim)
                zero = SqMatrix.zero(dim)
                self.assertEqual(m3 - m3, zero)
                self.assertEqual(m3 + m3 - m3 - m3, zero)
                self.assertEqual(m3 + m3 * -1, zero)

    def test_zero(self):
        for dim in range(1, 5):
            z = SqMatrix.zero(dim)
            for row in range(dim):
                for col in range(dim):
                    self.assertEqual(z[row][col], 0)

    def test_ident(self):
        for dim in range(1, 5):
            z = SqMatrix.identity(dim)
            for row in range(dim):
                for col in range(dim):
                    if row == col:
                        self.assertEqual(z[row][col], 1)
                    else:
                        self.assertEqual(z[row][col], 0)

    def test_power(self):
        for dim in range(1, 5):
            I = SqMatrix.identity(dim)
            for p in range(10):
                self.assertEqual(I, I.power(p))
            Z = SqMatrix.zero(dim)
            for p in range(1, 10):
                self.assertEqual(Z, Z.power(p))
            m = SqMatrix.random(dim)
            for p in range(0, 10):
                mp = m.power(p)
                self.assertEqual(mp * m, m.power(p + 1))
                self.assertEqual(mp * mp, m.power(2 * p))
            # TODO -- test that powers commute M^p * M^q = M^q * M^p
            # test M^p + M^q = M^p(I+M^(q-p)) when q > p

    def test_acquaintance_graph(self):
        A = SqMatrix(((1, 1, 0, 0, 0, 0),
                      (0, 1, 1, 0, 1, 0),
                      (1, 0, 1, 0, 0, 0),
                      (1, 1, 0, 1, 0, 0),
                      (1, 1, 0, 0, 1, 1),
                      (0, 0, 1, 1, 0, 1)))
        self.assertEqual(A.power(0)[2][5], 0)
        self.assertEqual(A.power(1)[2][5], 0)
        self.assertEqual(A.power(2)[2][5], 0)
        self.assertEqual(A.power(3)[2][5], 0)
        self.assertEqual(A.power(4)[2][5], 1)

    def test_row_col_SqMatrix(self):
        for dim in range(2, 7):
            mat = SqMatrix.random(dim)
            self.assertEqual(mat.rows, dim)
            self.assertEqual(mat.cols, dim)
            self.assertEqual(mat.dim, dim)

    def test_matrix_multiply_complexity(self):
        """Assert that the complexity of SqMatrix.power is approx n^3 log p,
        not p n^3
        """
        from common.utils import randomize_float, fast_power
        from math import log
        from datetime import datetime
        """Assert that matrix multiply has n^3 log n complexity or better"""
        dim = 15
        mat = SqMatrix.random(dim, randomizer=randomize_float(-1.0, 1.0))

        def time_it(f, repeat=1):
            t0 = datetime.now()
            for i in range(repeat):
                f()
            return (datetime.now() - t0).total_seconds() / repeat

        # complexity of the good algorithm is n^3 log p
        #    where p is the exponent, and n is the matrix dimension
        #    so time is some alpha * n^3 log p
        #        (where log is log base 2)
        #    here we compute alpha
        alpha = time_it(lambda: mat * mat, 100) / (dim * dim * dim)
        repeat_student_code = 3
        times = [gamma
                 for k in range(35, 40)
                 for time_student in [time_it(lambda: mat.power(k),
                                              repeat_student_code)]
                 for expected_time in [alpha * dim * dim * dim * log(k, 2.0)]
                 for gamma in [time_student / expected_time]
                 ]

        # if the code being tested has complexity n^3 log p, then this
        #  averages will be close to 1.
        avg = sum(times) / len(times)
        assert avg < 2, f"expecting n^3 log p complexity,  expecting avg={avg} < 2"

    def test_Matrix_times_Vector(self):
        # assert that M*v is Vector
        for dim in range(2, 7):
            mat = SqMatrix.random(dim)
            vec = Vector.random(dim)
            p = mat * vec
            self.assertTrue(isinstance(mat * vec, Vector))
            self.assertEqual(p.dim, dim)


if __name__ == '__main__':
    unittest.main()
