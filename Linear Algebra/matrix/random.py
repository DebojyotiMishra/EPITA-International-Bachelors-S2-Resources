from matrix.SqMatrix import SqMatrix
import random
from math import prod
from common.utils import shuffle


def random_invertible(dim: int, min_det: float = 0.0001, max_det=20.0):
    """Generate a random invertible SqMatrix of the given dimension,
    whose determinant > epsilon or < -epsilon """
    assert 0 < min_det < max_det

    def rand_diagonal():
        diag = [rand_element() for i in range(dim)]
        return SqMatrix.diagonal(diag), prod(diag)

    def rand_sparse():
        m, det = rand_diagonal()
        return SqMatrix(shuffle(m.content)), det

    def rand_element():
        return random.choice([1.0, -1.0, 2.0, -2.0, 2.5, -2.5, 0.5, 0.25])

    def rand_matrix():
        m, det = rand_sparse()
        for i in range(2 * dim):
            m2, det2 = rand_sparse()
            m *= m2
            det *= det2

        return m, det

    m, det = rand_matrix()
    while abs(det) < min_det or abs(det) > max_det:
        # print(f"oops, {det=} ")
        m, det = rand_matrix()

    #print(f"{dim=} {det=}")
    return m
