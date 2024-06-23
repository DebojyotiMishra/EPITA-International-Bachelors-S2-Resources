import unittest

from common.utils import randomize_int
from matrix.SqMatrix import SqMatrix
from matrix.Matrix import Matrix


# this file contains extra tests that should be added to the other unit tests.
# they are in this file at the moment, so that the students don't have surprises.


class ExtraTestCase(unittest.TestCase):
    # TODO move to SqMatrix_test.py
    def test_row_col_SqMatrix(self):
        for dim in range(2, 7):
            mat = SqMatrix.random(dim)
            self.assertEqual(mat.rows, dim)
            self.assertEqual(mat.cols, dim)
            self.assertEqual(mat.dim, dim)

    # TODO move to Matrix_test.py
    def test_row_col_Matrix(self):
        for rows in range(2, 7):
            for cols in range(2, 6):
                mat = Matrix.random(rows, cols)
                self.assertEqual(mat.rows, rows)
                self.assertEqual(mat.cols, cols)

    # TODO move to SqMatrix_test.py
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

    def test_laplacian_view(self):
        """Detect whether the student has allocated a Matrix or SqMatrix,
        which he should not have done."""
        from common.utils import randomize_float
        sqinit = SqMatrix.__init__
        minit = Matrix.__init__

        ccc = 0

        def sqalternate(self, content):
            nonlocal ccc, sqinit, minit

            ccc += 1
            sqinit(self, content)

        def malternate(self, content):
            nonlocal ccc, sqinit, minit

            ccc += 1
            minit(self, content)

        try:
            dim = 5
            m = SqMatrix.random(dim, randomizer=randomize_float(-1.0, 1.0))
            SqMatrix.__init__ = sqalternate
            Matrix.__init__ = malternate
            m.laplacian_expansion()
            assert ccc == 0, f"Computing determinant of {dim}x{dim} Expecting no allocations of SqMatrix, you've made {ccc}"
        finally:
            SqMatrix.__init__ = sqinit
            Matrix.__init__ = minit

    def test_row_vec(self):
        from matrix.Vector import Vector
        for rows in range(5, 10):
            for cols in range(5, 10):
                mat = Matrix.random(rows, cols)
                for r in range(rows):
                    v = mat.row_vec(r)
                    self.assertTrue(isinstance(v, Vector))
                    self.assertIs(v.content, mat[r])

    def test_col_vec(self):
        from matrix.Vector import Vector
        for rows in range(5, 10):
            for cols in range(5, 10):
                mat = Matrix.random(rows, cols)
                for c in range(cols):
                    v = mat.col_vec(c)
                    self.assertTrue(isinstance(v, Vector))
                    for r in range(rows):
                        self.assertEqual(v[r], mat[r][c])

    def test_find_pivot_row(self):
        from matrix.Matrix import Matrix
        m = Matrix([[100, 100, 100], [4, 5, 8], [1, 1, 0]])
        self.assertEqual(m.find_pivot_row(0), 2)
        self.assertEqual(m.find_pivot_row(1), 2)

        m = Matrix([[100, 100, 100], [1, 1, 0], [4, 5, 8]])
        self.assertEqual(m.find_pivot_row(0), 1)
        self.assertEqual(m.find_pivot_row(1), 1)
        self.assertEqual(m.find_pivot_row(2), 2)

        m = Matrix([[100, 0, 100], [1, 0, 0], [4, 0, 8]])
        self.assertEqual(m.find_pivot_row(0), 1)
        self.assertEqual(m.find_pivot_row(1), None)
        self.assertEqual(m.find_pivot_row(2), 2)

    def test_Matrix_times_Vector(self):
        from matrix.Vector import Vector
        # assert that M*v is Vector
        for dim in range(2, 7):
            mat = SqMatrix.random(dim)
            vec = Vector.random(dim)
            p = mat*vec
            self.assertTrue(isinstance(mat*vec, Vector))
            self.assertEqual(p.dim, dim)

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
        from matrix.Vector import Vector
        for dim in range(2, 7):
            for rep in range(25):
                for alpha in [1.0, 0.5, -0.5, 0.75, -0.75]:
                    m = SqMatrix.random_invertible(dim).scale(alpha)
                    if abs(m.laplacian_expansion()) < 0.001:
                        continue
                    x1 = Vector.random(dim).scale(alpha)
                    b = m*x1
                    x2 = m.gaussian_elimination_back_substitution(b)
                    self.assertLess(x1.distance(x2), 0.01)

    def test_random_cramers_rule_float(self):
        from matrix.Vector import Vector
        for alpha in [1.0, 0.5, -0.5, 0.75, -0.75]:
            for dim in range(2, 7):
                for rep in range(100):
                    m = SqMatrix.random_invertible(dim).scale(alpha)
                    if abs(m.laplacian_expansion() < 0.001):
                        continue
                    x1 = Vector.random(dim)
                    y = m.cramers_rule(x1)
                    x2 = m * y
                    self.assertLess(x1.distance(x2), 0.01)

    def test(self):
        # add test of field which will fail if 0*a != a*0 for some a
        pass

    def test_field_modulo_except_0(self):
        import random
        from structure.Field import is_field
        num_tests = 500
        def prime(k):
            """good enough prime test for small integers"""
            return not any(k % n == 0
                           for n in range(2, k - 1))

        for j in [2, 3, 5, 7, 11, 13]:
            self.assertTrue(prime(j), f"{j} is prime")
        for j in [4, 6, 8, 9, 10, 12, 14]:
            self.assertFalse(prime(j), f"{j} is non-prime")


        for k in range(2, 13):
            if not prime(k):
                continue
            for z in range(1, k):
                def plus(a, b):
                    return (a + b) % k

                def times_a(a, b):
                    # a version of field multiplication which
                    #   is not commutative for 0
                    if a == 0:
                        return z
                    return (a * b) % k

                def times_b(a,b):
                    # a version of field multiplication which
                    #   is not commutative for 0
                    if b == 0:
                        return z
                    return (a * b) % k

                zero = 0
                one = 1
                for times in [times_a, times_b]:
                    field = is_field(iterations=num_tests,
                                     add=plus,
                                     mult=times,
                                     zero=zero,
                                     one=one,
                                     additive_inverse=lambda a: next((b for b in range(k)
                                                                      if zero == plus(a, b)),
                                                                     None),
                                     multiplicative_inverse=lambda a: next((b for b in range(k)
                                                                            if one == times(a, b)),
                                                                           None),

                                     member=lambda x: isinstance(x, int) and 0 <= x < k,
                                     equivalent=lambda a, b: a == b,
                                     gen=lambda: random.randint(0, k - 1))
                    self.assertFalse(field, "0*a != a*0 is not commutative")

