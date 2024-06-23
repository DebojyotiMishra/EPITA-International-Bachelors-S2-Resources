from common.utils import trace
from typing import TypeVar, Callable, Tuple
from matrix.Vector import Vector

M = TypeVar("M")


def is_metric_space(
    d: Callable[[M, M], float], gen: Callable[[], M], iterations: int
) -> bool:
    """Apply heuristics to determine whether the described set is a metric space.
    Args:
        d: a binary function proposed as a distance function
        gen: a zero-ary function to generate an element of the set
        iterations: minimum number of times each metric space axiom should be tested.

    This function tests each of the metric space axioms at least `iterations` number
    of times to attempt to falsify the metric space axioms.

    Some axioms may remain unchecked (or may be tested fewer than `iterations` number
    of times) if an axiom is found to be violated.
    """

    def is_positive() -> bool:
        for r in range(iterations):
            x = gen()
            y = gen()
            if x != y:
                if d(x, y) == 0:
                    return False
        return True

    def is_definite() -> bool:
        epsilon = 0.001
        return all(d(x, x) < epsilon for _k in range(iterations) for x in [gen()])

    def is_symmetric():
        epsilon = 0.001
        for r in range(iterations):
            x = gen()
            y = gen()
            if abs(d(x, y) - d(y, x)) > epsilon:
                return False
        return True

    def triangle_inequality_holds():
        epsilon = 0.001
        for r in range(iterations):
            x = gen()
            y = gen()
            z = gen()
            dxz = d(x, z)
            dxy = d(x, y)
            dyz = d(y, z)
            if dxz - epsilon > dxy + dyz:
                return False
        return True

    return (
        is_positive()
        and is_definite()
        and is_symmetric()
        and triangle_inequality_holds()
    )


def discrete_distance(x, y):
    """Implementation of the discrete metric.  Suppose that == works
    for the given values, x and y."""
    return 0 if x == y else 1


def manhattan_distance(v1: Vector, v2: Vector):
    """Implementation of the taxi-cab, Manhattan metric.
    Raises an error if the given Vectors are not of the
    same dimension."""
    assert v1.dim == v2.dim
    return sum(abs(v1[k] - v2[k]) for k in range(v1.dim))


from math import atan2, cos, sin, acos, pi, isclose, sqrt


def geodesic_distance(pt1: Tuple[float, float], pt2: Tuple[float, float]) -> float:
    """Takes two points of the form (degrees-latitude, degrees-longitude),
    returns the distance (in km) on the surface of the earth between the
    two designated points. This assumes the earth is a perfect sphere with
    radius 6371.0 km."""
    r_earth = 6371.0  # radius of earth in km
    phi1d, lambda1d = pt1
    phi2d, lambda2d = pt2
    assert -180 <= lambda1d <= 180
    assert -180 <= lambda2d <= 180
    assert -90 <= phi1d <= 90
    assert -90 <= phi2d <= 90

    phi1 = phi1d * pi / 180
    phi2 = phi2d * pi / 180
    lambda1 = lambda1d * pi / 180
    lambda2 = lambda2d * pi / 180

    delta_phi = phi2 - phi1
    delta_lambda = lambda2 - lambda1

    a = sin(delta_phi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(delta_lambda / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return r_earth * c
