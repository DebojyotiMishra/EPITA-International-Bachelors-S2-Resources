import sys
import os
import unittest

# this path insertion is needed for VS Code, and does no harm for PyCharm
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.linalgtest import LinAlgTestCase
from common.utils import randomize_float

import_exception = None
try:
    from matrix.Vector import Vector
except Exception as e:
    print(e)
    import_exception = e

num_tests = 10000


class VectorDistanceTestCase(LinAlgTestCase):
    def test_code_check(self):
        self.code_check(["Vector"], import_exception)

    def test_distance_float(self):
        afloat = randomize_float()
        for r in range(num_tests):
            v1 = Vector((afloat(), afloat(), afloat()))
            v2 = Vector((afloat(), afloat(), afloat()))
            self.assertLess(v1.distance(v2), v1.norm() + v2.norm(), 3)

    def test_norm(self):
        self.assertEqual(Vector([0, 0, 0]).norm(), 0)
        self.assertEqual(Vector([1, 0, 0]).norm(), 1)
        for dim in range(3, 6):
            for r in range(num_tests):
                v1 = Vector.random(dim)
                v2 = Vector(sorted(v1.content))
                self.assertEqual(v1.norm(), v2.norm())

    def test_normalize_0(self):
        self.assertIs(None, Vector([0]).normalize())
        self.assertIs(None, Vector([0, 0]).normalize())
        self.assertIs(None, Vector([0, 0, 0]).normalize())
        self.assertIs(None, Vector([0, 0, 0, 0]).normalize())

    def test_normalize_1(self):
        for k in range(10):
            v = Vector([1 if k == i else 0 for i in range(10)])
            self.assertEqual(v, v.normalize())

    def test_normalize_2(self):
        for _ in range(num_tests):
            v = Vector.random(8)
            if v.norm() != 0:
                self.assertAlmostEqual(1.0, v.normalize().norm(), 3)

    def test_distance_triangle(self):
        afloat = randomize_float()
        for dim in range(2, 7):
            for r in range(num_tests):
                v1 = Vector.tabulate(dim, lambda _k: afloat())
                v2 = Vector.tabulate(dim, lambda _k: afloat())
                self.assertLess(v1.distance(v2), v1.norm() + v2.norm(), dim)

    def test_distance_2(self):
        rand = randomize_float(-0.001, 0.001)

        def epsilon(_k):
            return rand()

        for dim in range(2, 7):
            for r in range(num_tests):
                v1 = Vector.random(dim)
                v2 = v1 + Vector.tabulate(dim, epsilon)
                self.assertLess(v1.distance(v2), 0.01, dim)

    def test_distance_symmetric(self):
        afloat = randomize_float()
        for dim in range(2, 7):
            for r in range(num_tests):
                v1 = Vector.tabulate(dim, lambda _k: afloat())
                v2 = Vector.tabulate(dim, lambda _k: afloat())
                self.assertAlmostEqual(v1.distance(v2), v2.distance(v1), 4)

    def test_scale_norm(self):
        afloat = randomize_float()
        for dim in range(2, 7):
            for r in range(num_tests):
                v1 = Vector.random(dim)
                s = afloat()
                # |a| ||v|| = ||av||
                self.assertAlmostEqual(v1.norm() * abs(s), (v1 * s).norm(), 3)

    def test_distance_positive(self):
        afloat = randomize_float()
        for dim in range(2, 7):
            for r in range(num_tests):
                v1 = Vector.tabulate(dim, lambda _k: afloat())
                v2 = Vector.tabulate(dim, lambda _k: afloat())
                self.assertGreaterEqual(v1.distance(v2), 0)
                self.assertEqual(v1.distance(v1), 0)


if __name__ == '__main__':
    unittest.main()
