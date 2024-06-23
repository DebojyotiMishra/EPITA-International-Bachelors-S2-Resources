import sys
import os
import unittest
from functools import reduce
import random

# this path insertion is needed for VS Code, and does no harm for PyCharm
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.linalgtest import LinAlgTestCase

import_exception = None
try:
    from structure.Group import is_group, is_abelian_group
    from matrix.SqMatrix import SqMatrix
except Exception as e:
    print(e)
    import_exception = e

num_tests = 1000


class GroupTestCase(LinAlgTestCase):
    def test_code_check(self):
        self.code_check(["Group", "SqMatrix", "Matrix"], import_exception)

    def test_num_iterations(self):
        order = 5
        for k in range(100, 110):
            n1 = 1
            n2 = 1

            def plus(a, b):
                nonlocal n1
                n1 += 1
                return (a + b) % order

            def inverse(a):
                nonlocal n2
                n2 += 1
                return next((b for b in range(k) if 0 == plus(a, b)), None)

            self.assertTrue(is_abelian_group(iterations=k,
                                             member=lambda x: isinstance(x, int) and 0 <= x < order,
                                             op=plus,
                                             identity=0,
                                             inverse=inverse,
                                             equivalent=lambda a, b: a == b,
                                             gen=lambda: random.randint(0, order - 1)))
            self.assertGreaterEqual(n1, k)
            self.assertGreaterEqual(n2, k)

    def test_group_modulo(self):
        for k in range(2, 10):
            def plus(a, b):
                return (a + b) % k

            def times(a, b):
                return (a * b) % k

            self.assertTrue(is_abelian_group(iterations=num_tests,
                                             member=lambda x: isinstance(x, int) and 0 <= x < k,
                                             op=plus,
                                             identity=0,
                                             inverse=lambda a: next((b for b in range(k) if 0 == plus(a, b)), None),
                                             equivalent=lambda a, b: a == b,
                                             gen=lambda: random.randint(0, k - 1)))
            self.assertFalse(is_group(iterations=num_tests,
                                      member=lambda x: isinstance(x, int) and 0 <= x < k,
                                      op=times,
                                      identity=1,
                                      inverse=lambda a: next((b for b in range(k) if 0 == times(a, b)), None),
                                      equivalent=lambda a, b: a == b,
                                      gen=lambda: random.randint(0, k - 1)))

    def test_group_prime_modulo(self):
        def test(k, expect):
            def times(a, b):
                return (a * b) % k

            self.assertEqual(expect, is_group(iterations=num_tests,
                                              member=lambda x: isinstance(x, int) and 0 < x < k,
                                              op=times,
                                              identity=1,
                                              inverse=lambda a: next((b for b in range(k)
                                                                      if 1 == times(a, b)),
                                                                     None),
                                              equivalent=lambda a, b: a == b,
                                              gen=lambda: random.randint(1, k - 1)))

        for k in [2, 3, 5, 7, 11]:
            # integers modulo prime is a multiplicative group
            test(k, True)
        for k in [4, 6, 8, 9, 10, 12]:
            # integers modulo composite is not a multiplicative group
            test(k, False)

    def test_group_int(self):
        self.assertTrue(is_abelian_group(iterations=num_tests,
                                         member=lambda x: isinstance(x, int),
                                         op=lambda a, b: a + b,
                                         identity=0,
                                         inverse=lambda a: -a,
                                         equivalent=lambda a, b: a == b,
                                         gen=lambda: random.randint(0, 2 ^ 63 - 1)))

    def test_group_matrix(self):

        self.assertTrue(is_abelian_group(iterations=num_tests,
                                         member=lambda x: isinstance(x, SqMatrix) and x.dim == 2,
                                         op=lambda a, b: a + b,
                                         identity=SqMatrix.zero(2),
                                         inverse=lambda a: a.scale(-1),
                                         equivalent=lambda a, b: a == b,
                                         gen=lambda: SqMatrix.random(2)))
        self.assertFalse(is_group(iterations=num_tests,
                                  member=lambda x: isinstance(x, SqMatrix) and x.dim == 2,
                                  op=lambda a, b: a * b,
                                  identity=SqMatrix.identity(2),
                                  inverse=lambda a: a.gauss_jordan_inverse()[0],
                                  equivalent=lambda a, b: a == b,
                                  gen=lambda: SqMatrix.random(2)))

    def test_non_associative(self):
        def op(a, b):
            if a == b:
                return 'a'
            else:
                return a

        population = ['a', 'b', 'c']
        # not associative,
        self.assertFalse(is_group(iterations=num_tests,
                                  member=lambda x: x in population,
                                  op=op,
                                  identity='a',
                                  inverse=lambda a: a,
                                  equivalent=lambda a, b: a == b,
                                  gen=lambda: random.choice(population)))

    def test_non_abelian(self):
        from math import cos, sin, pi

        def closest(x):
            if abs(x) < 0.5:
                return 0
            elif x > 0:
                return 1
            else:
                return -1

        identity = SqMatrix.identity(3)
        rx = SqMatrix(((-1, 0, 0),
                       (0, 1, 0),
                       (0, 0, 1)))
        ry = SqMatrix(((1, 0, 0),
                       (0, -1, 0),
                       (0, 0, 1)))
        # first we compute all the 90 degree rotations and reflections,
        # but some of these are duplicates; so below, remove duplicates
        over_population = [SqMatrix(((c, -s, 0),
                                     (s, c, 0),
                                     (0, 0, 1))) * f
                           for x in [0, 90, 180, 270]
                           for f in [identity, rx, ry]
                           for r in [x * pi / 180]
                           for c in [closest(cos(r))]
                           for s in [closest(sin(r))]
                           ]

        self.assertEqual(len(over_population), 12)
        self.assertTrue(SqMatrix.identity(3) in over_population)

        # remove duplicates
        population = reduce(lambda acc, item: acc if item in acc else acc + [item],
                            over_population,
                            [])
        self.assertEqual(len(population), 8)

        def inverse(a):
            for m in population:
                if m * a == identity:
                    return m
            return None

        kwargs = dict(iterations=num_tests,
                      member=lambda x: x in population,
                      op=lambda a, b: a * b,
                      identity=identity,
                      inverse=inverse,
                      equivalent=lambda a, b: a == b,
                      gen=lambda: random.choice(population))
        # the group of rotations and reflections in the plane is a group
        self.assertTrue(is_group(**kwargs))
        # but it is not abelian
        self.assertFalse(is_abelian_group(**kwargs))


if __name__ == '__main__':
    unittest.main()
