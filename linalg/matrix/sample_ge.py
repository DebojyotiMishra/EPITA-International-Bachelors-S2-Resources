from pprint import pprint

from matrix.SqMatrix import SqMatrix
from matrix.Vector import Vector

def test_it():
    print("\n")
    a = SqMatrix([[0, 1, 1], [3, -1, 1], [2, 1, 0]])
    x = Vector([2, -1, 5])
    b = a*x
    a0 = a.adjoin_col(b)
    print(a0.format())
    a1 = a0.swap_rows(2, 0)
    print(a1.format())
    a2 = a1.row_operation(3, 0, -2, 1)
    print(a2.format())
    a3 = a2.swap_rows(1, 2)
    print(a3.format())
    a4 = a3.row_operation(5,1,-1,2)
    print(a4.format())
    print("\n")
    pprint(a4.content, depth=1)

def test_it2():
    a = SqMatrix([[0, 2, 1, 1], [1, -1, -2, 3], [2, -2, 1, 0], [3, -2, 0, 1]])
    x = Vector([-1,1,2,-3])
    b = a*x
    a0 = a.adjoin_col(b)
    a1 = a0.swap_rows(0,1)
    a2 = a1.row_operation(2, 0, -1, 2)
    a3 = a2.row_operation(3, 0, -1, 3)

    a4 = a3.swap_rows(1,3)
    a5 = a4.row_operation(2,1,1,3)

    a6 = a5.row_operation(-11,2,5,3)
    print("\n")
    print(a6.format())
    print(a.gaussian_elimination_back_substitution(b))

def test_cramers_rule():
    a = SqMatrix([[0, 2, 1, 1], [1, -1, -2, 3], [2, -2, 1, 0], [3, -2, 0, 1]])
    x = Vector([-1, 1, 2, -3])
    b = a * x
    det_a = a.laplacian_expansion()

    x0 = a.replace_col(0,b).laplacian_expansion() / det_a
    x1 = a.replace_col(1,b).laplacian_expansion() / det_a
    x2 = a.replace_col(2,b).laplacian_expansion() / det_a
    x3 = a.replace_col(3,b).laplacian_expansion() / det_a


    print(Vector([x0,x2,x2,x3]))

