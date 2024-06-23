from typing import List, Callable, TypeVar, Tuple, Optional, Union
from functools import reduce
from math import isinf, isnan

from common.utils import randomize_int, fast_power
from matrix.Vector import Vector
from matrix.Matrix import Matrix

T = TypeVar("T")


class SqMatrix(Matrix):
    def __init__(self, content):
        self.dim = len(content)
        self.content = tuple(tuple(row) for row in content)
        assert all(len(row) == self.dim for row in content)
        super().__init__(content)

    def __repr__(self):
        lines = ",\n        ".join(f"{row}" for row in self.content)
        return f"SqMatrix(({lines}))"

    @staticmethod
    def random(dim: int, randomizer: Callable[[], int] = randomize_int()) -> "SqMatrix":
        return Matrix.random(dim, dim, randomizer)

    @staticmethod
    def identity(dim: int) -> "SqMatrix":
        return SqMatrix.tabulate(dim, lambda r, c: 1 if r == c else 0)

    @staticmethod
    def zero(dim: int) -> "SqMatrix":
        return Matrix.zero(dim, dim)

    @staticmethod
    def tabulate(dim: int, f: Callable[[int, int], float]) -> "SqMatrix":
        return Matrix.tabulate(dim, dim, f)

    @staticmethod
    def diagonal(entries) -> "SqMatrix":
        return SqMatrix.tabulate(len(entries), lambda r, c: entries[r] if r == c else 0)

    def gaussian_elimination_back_substitution(self, v: Vector) -> Optional[Vector]:
        assert isinstance(v, Vector)
        assert v.dim == self.dim

        ech = self.adjoin_col(v).make_row_echelon()
        if ech is None:
            return None
        assert ech.rows == self.rows
        assert ech.cols == self.cols + 1
        return ech.back_substitution()

    def gauss_jordan_elimination(self, v: Vector) -> Optional[Vector]:
        assert isinstance(v, Vector)
        assert v.dim == self.dim

        diag, _ = self.adjoin_col(v).make_unit_diagonal()
        if diag is None:
            return None
        assert diag.rows == self.rows
        assert diag.cols == self.cols + 1

        return diag.col_vec(v.dim)

    def gauss_jordan_inverse(self) -> Tuple[Optional["SqMatrix"], T]:
        diag, det = self.adjoin_cols(SqMatrix.identity(self.dim)).make_unit_diagonal()
        if diag is None:
            return None, 0
        assert diag.rows == self.rows
        assert diag.cols == 2 * self.cols
        return diag.extract_cols(range(self.dim, 2 * self.dim)), det

    def laplacian_expansion(self, zero: T = 0) -> T:
        def recur(dim, v):
            if dim == 1:
                return v[0][0]
            # This code ends up failing gauss_jordan_test, gaussian_test, laplacian_determinant_test
            # elif dim >= 5:
            #     return 0
            elif dim == 2:
                return v[0][0] * v[1][1] - v[1][0] * v[0][1]
            else:
                return sum(
                    (
                        v[0][k] * (-1) ** k * r
                        for k in range(dim)
                        for r in [recur(dim - 1, v.suppress_rc(0, k))]
                        if v[0][k] != zero
                    ),
                    zero,
                )

        return recur(self.dim, self)

    def cramers_rule(self, b: Vector) -> Vector:
        assert self.dim == b.dim

        detA = self.laplacian_expansion()
        if detA == 0:
            return None

        return Vector(
            tuple(
                self.replace_col(k, b).laplacian_expansion() / detA
                for k in range(b.dim)
            )
        )

    def power(self, p: int) -> "SqMatrix":
        assert isinstance(p, int)
        assert p >= 0

        if p == 0:
            return SqMatrix.identity(self.dim)
        else:
            return fast_power(self, lambda a, b: a * b, p)

    def characteristic_polynomial(self):  # --> "Polynomial"
        from matrix.Polynomial import Polynomial

        m = SqMatrix(
            [
                [
                    Polynomial([v, -1]) if c == r else Polynomial([v])
                    for c, v in enumerate(row)
                ]
                for r, row in enumerate(self.content)
            ]
        )
        return m.laplacian_expansion(Polynomial.zero())

    def eigenvalues(self, epsilon: float) -> List[float]:
        from algebra.roots import poly_roots

        assert isinstance(epsilon, float), f"epsilon={epsilon} is not a float"

        p = self.characteristic_polynomial()
        return poly_roots(p.coefs, epsilon)

    def eigenvectors(self, spectrum: List[float], epsilon=0.0000001) -> List[Vector]:
        assert spectrum == sorted(spectrum)
        if len(spectrum) != self.dim or any(
            abs(eigenvalue) < epsilon for eigenvalue in spectrum
        ):
            return None
        for k in range(len(spectrum) - 1):
            if spectrum[k + 1] - spectrum[k] < epsilon:
                return None

        def condition(matrix):
            return SqMatrix.tabulate(
                self.dim,
                lambda r, c: 0 if abs(matrix[r][c]) < epsilon else matrix[r][c],
            )

        identity_matrix = SqMatrix.identity(self.dim)
        modified_matrices = [
            condition(self - identity_matrix.scale(eigenvalue))
            for eigenvalue in spectrum
        ]

        def product(matrices):
            return reduce(lambda a, b: a * b, matrices, identity_matrix)

        modified_product_matrices = [
            product(matrices)
            for k in range(len(spectrum))
            for matrices in [
                [modified_matrices[j] for j in range(len(spectrum)) if j != k]
            ]
        ]

        vectors = []
        for k in range(len(spectrum)):
            independent_vectors = [
                column_vector
                for j in range(modified_product_matrices[k].cols)
                for column_vector in [modified_product_matrices[k].col_vec(j)]
                if column_vector.norm() > epsilon
            ]
            vectors.append(
                min(independent_vectors, key=lambda vector: vector.norm())
                if independent_vectors
                else None
            )

        return vectors

    def eigen(self, epsilon: float) -> Optional[List[Tuple[float, Vector]]]:
        spectrum = self.eigenvalues(epsilon)
        if len(set(spectrum)) != self.dim:
            return None
        if any(abs(e) < epsilon for e in spectrum):
            return None

        vectors = self.eigenvectors(spectrum)
        if vectors is None:
            return None
        return [(spectrum[k], vectors[k]) for k in range(len(vectors))]
