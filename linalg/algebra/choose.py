from typing import TypeVar, Callable, List
from algebra.recursion import factorial

T = TypeVar('T')


def prime_factors(n: int) -> List[int]:
    """Returns the list of prime factors of the given integer,
    in increasing order.  If a factor occurs multiple times, it is included
    that many times in the result, so that the product of the factors
    is the given numbers.   The list of factors of 12 is [2, 2, 3].
    Note that the list of prime factors of 1 is [].
    This function should never be called with n=0, as it is impossible to
    return a list of prime numbers whose product is 0."""
    from math import sqrt, ceil
    assert n > 0

    # CHALLENGE: student must complete the implementation.
    def loop(start, n):
        if n == 1:
            return []
        # find a factor of n
        p = next((p
                  for p in range(start, ceil(sqrt(n)) + 1)
                  if n % p == 0),
                 None)
        if p is None:
            # then n is prime
            return [n]
        else:
            # then n is composite and its smallest prime factor is p
            return [p] + loop(p, n // p)

    return loop(2, n)


def factorial_factors(n: int) -> List[int]:
    """Return the list of prime factors of n! in ascending order. [2,2,3,....]
    If a prime number appears more than once as a factor of n!, it should appear
    multiple times in the returned list.
    The product of the values of the list must equal n!.
    However, this function does not compute n! explicitly, and does
    not call the factorial function.
    Note, the list of prime factors of 1! is []
    Also, the list of prime factors of 0! is []
    """

    # CHALLENGE: student must complete the implementation.
    return sorted([pf
                   for k in range(2, n + 1)
                   for pf in prime_factors(k)])


def choose_direct(n: int, k: int) -> int:
    """Compute n choose k directly as n! / ( k! * (n-k)!).
    n! is computed by a call to factorial."""
    # CHALLENGE: student must complete the implementation.
    return factorial(n) // (factorial(k) * factorial(n - k))


def choose_pascal(n: int, k: int) -> int:
    """Compute n choose k by Pascal's triangle.
    I.e., compute an entry by adding the two entries
    (left and right) in the line above in Pascals triangle.
    The recursion terminates which a 1 on the boundary is encountered.
    This function has exponential complexity, so it will not work for
    large values of n. You should be able to test the function at least
    up to n=20"""
    assert isinstance(n, int)
    assert isinstance(k, int)
    assert n >= k
    assert n > 0
    assert k >= 0
    # CHALLENGE: student must complete the implementation.

    if k == 0:
        return 1
    elif k == 1:
        return n
    elif k == n:
        return 1
    else:
        return choose_pascal(n - 1, k - 1) + choose_pascal(n - 1, k)


def cancel_factors(numerator_factors: List[int], denominator_factors: List[int]) -> List[int]:
    """Return a new list of numerator factors, having all the denominator
    factors removed.   Warning, the same factor may appear multiple times in
    the numerator and denominator.
    cancel_factors([2,3,2,3,3,3],[3,2,3]) should return [2,3,3], having
    only removed one 2, and having removed two 3's.
    The return list may have elements in any order, they are not required to be
    sorted.
    You may assume that all the denominator factors appear in the numerator
    at least as many times as they appear in the denominator. E.g., if 3 is
    in denominator_factors 4 times, then it is guaranteed to be in
    numerator_factors 4 or more times.
    """
    # CHALLENGE: student must complete the implementation.
    # must make a copy first, because numerator_factors.remove(d)
    nf = numerator_factors[:]
    for d in denominator_factors:
        nf.remove(d)
    return nf


def choose_factors(n: int, k: int) -> int:
    """Compute n choose k by computing the prime factors of n!, k! and (n-k)!,
    then removing all the factors of k! and (n-k)! from the factors of n!.
    The un-cancelled factors of n! can then be multiplied together to obtain
    the desired result.
    This function does not make any call to factorial.  Prime factors
    of n! are computed by a call to factorial_factors."""
    assert isinstance(n, int)
    assert isinstance(k, int)
    assert n >= k
    assert n > 0
    assert k >= 0
    # CHALLENGE: student must complete the implementation.
    from math import prod

    return prod(cancel_factors(factorial_factors(n),
                               factorial_factors(k) + factorial_factors(n - k)))


def choose_linear(n: int, k: int) -> int:
    """Compute the number of combinations of n things taken k at a time.
    We assume that n and k are both integers, and that n > 0, k >= 0,
    and n >= k.
    The method used is to multiply n-1 choose k-1 by n//k.
    Careful of the cases which must terminate the recursion.
    """
    assert isinstance(n, int)
    assert isinstance(k, int)
    assert n >= k
    assert n > 0
    assert k >= 0
    # CHALLENGE: student must complete the implementation.

    if k == 0:
        return 1
    elif k == 1:
        return n
    elif n - k < k:
        return choose_linear(n, n - k)
    else:
        return choose_linear(n - 1, k - 1) * n // k
