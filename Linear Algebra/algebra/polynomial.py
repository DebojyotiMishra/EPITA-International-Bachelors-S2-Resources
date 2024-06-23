from typing import TypeVar, List, Callable

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

def poly_degree(coefs):
    """Return the degree of the given polynomial.
    This is the highest exponent ignoring coefficients """
    # TODO, student should implement this, for now, the solution is given
    assert len(coefs) > 0, f"[] is not a valid polynomial"
    if len(coefs) == 1:
        # CHALLENGE: student must complete the implementation.
        return 0
    elif coefs[-1] == 0:
        # CHALLENGE: student must complete the implementation.
        return poly_degree(coefs[0:-1])
    else:
        # CHALLENGE: student must complete the implementation.
        return len(coefs) - 1


def poly_chop(coefs: List[float]) -> List[float]:
    """Return the list of coefficients with all unnecessary """
    # CHALLENGE: student must complete the implementation.
    return coefs[0:poly_degree(coefs) + 1]


def poly_pad_right(n: int, coefs: List[float]) -> List[float]:
    """Extend coefs to length of n by appending 0's to the
    tail as necessary.  If len(coefs) > n, then do nothing.
    return the new list, without modifying the given one."""
    if len(coefs) >= n:
        return coefs
    else:
        return coefs + [0] * (n - len(coefs))


def poly_equal(coefs1: List[float], coefs2: List[float]) -> bool:
    """Detect whether two given list of coefficients specify the same
    polynomial.  I.e., are the lists the same except for trailing
    zeros?
    """
    # CHALLENGE: student must complete the implementation.
    return poly_chop(coefs1) == poly_chop(coefs2)


def poly_add(coefs1: List[float], coefs2: List[float]) -> List[float]:
    """Given two polynomials in terms of their coefficients, return the
    coefficients of the polynomial representing their sum."""
    assert len(coefs1) > 0
    assert len(coefs2) > 0
    assert all(isinstance(x, float) or isinstance(x, int) for x in coefs1), f"expecting list of numbers: {coefs1}"
    assert all(isinstance(x, float) or isinstance(x, int) for x in coefs2), f"expecting list of numbers: {coefs2}"
    # CHALLENGE: student must complete the implementation.

    if len(coefs1) == len(coefs2):
        return [coefs1[k] + coefs2[k]
                for k in range(len(coefs1))]
    elif len(coefs1) < len(coefs2):
        return poly_add(coefs1 + [0] * (len(coefs2) - len(coefs1)),
                        coefs2)
    else:
        return poly_add(coefs2, coefs1)


def poly_sub(coefs1: List[float], coefs2: List[float]) -> List[float]:
    """Return the difference (subtraction) of the polynomials,
    i.e., coefs1 - coefs2"""
    return poly_add(coefs1, poly_scale(-1, coefs2))


def polys_add(coefss: List[List[float]]) -> List[float]:
    """Given a list of polynomials (each polynomial is a list
        of coefficients) compute the coefficients of the sum (addition)
        of all the polynomials.
        If the list of polynomials is empty [0] is returned."""
    from functools import reduce
    assert isinstance(coefss, list)
    assert all(isinstance(x, list) for x in coefss)
    # CHALLENGE: student must complete the implementation.

    return reduce(poly_add, coefss, [0])


def poly_scale(s: float, coefs: List[float]) -> List[float]:
    """Given a polynomial and a scalar (number), return
    the new polygon equal to the original scaled by the scalar."""
    # CHALLENGE: student must complete the implementation.

    return [s * c for c in coefs]


def poly_mult(coefs1: List[float], coefs2: List[float]) -> List[float]:
    """Given two polynomials in terms of their coefficients, return the
        coefficients of the polynomial representing their product."""
    assert len(coefs1) > 0
    assert len(coefs2) > 0
    assert all(isinstance(x, float) or isinstance(x, int) for x in coefs1), f"expecting list of numbers: {coefs1}"
    assert all(isinstance(x, float) or isinstance(x, int) for x in coefs2), f"expecting list of numbers: {coefs2}"
    # CHALLENGE: student must complete the implementation.

    partials = [[0] * i + poly_scale(coefs1[i], coefs2)
                for i in range(len(coefs1))]
    return polys_add(partials)


def polys_mult(polynomials: List[List[float]]) -> List[float]:
    """Given a list of polynomials (each polynomial is a list
    of coefficients) compute the coefficients of the product (multiplication)
    of all the polynomials.   If the list of polynomials is empty [1] is returned."""
    from functools import reduce
    # CHALLENGE: student must complete the implementation.

    return reduce(poly_mult, polynomials, [1])


def poly_power(coefs: List[float], p: int) -> List[float]:
    """Compute a polynomial specified by coefs, raised to integer power p, assuming p >= 0.
    It is guaranteed that poly_mult is not called more than 2*log(p)  (log base 2)"""
    from algebra.recursion import power
    # CHALLENGE: student must complete the implementation.
    return power(coefs, p, poly_mult, [1])


def poly_eval(coefs: List[float], x: float) -> float:
    """Given the coefficients of a polynomial and a value of x,
    return the value of the polynomial evaluated at x."""
    # CHALLENGE: student must complete the implementation.

    return sum(coefs[n] * x ** n
               for n in range(len(coefs)))


def poly_to_function(coefs: List[float]) -> Callable[[float], float]:
    """Convert a set of polynomial coefficients into a function from float to float.
    poly_to_function returns a function, which can be called multiple times
    with a single argument.  That function evaluates the polynomial at the given x.
    Example function call taken from handout:
    >>> p = poly_to_function([3, -1, 0, 3])
    >>> p(1)
    5"""

    # CHALLENGE: student must complete the implementation.

    def f(x):
        return poly_eval(coefs, x)

    return f
