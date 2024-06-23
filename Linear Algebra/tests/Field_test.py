import sys
import os
import unittest
import random

# this path insertion is needed for VS Code, and does no harm for PyCharm
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.linalgtest import LinAlgTestCase

import_exception = None
try:
    from structure.Field import is_field
    from matrix.SqMatrix import SqMatrix
except Exception as e:
    print(e)
    import_exception = e

num_tests = 5000
epsilon = 0.000001


def prime(k):
    """good enough prime test for small integers"""
    return not any(k % n == 0
                   for n in range(2, k - 1))


class FieldTestCase(LinAlgTestCase):
    def test_code_check(self):
        self.code_check(["Field"], import_exception)

    def test_num_iterations(self):
        for k in range(1000, 1010):
            n1 = 1
            n2 = 1
            n3 = 1
            n4 = 1

            def plus(a, b):
                nonlocal n1
                n1 += 1
                return (a + b) % 3

            def times(a, b):
                nonlocal n2
                n2 += 1
                return (a * b) % 3

            one = 1
            zero = 0

            def multiplicative_inverse(y):
                nonlocal n3
                n3 += 1
                return next((x for x in [0, 1, 2] if times(x, y) == one),
                            None)

            def additive_inverse(y):
                nonlocal n4
                n4 += 1
                return next((x for x in [0, 1, 2] if plus(x, y) == zero),
                            None)

            self.assertTrue(
                is_field(iterations=num_tests,
                         add=plus,
                         mult=times,
                         zero=zero,
                         one=one,
                         additive_inverse=additive_inverse,
                         multiplicative_inverse=multiplicative_inverse,
                         member=lambda x: isinstance(x, int) and 0 <= x < k,
                         equivalent=lambda a, b: a == b,
                         gen=lambda: random.randint(0, 3 - 1)))
            self.assertGreaterEqual(n1, k)
            self.assertGreaterEqual(n2, k)
            self.assertGreaterEqual(n3, k)
            self.assertGreaterEqual(n4, k)

    def test_field_modulo(self):

        for j in [2, 3, 5, 7, 11, 13]:
            self.assertTrue(prime(j), f"{j} is prime")
        for j in [4, 6, 8, 9, 10, 12, 14]:
            self.assertFalse(prime(j), f"{j} is non-prime")

        for k in range(2, 13):
            def plus(a, b):
                return (a + b) % k

            def times(a, b):
                return (a * b) % k

            zero = 0
            one = 1
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
            if prime(k):
                self.assertTrue(field)
            else:
                self.assertFalse(field)

    def test_complex(self):
        one = SqMatrix.identity(2)
        zero = SqMatrix.zero(2)

        def plus(a, b):
            return a + b

        def times(a, b):
            return a * b

        def gen():
            r = random.uniform(-1.0, 1.0)
            c = random.uniform(-1.0, 1.0)
            return SqMatrix(((r, -c),
                             (c, r)))

        def iii(m):
            a = m[0][0]
            b = m[0][1]
            c = m[1][0]
            d = m[1][1]
            det = a*d - b*c
            return SqMatrix([[d, -b],
                             [-c, a]]).scale(1/det)

        self.assertTrue(is_field(iterations=num_tests,
                                 add=plus,
                                 mult=times,
                                 zero=zero,
                                 one=one,
                                 additive_inverse=lambda a: a.scale(-1),
                                 multiplicative_inverse=iii,
                                 member=lambda m: isinstance(m, SqMatrix) and m.dim == 2,
                                 equivalent=lambda a, b: a.distance(b) < epsilon,
                                 gen=gen))

    def test_field_modulo_except_0(self):
        import random
        num_tests = 500

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

                def times_b(a, b):
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


if __name__ == '__main__':
    unittest.main()
