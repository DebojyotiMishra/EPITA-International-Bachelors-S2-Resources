def quad_roots(a, b, c):
    """Return a list of two (real) roots of the quadratic polynomial, a x^2 + bx + c.
    If the polynomial one root, return a list of the same root, repeated, list of length 2.
    If the polynomial has no real root, return None."""
    # CHALLENGE: student must complete the implementation.
    from math import sqrt
    discr = b * b - 4 * a * c
    if discr >= 0:
        return [(-b + sqrt(discr)) / (2 * a),
                (-b - sqrt(discr)) / (2 * a)]
    else:
        return None
