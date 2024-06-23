from typing import TypeVar, Callable, List

T = TypeVar('T')


def is_injection(f: Callable[[T], T], xs: List[T], ys: List[T]) -> bool:
    """Return a bool indicating whether the function f is an
    injection from domain:xs to range:ys"""
    # CHALLENGE: student must complete the implementation.
    return all(f(x) in ys
               for x in xs) and \
        all(x1 == x2
            for x1 in xs
            for x2 in xs
            if f(x1) == f(x2))


def is_surjection(f: Callable[[T], T], xs: List[T], ys: List[T]) -> bool:
    """Return a bool indicating whether the function f is an
        injection from domain:xs to range:ys"""
    # CHALLENGE: student must complete the implementation.

    return all(f(x) in ys
               for x in xs) and \
        all(any(f(x) == y
                for x in xs)
            for y in ys)


def is_bijection(f: Callable[[T], T], xs: List[T], ys: List[T]) -> bool:
    """Return a bool indicating whether the function f is an
        injection from domain:xs to range:ys"""
    # CHALLENGE: student must complete the implementation.

    return is_surjection(f, xs, ys) and is_injection(f, xs, ys)
