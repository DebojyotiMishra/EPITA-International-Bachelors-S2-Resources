import sys
import os
import unittest

# this path insertion is needed for VS Code, and does no harm for PyCharm
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.linalgtest import LinAlgTestCase

import_exception = None
try:
    from matrix.Vector import Vector
except Exception as e:
    print(e)
    import_exception = e

num_tests = 10000


class VectorTestCase(LinAlgTestCase):
    def test_code_check(self):
        self.code_check(["Vector"], import_exception)

    def test_randomizer(self):
        for dim in range(2, 7):
            vectors = set(Vector.random(dim).content for _k in range(num_tests))
            self.assertGreater(len(vectors), num_tests // 2)

    def test_print(self):
        self.assertEqual(f"{Vector([1, 2, 3])}", "Vector[3]((1, 2, 3))")
        self.assertEqual(f"{Vector([1, 2, 3, -1])}", "Vector[4]((1, 2, 3, -1))")
        self.assertEqual(f"{Vector([1, 2])}", "Vector[2]((1, 2))")

    def test_type(self):
        self.assertEqual(tuple, type(Vector([1, 2, 3]).content))

    def test_access(self):
        self.assertEqual(Vector([10, 20]).content, (10, 20))
        self.assertEqual(Vector([10, 20])[0], 10)
        self.assertEqual(Vector([10, 20])[1], 20)

    def test_equal(self):
        self.assertEqual(Vector([1, 2, 3]), Vector([1, 2, 3]))
        self.assertNotEqual(Vector([1, 2, 3]), Vector([2, 1, 3]))
        self.assertNotEqual(Vector([1, 2]), Vector([1, 2, 3]))
        self.assertNotEqual(Vector([1, 2, 3]), Vector([1, 2]))

        for dim in range(3, 6):
            v0 = Vector([1 for _ in range(dim)])
            for r in range(num_tests):
                v = Vector.random(dim)
                self.assertEqual(v, v)
                self.assertNotEqual(v, v + v0)

    def test_add(self):
        self.assertEqual(Vector([1, 2, 3]) + Vector([10, 20, 30]),
                         Vector([11, 22, 33]))

        for dim in range(3, 6):
            v0 = Vector([0 for _ in range(dim)])
            for r in range(num_tests):
                v1 = Vector.random(dim)
                v2 = Vector.random(dim)
                v3 = Vector.random(dim)
                self.assertEqual(v1 + v2, v2 + v1)
                self.assertEqual(v1 + v0, v1)
                self.assertEqual(v0 + v1, v1)
                self.assertEqual((v1 + v2) + v3,
                                 v1 + (v2 + v3))

    def test_scale(self):
        self.assertEqual(Vector([1, 2, 3]) * 4,
                         Vector([4, 8, 12]))
        for dim in range(3, 6):
            v0 = Vector.zero(dim)
            for r in range(num_tests):
                v1 = Vector.random(dim)
                self.assertEqual(v1 * 0, v0)
                self.assertEqual(v1 + v1 * -1, v0)

    def test_subtract(self):
        self.assertEqual(Vector([1, 2, 3]) - Vector([10, 20, 30]),
                         Vector([-9, -18, -27]))
        for dim in range(3, 6):
            v0 = Vector.zero(dim)
            for r in range(num_tests):
                v1 = Vector.random(dim)
                self.assertEqual(v1 + v1 * 2 - v1 - v1, v1)
                self.assertEqual(v1 - v1, v0)


if __name__ == '__main__':
    unittest.main()
