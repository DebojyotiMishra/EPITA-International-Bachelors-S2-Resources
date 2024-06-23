import sys
import os
import unittest

# this path insertion is needed for VS Code, and does no harm for PyCharm
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.linalgtest import LinAlgTestCase
from common.utils import randomize_int
from matrix.randmat import random_invertible

import_exception = None
try:
    from matrix.SqMatrix import SqMatrix
    from matrix.Vector import Vector
    from structure.VectorSpace import find_coordinates, change_coordinates
except Exception as e:
    print(e)
    import_exception = e

num_tests = 1000


class CoordinatesTestCase(LinAlgTestCase):
    def test_code_check(self):
        self.code_check(["VectorSpace", "Vector", "SqMatrix", "Matrix"], import_exception)

    # this is a test of the function find_coordinates
    # given a basis and a vector, find the coordinates of the vector w.r.t the basis
    def test_find_coords(self):
        rand_int = randomize_int(-10, 10)
        for dim in range(2, 7):
            for _rep in range(num_tests):
                m = random_invertible(dim)
                while m.gauss_jordan_inverse() == (None, 0):
                    m = random_invertible(dim)
                basis = [Vector(m[k]) for k in range(dim)]
                v = Vector.random(dim, randomizer=rand_int)
                c = find_coordinates(v, basis)
                self.assertIsNotNone(c)
                self.assertAlmostEqual(v.distance(m.transpose() * c), 0, 3)

    # given a vector in the coordinate system of basis 1, find its coordinates
    #  in basis 2.
    def test_change_coordinates(self):
        # this is a test of the function change_coordinates
        # this test supposes that find_coordinates already works and has been tested
        rand_int = randomize_int(-10, 10)

        for dim in range(2, 6):
            for _rep in range(num_tests):
                v = Vector.random(dim, randomizer=rand_int)

                m1 = random_invertible(dim)
                while m1.gauss_jordan_inverse() == (None, 0):
                    print(f"searching again {dim=}")
                    m1 = random_invertible(dim)
                basis1 = [Vector(m1[k]) for k in range(dim)]
                c1 = find_coordinates(v, basis1)
                self.assertIsNotNone(c1, f"unable to find coords of {v=} with {basis1=}")

                m2 = random_invertible(dim)
                while m2.gauss_jordan_inverse() == (None, 0):
                    m2 = random_invertible(dim)
                basis2 = [Vector(m2[k]) for k in range(dim)]

                c2 = change_coordinates(c1, basis1, basis2)
                self.assertTrue(c2, f"unable to change coords of {c1=} with {basis1=} and {basis2=}")
                inv2, det2 = m2.transpose().gauss_jordan_inverse()
                if det2 == 0:
                    self.assertIsNone(c2)
                else:
                    self.assertAlmostEqual(c2.distance(inv2 * v), 0, 3,
                                           f"dimension={dim}")


if __name__ == '__main__':
    unittest.main()
