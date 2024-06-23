from typing import TypeVar, Callable, Any, Optional

from common.utils import trace
from structure.Group import is_abelian_group

F = TypeVar("F")


def is_field(
    member: Callable[[Any], bool],
    add: Callable[[F, F], F],
    mult: Callable[[F, F], F],
    zero: F,
    one: F,
    additive_inverse: Callable[[F], Optional[F]],
    multiplicative_inverse: Callable[[F], Optional[F]],
    equivalent: Callable[[F, F], bool],
    gen: Callable[[], F],
    iterations: int,
) -> bool:
    def gen_non_zero() -> F:
        elt = gen()
        while equivalent(elt, zero):
            elt = gen()
        return elt

    def distributive() -> bool:
        for k in range(iterations):
            x1 = gen()
            x2 = gen()
            x3 = gen()
            if not equivalent(mult(x1, add(x2, x3)), add(mult(x1, x2), mult(x1, x3))):
                return False
        return True
        # return all(
        #     equivalent(mult(x1, add(x2, x3)), add(mult(x1, x2), mult(x1, x3)))
        #     for k in range(iterations)
        #     for x1 in [gen()]
        #     for x2 in [gen()]
        #     for x3 in [gen()]
        # )

    def is_closed(f) -> bool:
        for k in range(iterations):
            x1 = gen()
            x2 = gen()
            if not member(f(x1, x2)):
                return False
        return True
        # return all(
        #     member(f(x1, x2))
        #     for k in range(iterations)
        #     for x1 in [gen()]
        #     for x2 in [gen()]
        # )

    def is_associative(f) -> bool:
        for k in range(iterations):
            x1 = gen()
            x2 = gen()
            x3 = gen()
            if not equivalent(f(x1, f(x2, x3)), f(f(x1, x2), x3)):
                return False
        return True
        # return all(
        #     equivalent(f(x1, f(x2, x3)), f(f(x1, x2), x3))
        #     for k in range(iterations)
        #     for x1 in [gen()]
        #     for x2 in [gen()]
        #     for x3 in [gen()]
        # )

    def is_commutative(f) -> bool:
        for k in range(iterations):
            x1 = gen()
            x2 = gen()
            if not equivalent(f(x1, x2), f(x2, x1)):
                return False
        return True
        # return all(
        #     equivalent(f(x1, x2), f(x2, x1))
        #     for k in range(iterations)
        #     for x1 in [gen()]
        #     for x2 in [gen()]
        # )

    def member_non_zero(x):
        return member(x) and not equivalent(x, zero)

    return (
        member(zero)
        and member(one)
        and is_closed(mult)
        and is_associative(mult)
        and is_commutative(mult)
        and is_abelian_group(
            member, add, zero, additive_inverse, equivalent, gen, iterations
        )
        and is_abelian_group(
            member_non_zero,
            mult,
            one,
            multiplicative_inverse,
            equivalent,
            gen_non_zero,
            iterations,
        )
        and distributive()
    )
