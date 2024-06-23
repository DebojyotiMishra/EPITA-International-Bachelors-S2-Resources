import sys
import os
import unittest
import random

# this path insertion is needed for VS Code, and does no harm for PyCharm
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.linalgtest import LinAlgTestCase
from common.utils import trace, randomize_float

import_exception = None
try:
    from structure.MetricSpace import is_metric_space
    from structure.VectorSpace import is_vector_space
    from matrix.Vector import Vector
except Exception as e:
    print(e)
    import_exception = e

num_tests = 1000
# TODO change of constants such as 0.001 to epsilon
epsilon = 0.00000001


def field_member(s):
    return isinstance(s, float) or isinstance(s, int)


def vector_member(k):
    return lambda v: isinstance(v, Vector) and v.dim == k


def prime(k):
    """good enough prime test for small integers"""
    return not any(k % n == 0
                   for n in range(2, k - 1))


class VectorSpaceTestCase(LinAlgTestCase):
    def test_code_check(self):
        self.code_check(["MetricSpace", "VectorSpace", "Vector"], import_exception)

    def test_num_iterations(self):
        dim = 4
        for k in range(100, 110):
            n1 = 1
            n2 = 1
            n3 = 1
            n4 = 1
            n5 = 1
            n6 = 1
            n7 = 1

            def vv_add(u, v):
                nonlocal n3
                n3 += 1
                return u + v

            def ss_mult(a, b):
                nonlocal n1
                n1 += 1
                return a * b

            def ss_add(a, b):
                nonlocal n2
                n2 += 1
                return a + b

            def sv_mult(s, v):
                nonlocal n4
                n4 += 1
                return v.scale(s)

            def v_inverse(v):
                nonlocal n5
                n5 += 1
                return v.scale(-1)

            def s_add_inverse(s):
                nonlocal n6
                n6 += 1
                return -s

            def s_mult_inverse(s):
                nonlocal n7
                n7 += 1
                return 1.0 / s

            self.assertTrue(is_vector_space(v_member=vector_member(dim),
                                            s_member=field_member,
                                            vv_add=vv_add,
                                            ss_add=ss_add,
                                            ss_mult=ss_mult,
                                            sv_mult=sv_mult,
                                            v_identity=Vector.zero(dim),
                                            s_add_ident=0.0,
                                            s_mult_ident=1.0,
                                            v_inverse=v_inverse,
                                            s_add_inverse=s_add_inverse,
                                            s_mult_inverse=s_mult_inverse,
                                            v_equivalent=lambda u, v: u.distance(v) < epsilon,
                                            s_equivalent=lambda a, b: abs(a - b) < epsilon,
                                            v_gen=lambda: Vector.random(dim),
                                            s_gen=lambda: random.uniform(-1.0, 1.0),
                                            iterations=num_tests
                                            ))
            self.assertGreaterEqual(n1, k)
            self.assertGreaterEqual(n2, k)
            self.assertGreaterEqual(n3, k)
            self.assertGreaterEqual(n4, k)
            self.assertGreaterEqual(n5, k)
            self.assertGreaterEqual(n6, k)
            self.assertGreaterEqual(n7, k)

    def test_vector_space_1(self):
        for k in range(2, 10):
            # test whether the set of k-vectors is a vector space
            #   using float as scalar

            # 1
            self.assertTrue(is_vector_space(v_member=vector_member(k),
                                            s_member=field_member,
                                            vv_add=lambda u, v: u + v,
                                            ss_add=lambda a, b: a + b,
                                            ss_mult=lambda a, b: a * b,
                                            sv_mult=lambda s, v: v.scale(s),
                                            v_identity=Vector.zero(k),
                                            s_add_ident=0.0,
                                            s_mult_ident=1.0,
                                            v_inverse=(lambda v: v.scale(-1)),
                                            s_add_inverse=(lambda s: -s),
                                            s_mult_inverse=lambda s: 1.0 / s,
                                            v_equivalent=lambda u, v: u.distance(v) < epsilon,
                                            s_equivalent=lambda a, b: abs(a - b) < epsilon,
                                            v_gen=lambda: Vector.random(k),
                                            s_gen=lambda: random.uniform(-1.0, 1.0),
                                            iterations=num_tests
                                            ))

    def test_vector_space_2(self):
        for k in range(2, 10):
            # 2
            self.assertFalse(is_vector_space(v_member=vector_member(k),
                                             s_member=field_member,
                                             # if adding divides by 2, it is not a vector space
                                             vv_add=lambda u, v: (u + v).scale(0.5),
                                             ss_add=lambda a, b: a + b,
                                             ss_mult=lambda a, b: a * b,
                                             sv_mult=lambda s, v: v.scale(s),
                                             v_identity=Vector.zero(k),
                                             s_add_ident=0.0,
                                             s_mult_ident=1.0,
                                             v_inverse=(lambda v: v.scale(-1)),
                                             s_add_inverse=(lambda s: -s),
                                             s_mult_inverse=lambda s: 1.0 / s,
                                             v_equivalent=lambda u, v: u.distance(v) < epsilon,
                                             s_equivalent=lambda a, b: abs(a - b) < epsilon,
                                             v_gen=lambda: Vector.random(k),
                                             s_gen=lambda: random.uniform(-1.0, 1.0),
                                             iterations=num_tests
                                             ))

    def test_vector_space_3(self):
        for k in range(2, 10):
            # 3
            self.assertFalse(is_vector_space(v_member=vector_member(k),
                                             s_member=field_member,
                                             vv_add=lambda u, v: u + v,
                                             # not vector space
                                             ss_add=lambda a, b: a + b + 1.0,
                                             ss_mult=lambda a, b: a * b,
                                             sv_mult=lambda s, v: v.scale(s),
                                             v_identity=Vector.zero(k),
                                             s_add_ident=0.0,
                                             s_mult_ident=1.0,
                                             v_inverse=(lambda v: v.scale(-1)),
                                             s_add_inverse=(lambda s: -s),
                                             s_mult_inverse=lambda s: 1.0 / s,
                                             v_equivalent=lambda u, v: u.distance(v) < epsilon,
                                             s_equivalent=lambda a, b: abs(a - b) < epsilon,
                                             v_gen=lambda: Vector.random(k),
                                             s_gen=lambda: random.uniform(-1.0, 1.0),
                                             iterations=num_tests
                                             ))

    def test_vector_space_4(self):
        for k in range(2, 10):
            # 4
            self.assertFalse(is_vector_space(v_member=vector_member(k),
                                             s_member=field_member,
                                             vv_add=lambda u, v: u + v,
                                             ss_add=lambda a, b: a + b,
                                             # not vector space
                                             ss_mult=lambda a, b: a * b * 0.5,
                                             sv_mult=lambda s, v: v.scale(s),
                                             v_identity=Vector.zero(k),
                                             s_add_ident=0.0,
                                             s_mult_ident=1.0,
                                             v_inverse=(lambda v: v.scale(-1)),
                                             s_add_inverse=(lambda s: -s),
                                             s_mult_inverse=lambda s: 1.0 / s,
                                             v_equivalent=lambda u, v: u.distance(v) < epsilon,
                                             s_equivalent=lambda a, b: abs(a - b) < epsilon,
                                             v_gen=lambda: Vector.random(k),
                                             s_gen=lambda: random.uniform(-1.0, 1.0),
                                             iterations=num_tests
                                             ))

    def test_vector_space_5(self):
        for k in range(2, 10):
            # 5
            self.assertFalse(is_vector_space(v_member=vector_member(k),
                                             s_member=field_member,
                                             vv_add=lambda u, v: u + v,
                                             ss_add=lambda a, b: a + b,
                                             ss_mult=lambda a, b: a * b,
                                             # if scalar multiplication also multiplies by 2
                                             # then it is no longer a vector space
                                             sv_mult=lambda s, v: v.scale(s * 2),
                                             v_identity=Vector.zero(k),
                                             s_add_ident=0.0,
                                             s_mult_ident=1.0,
                                             v_inverse=(lambda v: v.scale(-1)),
                                             s_add_inverse=(lambda s: -s),
                                             s_mult_inverse=lambda s: 1.0 / s,
                                             v_equivalent=lambda u, v: u.distance(v) < epsilon,
                                             s_equivalent=lambda a, b: abs(a - b) < epsilon,
                                             v_gen=lambda: Vector.random(k),
                                             s_gen=lambda: random.uniform(-1.0, 1.0),
                                             iterations=num_tests
                                             ))

    def test_vector_space_6(self):
        for k in range(2, 10):
            # 6
            self.assertFalse(is_vector_space(v_member=vector_member(k),
                                             s_member=field_member,
                                             vv_add=lambda u, v: u + v,
                                             ss_add=lambda a, b: a + b,
                                             ss_mult=lambda a, b: a * b,
                                             sv_mult=lambda s, v: v.scale(s),
                                             v_identity=Vector.zero(k),
                                             s_add_ident=0.0,
                                             s_mult_ident=1.0,
                                             v_inverse=(lambda v: v.scale(-1)),
                                             # not the correct inverse
                                             s_add_inverse=(lambda s: s),
                                             s_mult_inverse=lambda s: 1.0 / s,
                                             v_equivalent=lambda u, v: u.distance(v) < epsilon,
                                             s_equivalent=lambda a, b: abs(a - b) < epsilon,
                                             v_gen=lambda: Vector.random(k),
                                             s_gen=lambda: random.uniform(-1.0, 1.0),
                                             iterations=num_tests
                                             ))

    def test_vector_space_7(self):
        for k in range(2, 10):
            # 7
            self.assertFalse(is_vector_space(v_member=vector_member(k),
                                             s_member=field_member,
                                             vv_add=lambda u, v: u + v,
                                             ss_add=lambda a, b: a + b,
                                             ss_mult=lambda a, b: a * b,
                                             sv_mult=lambda s, v: v.scale(s),
                                             v_identity=Vector.zero(k),
                                             s_add_ident=0.0,
                                             s_mult_ident=1.0,
                                             # wrong inverse
                                             v_inverse=(lambda v: v.scale(-1 / 2)),
                                             s_add_inverse=(lambda s: -s),
                                             s_mult_inverse=lambda s: 1 / s,
                                             v_equivalent=lambda u, v: u.distance(v) < epsilon,
                                             s_equivalent=lambda a, b: abs(a - b) < epsilon,
                                             v_gen=lambda: Vector.random(k),
                                             s_gen=lambda: random.uniform(-1.0, 1.0),
                                             iterations=num_tests
                                             ))

    def test_vector_space_8(self):
        for k in range(2, 10):
            # 8
            self.assertFalse(is_vector_space(v_member=vector_member(k),
                                             s_member=field_member,
                                             vv_add=lambda u, v: u + v,
                                             ss_add=lambda a, b: a + b,
                                             ss_mult=lambda a, b: a * b,
                                             sv_mult=lambda s, v: v.scale(s),
                                             v_identity=Vector.zero(k),
                                             s_add_ident=0.0,
                                             s_mult_ident=1.0,
                                             v_inverse=(lambda v: v.scale(-1)),
                                             s_add_inverse=(lambda s: -s),
                                             # not vector space, wrong inverse
                                             s_mult_inverse=lambda s: s,
                                             v_equivalent=lambda u, v: u.distance(v) < epsilon,
                                             s_equivalent=lambda a, b: abs(a - b) < epsilon,
                                             v_gen=lambda: Vector.random(k),
                                             s_gen=lambda: random.uniform(-1.0, 1.0),
                                             iterations=num_tests
                                             ))

    def test_vector_modulo(self):
        """We generate a vector space based on modulo arithmetic.
        The vector had dimension dim, and is composed of elements
        of the set of integers [0, 1, ... k-1].
        If k is prime, then this is a field.
        The vector space has this as its supposed field,
        and the vectors have elements of this set as component.
        This is a vector space if k is prime,
        and it is not a vector space if k is composite.
        """
        for k in range(2, 17):
            scalars = [x for x in range(k)]
            for dim in range(2, 6):
                def ss_add(a, b):
                    return (a + b) % k

                def ss_mult(a, b):
                    return (a * b) % k

                def vv_add(u, v):
                    return Vector([ss_add(u[i], v[i]) for i in range(dim)])

                def sv_mult(s, v):
                    return Vector([ss_mult(s, v[i]) for i in range(dim)])

                def s_add_inverse(s):
                    return 0 if s == 0 else k - s

                def v_inverse(v):
                    return Vector([s_add_inverse(v[i]) for i in range(dim)])

                def s_mult_inverse(s):
                    return next((x for x in scalars if ss_mult(s, x) == 1), None)

                self.assertEqual(prime(k),
                                 is_vector_space(v_member=lambda v: isinstance(v, Vector) and v.dim == dim,
                                                 s_member=lambda x: x in scalars,
                                                 vv_add=vv_add,
                                                 ss_add=ss_add,
                                                 ss_mult=ss_mult,
                                                 sv_mult=sv_mult,
                                                 v_identity=Vector.zero(dim),
                                                 s_add_ident=0,
                                                 s_mult_ident=1,
                                                 v_inverse=v_inverse,
                                                 s_add_inverse=s_add_inverse,
                                                 s_mult_inverse=s_mult_inverse,
                                                 v_gen=lambda: Vector([random.choice(scalars) for _k in range(dim)]),
                                                 s_gen=lambda: random.choice(scalars),
                                                 iterations=num_tests // 2
                                                 ),
                                 f"dim={dim} k={k} expecting {prime(k)}")

    def test_vector_space_metric(self):
        choose_float = randomize_float(-100.0, 100.0)
        for dim in range(2, 7):
            def d(u, v) -> float:
                return u.distance(v)

            def gen() -> Vector:
                return Vector.random(dim, randomizer=choose_float)

            self.assertTrue(is_metric_space(d, gen, iterations=num_tests))
            self.assertFalse(is_metric_space(lambda _u, _v: 1.0,
                                             gen, iterations=num_tests))
            self.assertFalse(is_metric_space(lambda u, v: u.distance(v.scale(-1)),
                                             gen,
                                             iterations=num_tests))


if __name__ == '__main__':
    unittest.main()
