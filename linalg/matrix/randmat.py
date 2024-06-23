import random
from math import prod
from common.utils import shuffle
from matrix.SqMatrix import SqMatrix

matrices = {2: [SqMatrix([[1, 2],
                          [2, -1]]),
                SqMatrix([[0, 1],
                          [1, 1]])],
            3: [SqMatrix([[1, 2, 3],
                          [-1, 2, 3],
                          [1, -2, 3]]),
                SqMatrix([[1, -2, -2],
                          [3, -1, 1],
                          [1, 1, 1]])],
            4: [SqMatrix([[1, 2, 3, -1],
                          [-1, 2, 3, -2],
                          [1, -2, 3, 2],
                          [1, 1, -1, 1]]),
                SqMatrix([[1, -2, -2, 1],
                          [3, -1, -1, 0],
                          [1, 2, 1, -1],
                          [1, 1, 1, 0]])],
            5: [SqMatrix([[1, 2, 3, -1, 1],
                          [-1, 2, 3, -2, -1],
                          [-1, 2, 3, -2, 0],
                          [1, -2, 3, 2, 1],
                          [1, 1, -1, 1, 1]]),
                SqMatrix([[1, -2, -2, 1, 1],
                          [3, -1, -1, 0, 2],
                          [3, -1, -1, 0, 1],
                          [1, 2, 1, -1, -1],
                          [1, 1, 1, 0, -1]])],
            6: [SqMatrix([[1, 2, 3, -1, 1, 1],
                          [-1, 2, 3, -2, -1, -1],
                          [-1, 2, 3, -2, -1, 0],
                          [-1, 2, 3, -2, 0, 1],
                          [1, -2, 3, 2, 1, -1],
                          [1, 1, -1, 1, 1, -2]]),
                SqMatrix([[1, -2, -2, 1, 1, 1],
                          [3, -1, -1, 0, 2, -1],
                          [3, -1, -1, 0, 1, -1],
                          [3, -1, -1, 0, 1, 0],
                          [1, 2, 1, -1, -1, 2],
                          [1, 1, 1, 0, -1, -1]])],
            7: [SqMatrix([[1, 1, 2, 3, -1, 1, 1],
                          [-1, 1, 2, 3, -2, -1, -1],
                          [-1, 2, 1, 3, -2, -1, -1],
                          [-1, 2, 3, 1, -2, -1, 0],
                          [-1, 2, 3, -2, 1, 0, 1],
                          [1, -2, 3, 2, 1, 1, -1],
                          [1, 1, -1, 1, 1, -2, 1]]),
                SqMatrix([[1, -2, -2, 1, 1, 1, 1],
                          [3, -1, -1, 1, 0, 2, -1],
                          [3, -1, -1, -1, 0, 1, -1],
                          [-1, 2, 3, -1, -2, -1, -1],
                          [3, -1, -1, 0, 1, 1, 0],
                          [-1, 2, 3, -2, -1, -1, -1],
                          [1, 1, 1, -1, 0, -1, -1]])]}

for i in range(2, 5):
    for j in range(len(matrices[i])):
        m = matrices[i][j]
        assert 0 != m.laplacian_expansion(), f"invertible {i=} {j=}"

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

        return m, det

    m, det = rand_matrix()
    while abs(det) < min_det or abs(det) > max_det:
        # print(f"oops, {det=} ")
        m, det = rand_matrix()

    #print(f"{dim=} {det=}")
    return m * random.choice(matrices[dim])
