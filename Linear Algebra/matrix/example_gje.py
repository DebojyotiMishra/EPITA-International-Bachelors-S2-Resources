from matrix.randmat import random_invertible
from matrix.SqMatrix import SqMatrix
from matrix.Vector import Vector


def starting_matrix():
    return SqMatrix(((2.5, 2.5, 2.5e6, 1.3e-6),
                     (2.5e7, -5.0, -5.0e7, 2.5),
                     (-7.5, 2.5e4, 2.5, 0.0),
                     (1.0e-5, 2.0e9, 1.0, -1.0))).adjoin_col(Vector([1, 2, -1, 0]))


def example_gje_with_pivot():
    m = starting_matrix()
    print(m)
    m = m.swap_rows(0, 2)
    print(m)
    m = m.scale_row(1 / m[0][0], 0)
    print(m)
    m = m.row_operation(-m[1][0], 0, 1, 1) \
        .row_operation(-m[2][0], 0, 1, 2) \
        .row_operation(-m[3][0], 0, 1, 3)
    print(m)
    m = m.scale_row(1 / m[1][1], 1)
    print(m)
    m = m.row_operation(-m[0][1], 1, 1, 0) \
        .row_operation(-m[2][1], 1, 1, 2) \
        .row_operation(-m[3][1], 1, 1, 3)
    print(m)
    m = m.swap_rows(2, 3)
    print(m)

    m = m.scale_row(1 / m[2][2], 2)
    print(m)
    m = m.row_operation(-m[0][2], 2, 1, 0) \
        .row_operation(-m[1][2], 2, 1, 1) \
        .row_operation(-m[3][2], 2, 1, 3)
    print(m)
    m = m.scale_row(1 / m[3][3], 3)
    print(m)
    m = m.row_operation(-m[0][3], 3, 1, 0) \
        .row_operation(-m[1][3], 3, 1, 1) \
        .row_operation(-m[2][3], 3, 1, 2)
    print(m)


def example_gje_no_pivot():
    m = starting_matrix()
    print(m)
    m = m.scale_row(1 / m[0][0], 0)
    print(m)
    m = m.row_operation(-m[1][0], 0, m[0][0], 1) \
        .row_operation(-m[2][0], 0, m[0][0], 2) \
        .row_operation(-m[3][0], 0, m[0][0], 3)
    print(m)
    m = m.scale_row(1 / m[1][1], 1)
    print(m)
    m = m.row_operation(-m[0][1], 1, m[1][1], 0) \
        .row_operation(-m[2][1], 1, m[1][1], 2) \
        .row_operation(-m[3][1], 1, m[1][1], 3)
    print(m)
    m = m.swap_rows(2, 3)
    print(m)
    m = m.scale_row(1 / m[2][2], 2)
    print(m)
    m = m.row_operation(-m[0][2], 2, m[2][2], 0) \
        .row_operation(-m[1][2], 2, m[2][2], 1) \
        .row_operation(-m[3][2], 2, m[2][2], 3)
    print(m)
    m = m.scale_row(1 / m[3][3], 3)
    print(m)
    m = m.row_operation(-m[0][3], 3, m[3][3], 0) \
        .row_operation(-m[1][3], 3, m[3][3], 1) \
        .row_operation(-m[2][3], 3, m[3][3], 2)
    print(m)



def example_inverse():
    m = SqMatrix(((2, 0, 5, 2),
                  (-1, 0, 1, -1),
                  (1, -4, -1, 3),
                  (-5, 4, -4, -1))).adjoin_cols(SqMatrix.identity(4))
    c = 0
    p = m.find_pivot_row(c)
    print([c,p])
    m = m.swap_rows(c, p)
    m = m.scale_row(1 / m[c][c], c)
    m = m.row_operation(-m[1][c], c, 1, 1) \
        .row_operation(-m[2][c], c, 1, 2) \
        .row_operation(-m[3][c], c, 1, 3)
    print(m)

    c = 1
    p = m.find_pivot_row(c)
    print([c,p])
    m = m.swap_rows(c, p)
    m = m.scale_row(1 / m[c][c], c)
    m = m.row_operation(-m[0][c], c, 1, 0) \
        .row_operation(-m[2][c], c, 1, 2) \
        .row_operation(-m[3][c], c, 1, 3)
    print(m)

    c = 2
    p = m.find_pivot_row(c)
    print([c,p])
    m = m.swap_rows(c, p)
    m = m.scale_row(1 / m[c][c], c)
    m = m.row_operation(-m[0][c], c, 1, 0) \
        .row_operation(-m[1][c], c, 1, 1) \
        .row_operation(-m[3][c], c, 1, 3)
    print(m)

    c = 3
    m = m.scale_row(1 / m[c][c], c)
    m = m.row_operation(-m[0][c], c, 1, 0) \
        .row_operation(-m[1][c], c, 1, 1) \
        .row_operation(-m[2][c], c, 1, 2)
    print(m)

if __name__ == '__main__':
    # example_gje_with_pivot()
    # print("----------------------")
    # example_gje_no_pivot()
    #example_inverse()
    pass
