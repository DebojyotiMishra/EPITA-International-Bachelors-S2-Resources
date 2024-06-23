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


class VectorAngleTestCase(LinAlgTestCase):
    def test_code_check(self):
        self.code_check(["Vector"], import_exception)

    def test_Vector_3_angle(self):
        import random
        import math
        n1 = random.randint(1, 5) * random.choice([-1, 1])
        n2 = random.randint(1, 5) * random.choice([-1, 1])
        n3 = random.randint(1, 5) * random.choice([-1, 1])
        for r in range(num_tests):
            theta1 = math.degrees(Vector([n1, 0, 0]).angle(Vector([0, n2, 0])))
            theta2 = math.degrees(Vector([0, n2, 0]).angle(Vector([0, 0, n3])))
            theta3 = math.degrees(Vector([0, 0, n3]).angle(Vector([n1, 0, 0])))
            self.assertAlmostEqual(theta1, 90)
            self.assertAlmostEqual(theta2, 90)
            self.assertAlmostEqual(theta3, 90)

    def test_Vector4_angle(self):
        import random
        import math
        n1 = random.randint(1, 6) * random.choice([-1, 1])
        n2 = random.randint(1, 6) * random.choice([-1, 1])
        n3 = random.randint(1, 6) * random.choice([-1, 1])
        n4 = random.randint(1, 6) * random.choice([-1, 1])
        for r in range(num_tests):
            theta1 = math.degrees(Vector([n1, 0, 0, 0]).angle(Vector([0, n2, 0, 0])))
            theta2 = math.degrees(Vector([0, n2, 0, 0]).angle(Vector([0, 0, n3, 0])))
            theta3 = math.degrees(Vector([0, 0, n3, 0]).angle(Vector([0, 0, 0, n4])))
            theta4 = math.degrees(Vector([0, 0, 0, n4]).angle(Vector([n4, 0, 0, 0])))
            self.assertAlmostEqual(theta1, 90)
            self.assertAlmostEqual(theta2, 90)
            self.assertAlmostEqual(theta3, 90)
            self.assertAlmostEqual(theta4, 90)

    def test_Vector_angle(self):
        import random
        import math

        for dim in range(3, 6):
            n = [random.randint(1, 5) * random.choice([-1, 1])
                 for _ in range(dim)]
            for r in range(num_tests):
                p1 = random.randint(0, dim - 1)
                p2 = random.randint(0, dim - 1)
                v1 = Vector([n[p1] if j == p1 else 0
                             for j in range(dim)])
                v2 = Vector([n[p2] if j == p2 else 0
                             for j in range(dim)])
                theta = math.degrees(v1.angle(v2))
                if p1 == p2:
                    self.assertAlmostEqual(theta, 0)
                else:
                    self.assertAlmostEqual(theta, 90)


if __name__ == '__main__':
    unittest.main()
