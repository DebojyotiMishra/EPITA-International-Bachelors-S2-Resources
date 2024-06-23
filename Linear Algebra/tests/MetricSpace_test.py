import sys
import os
import unittest
import random

# this path insertion is needed for VS Code, and does no harm for PyCharm
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.linalgtest import LinAlgTestCase
from common.utils import randomize_int, randomize_float, trace

import_exception = None
try:
    from structure.MetricSpace import is_metric_space, geodesic_distance, manhattan_distance, discrete_distance
    from matrix.Vector import Vector
except Exception as e:
    print(e)
    import_exception = e

num_tests = 1000


class MetricSpaceTestCase(LinAlgTestCase):
    def test_code_check(self):
        self.code_check(["MetricSpace", "Vector"], import_exception)

    def test_num_iterations(self):
        for k in range(1000, 1010):
            n = 1

            def d(x, y):
                nonlocal n
                n += 1
                if x == y:
                    return 0.0
                else:
                    return 1.0

            is_metric_space(d,
                            randomize_int(-100, 100),
                            k)
            self.assertGreaterEqual(n, k)

    def test_discrete_metric(self):
        def d(x, y):
            if x == y:
                return 0
            else:
                return 1

        self.assertTrue(is_metric_space(d,
                                        randomize_int(-100, 100),
                                        num_tests))
        self.assertTrue(is_metric_space(d,
                                        lambda: random.choice(['a', 'b', 'c', 'd']),
                                        num_tests))

    def test_floats(self):
        self.assertTrue(is_metric_space(lambda x, y: abs(x - y),
                                        randomize_float(-100.0, 100.0),
                                        num_tests))
        self.assertFalse(is_metric_space(lambda x, y: abs(2 * x - y),
                                         randomize_float(-100.0, 100.0),
                                         num_tests))
        self.assertFalse(is_metric_space(lambda x, y: abs(x),
                                         randomize_float(-100.0, 100.0),
                                         num_tests))

    def test_globe(self):
        from math import pi
        north_pole = (90, 0)
        south_pole = (-90, 0)
        paris = (48 + 51 / 60,
                 2 + 21 / 60)  # 48°51′N 2°21′E
        berlin = (52 + 31 / 60,
                  13 + 23 / 60)  # 52°31′N 13°23′E
        denver = (39 + 44 / 60,
                  -(104 + 59 / 60))  # 39°44′N 104°59′W
        sydney = (-(33 + 52 / 60),
                  151 + 13 / 60)  # 33°52′S 151°13′E

        # test with 10 km
        def within(a, b):
            return round(abs(a - b)) < 10

        self.assertTrue(geodesic_distance(north_pole, north_pole) == 0)
        self.assertTrue(within(geodesic_distance(north_pole, south_pole), 6371 * pi))
        # quarter way around the equator
        self.assertTrue(within(geodesic_distance((0, 0), (0, 90)), 6371 * pi / 2))
        # equator to north pole
        self.assertTrue(within(geodesic_distance((0, 0), north_pole), 6371 * pi / 2))
        # halfway around the equator
        self.assertTrue(within(geodesic_distance((0, 0), (0, 180)), 6371 * pi))
        self.assertAlmostEqual(geodesic_distance(paris, berlin),
                               geodesic_distance(berlin, paris))
        self.assertTrue(within(geodesic_distance(paris, berlin), 878))
        self.assertTrue(within(geodesic_distance(paris, denver), 7860))
        self.assertTrue(within(geodesic_distance(denver, sydney), 13408))
        self.assertTrue(within(geodesic_distance(sydney, berlin), 16094))
        self.assertTrue(within(geodesic_distance(sydney, paris), 16960))

    def test_globe_metric_space(self):
        self.assertTrue(is_metric_space(geodesic_distance,
                                        lambda: (random.uniform(-80.0, 80.0),
                                                 random.uniform(-170, 170)),
                                        num_tests))

    def test_discrete_metric_space(self):
        getint = randomize_int(-100, 100)
        self.assertTrue(is_metric_space(discrete_distance,
                                        lambda: (getint(), getint()),
                                        num_tests))

    def test_discrete(self):
        self.assertEqual(discrete_distance(3, 12), 1)
        self.assertEqual(discrete_distance((3, 3), (12, 11)), 1)
        self.assertEqual(discrete_distance(3, 3), 0)
        self.assertEqual(discrete_distance((3, 4), (3, 4)), 0)
        for x in range(100):
            for y in range(100):
                if x == y:
                    self.assertEqual(discrete_distance((x, x), (y, y)), 0)
                else:
                    self.assertEqual(discrete_distance((x, x), (y, y)), 1)

    def test_manhattan_metric(self):
        getint = randomize_int(-100, 100)
        for dim in range(2, 5):
            self.assertTrue(is_metric_space(manhattan_distance,
                                            lambda: Vector(tuple(getint() for _k in range(dim))),
                                            num_tests))


if __name__ == '__main__':
    unittest.main()
