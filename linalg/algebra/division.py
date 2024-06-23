from typing import TypeVar, List, Tuple

T = TypeVar('T')


# In this file we consider a list of number, either a list of int or list
# of float as a list of coefficients of a polynomial.   coefs[0] is the
# coefficient of x^0, coefs[1] is the coefficient of x^1, ..., coefs[n]
# is the coefficient of x^n.
# Thus, the polynomial 2x^3 - x^2 + 4 is represented as [4, 0, -1, 2].
# Be careful, the order of the coefficients is reversed from the normal way a polynomial is usually written.
# For example, in the list mentioned above [4, 0, -1, 2], the coefficients correspond to the polynomial:
# 2x^3 (coefficient 2 for x^3 term)
# -x^2 (coefficient -1 for x^2 term)
# 0 (no x term, hence coefficient 0 for x^1 term)
# 4 (constant term)
# Thus, the polynomial 2x^3 - x^2 + 4 is represented by the list [4, 0, -1, 2].


def poly_divide(numerator: List[float], denominator: List[float]) -> Tuple[List[float], List[float]]:
    """Divide one polynomial by another producing a quotient and remainder.
    numerator / denominator.
    If the denominator is the zero polynomial, an except is raised."""
    from algebra.polynomial import poly_add, poly_mult, poly_sub, poly_degree
    from algebra.polynomial import poly_chop, poly_pad_right
    denominator = poly_chop(denominator)
    if all(k == 0 for k in denominator):  # if denominator is the 0 polynomial
        raise Exception(f"polynomial division by zero: {numerator}/{denominator}")
    elif all(k == 0 for k in numerator):  # if numerator is the 0 polynomial
        return [0], [0]
    elif len(numerator) == len(denominator) == 1:  # if constant polynomial / constant polynomial
        return [numerator[0] / denominator[0]], [0]
    # (1 + x + x^2 + x^3 + 0x^4)  / (1 + x)
    #  --> (1 + x + x^2 + x^3)  / (1 + x)
    # elif numerator[-1] == 0:
    #     return poly_divide(numerator[0:-1], denominator)
    elif len(numerator) < len(denominator):  # if degree of numerator < degree of denominator
        return [0], numerator
    else:  # len(numerator) >=  len(denominator)
        # CHALLENGE: student must complete the implementation.
        # e.g., 12x^4 + x^3 + x^2 + x + 1      [1, 1, 1, 1 ,12]
        #       ------------------------- =   ----------------
        #              3x^2 + x + 1               [1, 1, 3]
        #  d = 5 - 3 = 2, i.e., we will compute the coefficient of x^d in the quotient
        d = poly_degree(numerator) - poly_degree(denominator)
        #  s = 12 / 3 = 4
        s = numerator[-1] / denominator[-1]
        #  leading = 4x^2 ==> [0, 0, 4]
        leading = [0] * d + [s]
        #  subtrahend = 4x^2 *  (3x^2 + x + 1)  = 12x^4 + 4x^3 +4x^2
        #  ==> [0, 0, 4] * [1, 1, 3] = [0, 0, 4, 4, 12]
        subtrahend = poly_mult(leading, denominator)
        #  n2 = [1, 1,  1,  1 ,12]
        #     - [0, 0,  4,  4, 12]
        #     = [1, 1, -3, -3, 0]
        new_numerator = poly_sub(numerator, subtrahend)
        new_numerator = poly_pad_right(len(numerator), new_numerator)[0:-1]

        # now compute [1, 1, -3, -3]     -3x^3 - 3x^2 + x + 1
        #             --------------- = ---------------------- -> q, r
        #                [1, 1, 3]           3x^2 + x + 1

        q, r = poly_divide(new_numerator, denominator)
        # r is the remainder
        # the quotient is leading + q
        return poly_add(q, leading), r


def divide_out_root(r: float, coefs: List[float]) -> Tuple[List[float], float]:
    """Divide the polynomial by (x-r).
    Return the quotient and remainder as (polynomial, coef)"""

    # CHALLENGE: student must complete the implementation.

    def synthetic(k, carry):
        if k >= 0:
            c2 = coefs[k] + carry
            return synthetic(k - 1, c2 * r) + [c2]
        else:
            return []

    s = synthetic(len(coefs) - 1, 0)
    return s[1:], s[0]


def divide_out_roots(rs: List[float], coefs: List[float]) -> Tuple[List[float], List[float]]:
    """Perform a sequence of divisions, one for each "suspected root" given in rs.
    Each division produces a quotient and remainder.  The remainder is 0 if the suspected
    root is an actual root.
    Return a tuple of the quotient polynomial, and the remainders of each successive
    division, in order.
    """
    # CHALLENGE: student must complete the implementation.

    c2 = coefs
    rems = []
    for r in rs:
        c2, rem = divide_out_root(r, c2)
        rems.append(rem)
    return c2, rems
