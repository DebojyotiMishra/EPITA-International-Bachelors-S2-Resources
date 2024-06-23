import sys
import os
import unittest
import random

# this path insertion is needed for VS Code, and does no harm for PyCharm
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from matrix.randmat import random_invertible
from tests.linalgtest import LinAlgTestCase

import_exception = None
try:
    from matrix.SqMatrix import SqMatrix
    from matrix.Matrix import Matrix
    from matrix.Vector import Vector
except Exception as e:
    print(e)
    import_exception = e

repetitions = 100
epsilon = 0.000001


class EigenvaluesTestCase(LinAlgTestCase):
    def test_code_check(self):
        self.code_check(["SqMatrix", "Matrix", "Vector"], import_exception)

    def test_eigenvalues_0(self):
        self.assertListAlmostEqual(
            [1.0, 1.0], SqMatrix([[1, 0], [0, 1]]).eigenvalues(0.001), 3
        )

    def test_eigenvalues_1(self):
        p = SqMatrix([[1, 2, 1], [2, 0, 1], [1, 1, 2]])
        p_inv, det = p.gauss_jordan_inverse()
        diag = SqMatrix.diagonal([-1, 1, 2])

        es = (p * diag * p_inv).eigenvalues(0.0001)
        self.assertListAlmostEqual([-1, 1, 2], es, 3)

    def test_eigenvalues_2(self):
        for dim in range(2, 6):
            for _ in range(repetitions):
                m = random_invertible(dim)
                mm = m * m.transpose()
                mm_inv, det = mm.gauss_jordan_inverse()
                if det < 0.001:
                    continue
                es = {}
                while len(es) != dim:
                    # create a list of dim-many integers between -10 and 9
                    # without repeats.
                    es = sorted(list({random.randint(-10, 10) for _ in range(dim)}))
                d = SqMatrix.diagonal(es)
                mat = mm * d * mm_inv
                self.assertListAlmostEqual(es, mat.eigenvalues(0.000001), 2)

    def test_eigenvectors_0a(self):
        epsilon = 0.00001
        A = SqMatrix(((4, 0), (0, 2)))
        spectrum = [2, 4]
        vectors = A.eigenvectors(spectrum, epsilon)
        self.assertAlmostEqual(0, vectors[0].angle(Vector((0, 1))))
        self.assertAlmostEqual(0, vectors[1].angle(Vector((1, 0))))

    def test_eigenvectors_0b(self):
        epsilon = 0.00001
        A = SqMatrix(((4, 0, 0), (0, 1, 0), (0, 0, 2)))
        spectrum = [1, 2, 4]
        vectors = A.eigenvectors(spectrum, epsilon)
        self.assertAlmostEqual(0, vectors[0].angle(Vector((0, 1, 0))))
        self.assertAlmostEqual(0, vectors[1].angle(Vector((0, 0, 1))))
        self.assertAlmostEqual(0, vectors[2].angle(Vector((1, 0, 0))))

    def test_eigenvectors_0(self):
        m = SqMatrix([[1, 0, 0], [0, 2, 0], [0, 0, 3]])

        pairs = m.eigen(0.00001)
        for e, v in pairs:
            uv = v.normalize()
            # the norm of p*v is the absolute value of the eigenvalue
            self.assertAlmostEqual(abs(e), (m * uv).norm(), 2)
            # the eigenvector is parallel to p*v
            self.assertAlmostEqual(1.0, abs(uv.inner_product((m * uv).normalize())), 2)
            self.assertListAlmostEqual(
                uv.scale(e).content,
                (m * uv).content,
                2,
                f"expecting {uv.scale(e)}; got {m * uv}",
            )

    def test_eigenvectors_1(self):
        # this example comes from
        # https://en.wikipedia.org/wiki/Eigenvalue_algorithm#3×3_matrices
        A = SqMatrix([[3, 2, 6], [2, 2, 5], [-2, -1, -4]])
        spectrum = A.eigenvalues(0.00001)
        self.assertListAlmostEqual(spectrum, [-1, 1, 1], 3)
        vectors = A.eigenvectors(spectrum)
        self.assertIsNone(
            vectors, f"with repeated eigenvalues, eigenvectors should return None"
        )

    def test_eigenvectors_2(self):
        p = SqMatrix([[1, 2, 1], [2, 0, 1], [1, 1, 2]])
        p_inv, det = p.gauss_jordan_inverse()
        diag = SqMatrix.diagonal([-1, 1, 2])
        m = p * diag * p_inv
        pairs = m.eigen(0.00001)
        for e, v in pairs:
            uv = v.normalize()  # unit vec in direction of v
            # the norm of p*(v.normalize()) is the absolute value of the eigenvalue
            self.assertAlmostEqual(abs(e), (m * uv).norm(), 2)
            # the eigenvector is parallel to p*v

            self.assertAlmostEqual(1.0, abs(uv.inner_product((m * uv).normalize())), 2)
            self.assertListAlmostEqual(
                uv.scale(e).content,
                (m * uv).content,
                2,
                f"expecting {uv.scale(e)}; got {m * uv}",
            )

    def test_eigenvectors_3(self):
        # from https://www.youtube.com/watch?v=7iI2BiDehhk&t=1737s
        a = SqMatrix(((4, -9, 6, 12), (0, -1, 4, 6), (2, -11, 8, 16), (-1, 3, 0, -1)))
        e0 = 1
        v0 = Vector((1, 1, -1, 1))
        e1 = 2
        v1 = Vector((3, 2, 0, 1))
        e2 = 3
        v2 = Vector((3, 1, 1, 0))
        e3 = 4
        v3 = Vector((1, 2, 1, 1))

        # we should have exact equality here because of the rational roots test
        self.assertEqual([e0, e1, e2, e3], a.eigenvalues(0.00001))
        vectors = a.eigenvectors([e0, e1, e2, e3], 0.0001)
        self.assertAlmostEqual(0, v0.angle(vectors[0]), 3)
        self.assertAlmostEqual(0, v1.angle(vectors[1]), 3)
        self.assertAlmostEqual(0, v2.angle(vectors[2]), 3)
        self.assertAlmostEqual(0, v3.angle(vectors[3]), 3)

    def test_eigenvectors_4(self):
        epsilon = 0.00000001
        for dim in range(2, 5):
            for _ in range(repetitions):
                m = random_invertible(dim)
                mm = m * m.transpose()
                mm_inv, det = mm.gauss_jordan_inverse()
                if det < 0.01:
                    continue
                int_es = {}
                while len(int_es) != dim:
                    # create a list of dim-many integers between -10 and 9
                    # without repeats.
                    int_es = sorted(list({random.randint(-10, 10) for _ in range(dim)}))
                d = SqMatrix.diagonal(int_es)
                mat = mm * d * mm_inv
                es = mat.eigenvalues(epsilon)
                if len(set(es)) != dim:
                    continue
                pairs = mat.eigen(epsilon)
                if pairs is None:
                    continue
                if any(
                    v is None or v.norm() < 0.01 or abs(e) < 2 * epsilon
                    for e, v in pairs
                ):
                    continue
                for e, v in pairs:
                    e = round(e)  # we know e is an integer by construction
                    self.assertTrue(
                        e in int_es, f"expecting eigenvalues: {es}, got {e}"
                    )
                    self.assertAlmostEqual((mat * v - v * e).norm(), 0, 2)

    def test_eigvenvectors_5(self):
        A = SqMatrix(((2, 3), (4, 6)))
        # eigenvalues are 0 and 8
        self.assertIsNone(A.eigenvectors([0.00001, 8.0], 0.001))


if __name__ == "__main__":
    unittest.main()
