from algebra.polynomial import *


class Polynomial:
    def __init__(self, content):
        assert len(content) > 0

        self.coefs = content

    def __repr__(self):
        return f"Polynomial{self.coefs}"

    def __getitem__(self, items):
        return self.coefs[items]

    def __add__(self, other):
        """create and return a new Vector which is the sum (addition) of the
        two given vectors, self and other. raise an error if the dimensions
        are not compatible to add."""
        assert isinstance(other, Polynomial)

        return Polynomial(poly_add(self.coefs, other.coefs))

    def scale(self, scalar):
        return Polynomial(poly_scale(scalar, self.coefs))

    def __mul__(self, other):
        from matrix.Matrix import Matrix
        if isinstance(other, int) or isinstance(other, float):
            return self.scale(other)
        if isinstance(other, Polynomial):
            return Polynomial(poly_mult(self.coefs, other.coefs))
        # Polynomial * Matrix -> Matrix
        if isinstance(other, Matrix):
            return Matrix.tabulate(other.rows, other.cols,
                                   lambda r, c: self.scale(other[r][c]))
        else:
            raise RuntimeError(f"cannot multiply {self} by {other}")

    def __sub__(self, other):
        return self + (other * -1)

    def __call__(self, x):
        return poly_eval(self.coefs, x)

    @staticmethod
    def zero():
        return Polynomial([0])
