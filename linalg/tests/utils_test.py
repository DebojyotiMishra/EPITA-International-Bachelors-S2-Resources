import sys
import os
import unittest
import math
from typing import List, Tuple

# this path insertion is needed for VS Code, and does no harm for PyCharm
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.utils import generate_lazy_val, fixed_point, uniquify, flat_map, randomize_int, interpolate_curve
from common.utils import search_replace_splice, search_replace, remove_element
from common.utils import find_first, group_by, group_map, make_counter, interpolate
from common.utils import argmax, argmin
from common.utils import trace_graph

# default value of num_random_tests is 1000, but you can temporarily edit this file
#   and set it to a smaller number for a quicker run of the tests.
num_random_tests = 1000


class UtilsCase(unittest.TestCase):

    def test_generate_lazy_val(self):
        a = 0

        def f():
            nonlocal a
            a += 1
            return a

        x = generate_lazy_val(f)
        self.assertEqual(a, 0)
        self.assertEqual(x(), 1)
        self.assertEqual(a, 1)
        self.assertEqual(x(), 1)
        self.assertEqual(a, 1)

    def test_fixed_point(self):
        self.assertEqual(0, fixed_point(10,
                                        lambda a: (a // 2),
                                        (lambda a, b: a == b),
                                        ))

    def test_uniquify(self):
        self.assertEqual(uniquify([1, 1, 2, 2, 3, 1, 3]),
                         [2, 1, 3])
        r = randomize_int(0, 10)
        for i in range(20):
            data = [r() for _i in range(10)]
            self.assertEqual(sorted(uniquify(data)), uniquify(sorted(data)))

    def test_flat_map(self):
        self.assertEqual(flat_map(lambda a: [a, a], [1, 2, 3]),
                         [1, 1, 2, 2, 3, 3])

    def test_search_replace_splice(self):
        self.assertEqual(search_replace_splice([1, 2, 3, 2, 1], 2, [0, 0]),
                         [1, 0, 0, 3, 0, 0, 1])
        self.assertEqual(search_replace_splice([1, 2, 3, 2, 1], 2, []),
                         [1, 3, 1])

    def test_search_replace(self):
        self.assertEqual(search_replace([1, 2, 3, 2, 1], 2, 0),
                         [1, 0, 3, 0, 1])

    def test_remove_element(self):
        self.assertEqual(remove_element([1, 2, 3, 2, 1], 2),
                         [1, 3, 1])

    def test_find_first(self):
        self.assertEqual(find_first(lambda x: x % 2 == 0,
                                    [1, 3, 2, 4, 5]),
                         2)
        self.assertIs(find_first(lambda x: x > 10 == 0,
                                 [1, 3, 2, 4, 5]),
                      None)
        self.assertEqual(find_first(lambda x: x > 10 == 0,
                                    [1, 3, 2, 4, 5],
                                    "not-found"),
                         "not-found")

    def test_group_by(self):
        g = group_by(lambda x: x % 3, [1, 2, 3, 1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(sorted(g[1]), [1, 1, 4, 7])
        self.assertEqual(sorted(g[2]), [2, 2, 5])
        self.assertEqual(sorted(g[0]), [3, 3, 6])

    def test_group_map(self):
        g = group_map(lambda x: x % 3,
                      [1, 2, 3, 1, 2, 3, 4, 5, 6, 7],
                      lambda x: [x])
        self.assertEqual(sorted(g[1]), [[1], [1], [4], [7]])
        self.assertEqual(sorted(g[2]), [[2], [2], [5]])
        self.assertEqual(sorted(g[0]), [[3], [3], [6]])

    def test_make_counter(self):
        c = make_counter(10, -2)
        self.assertEqual(c(), 10)
        self.assertEqual(c(), 8)
        self.assertEqual(c(), 6)

        c2 = make_counter()
        self.assertEqual(c2(), 0)
        self.assertEqual(c2(), 1)
        self.assertEqual(c2(), 2)

    def test_interpolate(self):
        for f in [lambda x: x * x,
                  lambda x: 0]:
            for epsilon in [10.0, 5.0, 2.0, 1.0, 0.5, 0.2, 0.1]:
                min_dx = 0.001
                max_dx = 1.0
                xys = interpolate(0.0, 10.0, min_dx, max_dx, epsilon, f)
                for i in range(len(xys) - 1):
                    (x1, y1), (x2, y2), *_ = xys
                    self.assertTrue(abs(x1 - x2) > min_dx)
                    self.assertTrue(abs(x1 - x2) < max_dx)
                # plot_xys(xys)

    def test_circle(self):
        xys = interpolate_curve(-math.pi, math.pi,
                                min_dt=0.1,
                                max_dt=0.2,
                                max_dx=0.1,
                                f=(lambda t: (t * math.sin(t * 2), t * math.cos(t * 3))))
        self.assertTrue(len(xys) > 60)

    def test_trace_graph(self):
        def neighbors(v: str) -> List[Tuple[float, str]]:
            if v == "a":
                return [(1.0, "a"), (2.5, "b")]
            if v == "b":
                return [(3.5, "c"), (3.0, "b")]
            if v == "c":
                return [(2.25, "b"), (1.5, "a")]

        vs, edges = trace_graph("a", neighbors)
        gr = [(vs[i], w, vs[j]) for i in range(len(edges))
              for w, j in edges[i]]
        self.assertEqual(sorted(gr),
                         [('a', 1.0, 'a'),
                          ('a', 2.5, 'b'),
                          ('b', 3.0, 'b'),
                          ('b', 3.5, 'c'),
                          ('c', 1.5, 'a'),
                          ('c', 2.25, 'b')])

    def test_argmax(self):
        self.assertEqual(-10, argmax(abs, [8, 9, -10]))
        self.assertEqual(10, argmax(abs, [8, -9, 10]))
        self.assertIsNone(argmax(abs, []))

    def test_argmin(self):
        self.assertEqual(-8, argmin(abs, [-8, 9, -10]))
        self.assertEqual(8, argmin(abs, [8, 9, 10]))
        self.assertIsNone(argmin(abs, []))


if __name__ == '__main__':
    unittest.main()
