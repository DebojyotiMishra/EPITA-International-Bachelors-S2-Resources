from typing import List, Callable, Set, Union, Tuple

from algebra.polynomial import *
from algebra.limit import *


def signum(x):
    if x == 0:
        return 0
    if x > 0:
        return 1
    return -1


def poly_by_roots(rs: List[float]) -> List[float]:
    """Given a list of roots, generate the polynomial and return its coefficients."""

    terms = [[-r, 1] for r in rs]
    # CHALLENGE: student must complete the implementation.
    return polys_mult(terms)


def search_root(g: Callable[[float], float], left: float, right: float, epsilon: float) -> float:
    """Assuming the function, g, crosses the x-axis, find one such x value.

    If g(right) and g(left) are both positive, or both negative, then
    a recursive call is made with the new left-d and right+d,
    with d chosen so as to double the search interval.
    For this reason, search_root should never be called on a function
    which is always positive, or always negative because it will loop forever.
    """
    assert left < right

    gl = g(left)
    if gl == 0:
        # CHALLENGE: student must complete the implementation.
        return left
    gr = g(right)
    if gr == 0:
        # CHALLENGE: student must complete the implementation.
        return right
    if gl * gr > 0:
        d = abs(right - left) / 2
        # CHALLENGE: student must complete the implementation.
        return search_root(g, left - d, right + d, epsilon)
    else:
        # CHALLENGE: student must complete the implementation.
        return find_x_intercept(g, left, right, epsilon)


def roots_quadratic(coefs: List[float], epsilon=0.00001) -> List[float]:  # TODO write unit test
    """Return a list of 2 roots (perhaps equal) if the polynomial has real roots,
    else return [] if the polynomial has no real roots."""
    from math import sqrt
    assert len(coefs) == 3
    c, b, a = coefs

    discr = b * b - 4 * a * c
    if discr > 0:
        # CHALLENGE: student must complete the implementation.
        return sorted([(-b + sqrt(discr)) / (2 * a),
                       (-b - sqrt(discr)) / (2 * a)])
    elif abs(discr) < epsilon:
        # CHALLENGE: student must complete the implementation.
        r = -b / (2*a)
        return [r, r]
    else:
        # CHALLENGE: student must complete the implementation.
        return []


def find_roots_by_inflection_points(coefs: List[float], epsilon: float) -> List[float]:  # TODO write unit test
    """Given a polynomial specified by coefficients, return a list of roots.
    The function used is to find the roots of the derivative.  These roots
    identify inflection points.  We look at the inflection points in order
    of increasing x value, and find two consecutive for which the value of
    the original polynomial changes sign.  If such is found, then there is
    a root between the two x values, and it can be found using a binary
    search, for which the function search_root can be used.
    """

    roots_found = []
    f = poly_to_function(coefs)

    inflections = sorted(list(poly_roots(poly_derivative(coefs), epsilon / 10)))

    # find all adjacent inflection points where the function changes sign;
    #   binary search here for a root. Return a generator which generates
    #   these roots.  If the inflection points happen to be roots, they are
    #   returned also by this generator.
    for k in range(len(inflections) - 1):
        fleft = f(inflections[k])
        if fleft == 0:
            roots_found.append(inflections[k])
        fright = f(inflections[k + 1])
        if fright == 0:
            # CHALLENGE: student must complete the implementation.
            roots_found.append(inflections[k + 1])
        if fleft * fright < 0:  # values have opposite signs
            # now we have identified an interval where the polynomial
            #   changes sign.  There must be a root in the interval somewhere.
            #   use search_root to find it.
            # CHALLENGE: student must complete the implementation.
            root = search_root(f, inflections[k], inflections[k + 1], epsilon)
            roots_found.append(root)

    return sorted(roots_found)


def factors(n: int) -> Set[int]:
    """"Given an integer such as 12, return its factors as a set
    E.g., {1,2,3,4,6,12}
    Note that the factors include 1 and abs(n), but no negatives
    factors(-4) --> {1,2,4} all positive, even if n is negative"""
    from math import ceil, sqrt
    if n < 0:
        return factors(-n)
    else:
        # CHALLENGE: student must complete the implementation.
        return {m for m in range(2, n // 2 + 1)
                if n % m == 0}.union({1, abs(n)})


def maybeToInteger(x: float) -> Union[int, float]:
    """convert to int if there is an integer equal to x,
    else return x"""
    if isinstance(x, int):
        return x
    elif isinstance(x, float) and x == round(x):
        return int(x)
    else:
        return x


def rrt_potential_roots(coefs: List[float]) -> List[float]:
    """If each of the coefficients is either an integer
    or equal to an integer, then return the list of potential
    roots for the rational-roots-test.  I.e., all ratios a/b
    such that a is a factor of coefs[0] and b is a factor of coefs[-1].
    If at least one coefficient is not equal to an integer, then
    the rational-roots-tests fails so return [].
    The returned list contains both the positive and negative
    ratios."""
    coefs = [maybeToInteger(c) for c in coefs]
    if any(isinstance(c, float) for c in coefs):
        return []
    if coefs[0] == 0:
        return []
    if coefs[-1] == 0:
        return []
    potential_root_pairs = []
    for b in factors(coefs[-1]):  # x^n term
        for a in factors(coefs[0]):  # x^0 term
            # collect (a,b) only if (ak, bk) not already in the list for some rational k
            # this check is because eventually we want the ration a/b, and we want to
            # avoid that (ak)/(bk) is also in the list of ratios because
            # a/b= (ak)/(bk) mathematically, but might not be equal using Python
            # floating point division.
            if all(a1 * b != b1 * a
                   for a1, b1 in potential_root_pairs):
                potential_root_pairs.append((a, b))
    return [i * a / b
            for a, b in potential_root_pairs
            for i in [-1, 1]]


def poly_rational_roots(coefs: List[float], epsilon: float) -> Tuple[List[float], List[float]]:
    """apply rational-roots-test.
    If all coefs are integers, or equal to an integer such as 2.0,
      let u = coefs[-1]
      let v = coefs[0]
    If there is a rational root of the form a/b (a,b integers)
    then a|u and b|v.
    So find all factors of coefs[-1] and all factors of coefs[0]
    then iterate two consecutive loops, and try +/- each
    to identify one or more roots.
    If no rational roots are found, return ([], coefs)
    where coefs is unchanged.
    If rational roots are found, return (list-of-rational-roots, coefs)
    where coefs is the new polynomial with those roots factored out.
    The roots are returned already sorted into increasing order,
    and may contain multiple roots e.g., [-1.0, -1.0, -0.5, 1.0, 1.0, 2.0]
    If coefs has length 1, i.e., degree=0, then all the roots have
    been factored out, and a linear time remains.
    """
    from algebra.division import divide_out_root

    potential_roots = rrt_potential_roots(coefs)

    # now we have the potential roots, no other rational number can be
    # a root.  However, some of these roots might be roots of duplicity 2 or higher.
    # So we have to try each root, and factor it out, and try it again before
    # moving on to the next potential root.
    rational_roots = []
    degree = len(coefs) - 1
    while potential_roots:
        if len(rational_roots) == degree:
            # if we've found all the roots (.e., degree many)
            #   then we don't need to search for more roots.
            break
        r = potential_roots[-1]
        if abs(poly_eval(coefs, r)) < epsilon:
            # r is a root, so append it to rational_roots,
            # however, r might be a root of multiplicity > 1,
            # so don't pop it off of potential_roots just yet.
            rational_roots.append(r)
            coefs, rem = divide_out_root(r, coefs)
        else:
            # r is not a root, so just discard it
            potential_roots.pop()
    return sorted(list(rational_roots)), coefs


def poly_mid_zero_roots(coefs, epsilon):
    """If a polynomial as only leading and tail terms such as
    [a, 0, 0, 0, 0, 0, b], then depending on the degree, n,
    and the signs of a and b,
    we may be guaranteed either 1 or 2 roots.
    For even degree if a and b have opposite signs:
       we have two roots nth root of -b/a and its negative.
       for even degree and same sign of a and b, the
       rule does not apply.

    For odd degree: negative nth root of b/a, -nth_root(b/a).

    If this rule applies, then return the roots, i.e.,
    the one or two roots thus derived.
    """
    from algebra.division import divide_out_roots, divide_out_root
    # if not coefs = [x, 0, ..., 0, y]
    if any(coefs[x] != 0 for x in range(1, len(coefs) - 1)):
        return []

    degree = len(coefs) - 1

    if degree % 2 != 0:  # odd degree
        root = -signum(coefs[0]) * abs(coefs[0] / coefs[-1]) ** (1 / (len(coefs) - 1))
        p1, _ = divide_out_root(root, coefs)
        return [root]

    assert degree % 2 == 0

    if coefs[0] * coefs[-1] < 0:
        root = abs(coefs[0] / coefs[-1]) ** (1 / (len(coefs) - 1))
        p1, _ = divide_out_roots([root, -root], coefs)
        return [-root, root]

    return []


def poly_roots(coefs: List[float], epsilon: float) -> List[float]:
    """Return a list (in increasing order) of roots of the given polynomial."""
    from algebra.division import divide_out_roots, divide_out_root
    assert len(coefs) > 0, f"cannot find roots of polynomial {coefs=}"
    assert any(x != 0 for x in coefs), f"cannot find roots of the zero polynomial {coefs=}"
    degree = len(coefs) - 1

    if degree == 0:
        return []
    if coefs[-1] == 0:
        return poly_roots(coefs[0:-1], epsilon)
    if coefs[-1] < 0:
        # assure the highest order coefficient is positive
        return poly_roots(poly_scale(-1, coefs), epsilon)

    if degree == 1:
        b, a = coefs
        # CHALLENGE: student must complete the implementation.
        return [-b / a]

    if coefs[0] == 0:
        # optimization:
        # if zero is a root, then just factor it out.
        # zero is a root iff the leading coefficient is zero
        # CHALLENGE: student must complete the implementation.
        return sorted([0] + poly_roots(coefs[1:], epsilon))

    rational_roots, coefs = poly_rational_roots(coefs, epsilon)
    if rational_roots:
        return sorted(list(rational_roots) + poly_roots(coefs, epsilon))

    mid_zero_roots = poly_mid_zero_roots(coefs, epsilon)
    if mid_zero_roots:
        return mid_zero_roots

    if degree == 2:
        # use quadratic formula
        # CHALLENGE: student must complete the implementation.
        return roots_quadratic(coefs, epsilon)

    if degree % 2 != 0:  # odd degree
        f = poly_to_function(coefs)
        r = search_root(f, -1.0, 1.0, epsilon)
        # CHALLENGE: student must complete the implementation.
        p2, remainder = divide_out_root(r, coefs)
        return sorted(poly_roots(p2, epsilon) + [r])

    # even degree
    rs = find_roots_by_inflection_points(coefs, epsilon)
    if rs:
        # CHALLENGE: student must complete the implementation.
        p2, remainder = divide_out_roots(rs, coefs)
        return sorted(poly_roots(p2, epsilon) + rs)

    # otherwise we are unable to find any roots
    return []
