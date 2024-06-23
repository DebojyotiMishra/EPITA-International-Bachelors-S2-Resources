from typing import TypeVar, Callable, Any, Optional
from common.utils import trace

G = TypeVar("G")


def is_group(
    member: Callable[[Any], bool],
    op: Callable[[G, G], G],
    identity: G,
    inverse: Callable[[G], Optional[G]],
    equivalent: Callable[[G, G], bool],
    gen: Callable[[], G],
    iterations: int,
) -> bool:
    """Apply heuristics to determine whether the described set is a group.
    I.e., 1) is the set closed under the given operation?
    2) does every element have an inverse?
    3) is the operation associative?
    4) is the given `identity` an element of the set?
    Args:
        member: a predicate determining whether the given element is in the set
        op: a binary operator which can be called on any element of the set
        identity: a proposed element of the set acting as the identity for the given operation
        inverse: a function which inverts a given element
        equivalent: binary predicate testing equivalence between elements
        gen: a zero-ary function to generate(randomly select) an element of the set.
        iterations: minimum number of checks to make for each group axiom
    For each of the group axioms, perform at least `iterations` number of tests
    of randomly selected (randomly generated) elements to attempt to find
    falsify a group axiom.
    """

    def is_closed() -> bool:
        for k in range(iterations):
            x1 = gen()
            x2 = gen()
            if not member(op(x1, x2)):
                return False
        return True
        # return all(member(op(x1, x2))
        #            for k in range(iterations)
        #            for x1 in [gen()]
        #            for x2 in [gen()])

    def is_associative() -> bool:
        for k in range(iterations):
            x1 = gen()
            x2 = gen()
            x3 = gen()
            if not equivalent(op(x1, op(x2, x3)),
                              op(op(x1, x2), x3)):
                return False
        return True
        # return all(equivalent(op(x1, op(x2, x3)),
        #                       op(op(x1, x2), x3))
        #            for k in range(iterations)
        #            for x1 in [gen()]
        #            for x2 in [gen()]
        #            for x3 in [gen()]
        #            )

    def has_inverses() -> int:
        for k in range(iterations):
            x1 = gen()
            x2 = inverse(x1)
            if x2 is None or not member(x2) or not equivalent(op(x1, x2), identity):
                return False
        return True
        # return all(member(x2) and equivalent(op(x1, x2), identity)
        #            for k in range(iterations)
        #            for x1 in [gen()]
        #            for x2 in [inverse(x1)])

    return member(identity) \
        and is_closed() \
        and is_associative() \
        and has_inverses()


def is_abelian_group(
    member: Callable[[Any], bool],
    op: Callable[[G, G], G],
    identity: G,
    inverse: Callable[[G], G],
    equivalent: Callable[[G, G], bool],
    gen: Callable[[], G],
    iterations: int,
) -> bool:
    """Apply heuristics to determine whether the described set is an Abelian group.
    Args:
        member: a predicate determining whether the given element is in the set
        op: a binary operator which can be called on any element of the set
        identity: a proposed element of the set acting as the identity for the given operation
        inverse: a function which inverts a given element
        equivalent: binary predicate testing equivalence between elements
        gen: a zero-ary function to generate(randomly select) an element of the set.
        iterations: minimum number of checks to make for each group axiom
    Some axioms may remain unchecked (or may be tested fewer than `iterations` number
    of times) if an axiom is found to be violated.
    """

    def is_abelian() -> bool:
        for k in range(iterations):
            x1 = gen()
            x2 = gen()
            if not equivalent(op(x1, x2), op(x2, x1)):
                return False
        return True
        # return all(equivalent(op(x1, x2),
        #                       op(x2, x1))
        #            for k in range(iterations)
        #            for x1 in [gen()]
        #            for x2 in [gen()])

    return is_group(member,
                    op,
                    identity,
                    inverse,
                    equivalent,
                    gen,
                    iterations) \
        and is_abelian()
