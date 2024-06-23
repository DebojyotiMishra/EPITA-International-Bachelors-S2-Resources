from common.utils import trace, randomize_float
from structure.Field import is_field
from structure.Group import is_abelian_group
from matrix.Vector import Vector
from matrix.SqMatrix import SqMatrix
from typing import TypeVar, Callable, Any, Optional, List

V = TypeVar("V")
K = TypeVar("K")


def is_vector_space(
    v_member: Callable[[Any], bool],
    s_member: Callable[[Any], bool],
    v_identity: V,
    s_add_ident: K,
    s_mult_ident: K,
    v_inverse: Callable[[V], Optional[V]],
    s_add_inverse: Callable[[K], Optional[K]],
    s_mult_inverse: Callable[[K], Optional[K]],
    v_gen: Callable[[], V],
    s_gen: Callable[[], K],
    iterations: int,
    vv_add: Callable[[V, V], V] = lambda u, v: u + v,
    ss_add: Callable[[K, K], K] = lambda s, t: s + t,
    ss_mult: Callable[[K, K], K] = lambda s, t: s * t,
    sv_mult: Callable[[K, V], V] = lambda s, v: v * s,
    v_equivalent: Callable[[V, V], bool] = lambda u, v: u == v,
    s_equivalent: Callable[[K, K], bool] = lambda s, t: s == t,
) -> bool:
    """Apply heuristics to determine whether the described set is a vector space.
    This check is done by testing every vector space axiom a minimum of `iterations`
    number of times in attempt to falsify one of them.
    Some axioms may remain unchecked (or may be tested fewer than `iterations` number
    of times) if an axiom is found to be violated.
    Args:
        v_member: predicate determining whether the given object is a vector
        s_member: predicate determining whether the given object is a scalar
        v_identity: the proposed vector additive identity
        s_add_ident: the proposed scalar additive identity
        s_mult_ident: the proposed scalar multiplicative identity
        v_inverse: function returning the additive inverse of a given vector
        s_add_inverse: function returning the additive inverse of a given scalar
        s_mult_inverse: function returning the multiplicative inverse of a scalar
        v_gen: zero-ary function returning a randomly generated vector
        s_gen: zero-ary function returning a randomly generated scalar
        iterations: minimum number of times each axiom is checked
        vv_add: function to add two vectors
        ss_add: function to add two scalars
        ss_mult: function to multiply to scalars
        sv_mult: function to multiply a scalar and a vector (in that order)
        v_equivalent: predicate to determine equivalence of two vectors
        s_equivalent: predicate to determine equivalence of two scalars
    """

    def is_closed_scalar_mult():
        return all(
            v_member(sv_mult(s, v))
            for _k in range(iterations)
            for v in [v_gen()]
            for s in [s_gen()]
        )

    def is_scale_ident():
        return all(
            v_equivalent(v, sv_mult(s_mult_ident, v))
            for _k in range(iterations)
            for v in [v_gen()]
        )

    def is_zero_vector():
        return all(v_equivalent(v_identity, v_gen()) for _ in range(iterations))

    def is_add_inv():
        return all(v_equivalent(v_identity, vv_add(v_gen(), v_inverse(v_gen()))))

    def is_distributive_1():
        return all(
            v_equivalent(
                sv_mult(s, vv_add(v1, v2)), vv_add(sv_mult(s, v1), sv_mult(s, v2))
            )
            for _k in range(iterations)
            for s in [s_gen()]
            for v1 in [v_gen()]
            for v2 in [v_gen()]
        )

    def is_distributive_2():
        return all(
            v_equivalent(
                sv_mult(ss_add(s1, s2), v), vv_add(sv_mult(s1, v), sv_mult(s2, v))
            )
            for _k in range(iterations)
            for s1 in [s_gen()]
            for s2 in [s_gen()]
            for v in [v_gen()]
        )

    def is_associative():
        return all(
            v_equivalent(sv_mult(ss_mult(s1, s2), v), sv_mult(s1, sv_mult(s2, v)))
            for _k in range(iterations)
            for s1 in [s_gen()]
            for s2 in [s_gen()]
            for v in [v_gen()]
        )

    return (
        is_field(
            member=s_member,
            add=ss_add,
            mult=ss_mult,
            zero=s_add_ident,
            one=s_mult_ident,
            additive_inverse=s_add_inverse,
            multiplicative_inverse=s_mult_inverse,
            equivalent=s_equivalent,
            gen=s_gen,
            iterations=iterations,
        )
        and is_abelian_group(
            member=v_member,
            op=vv_add,
            identity=v_identity,
            inverse=v_inverse,
            equivalent=v_equivalent,
            gen=v_gen,
            iterations=iterations,
        )
        and is_closed_scalar_mult()
        and is_scale_ident()
        and is_distributive_1()
        and is_distributive_2()
        and is_associative()
    )


def is_inner_product(
    inner_product: Callable[[V, V], float],
    add: Callable[[V, V], V],
    scale: Callable[[float, V], V],
    gen: Callable[[], V],
    iterations: int,
    epsilon: float = 0.001,
) -> bool:
    """Apply heuristics to determine whether the given function, inner_product,
    satisfies the axioms of an inner product for a vector space.
    This function assumes that the scalar field is the set of floats,
    thus the caller cannot specify a generator for scalars.
    Args:
        inner_product:  binary function, the supposed inner product to test
        add: binary function to add two vectors
        scale: binary function to multiply a scalar (on the left) by a vector
                (on the right)
        gen: zero-ary function to generate a vector (randomly)
        iterations: number of times (minimum) to test each axiom until a failure
                is found.
        epsilon: x==0.0 should be considered abs(x)<epsilon"""

    def is_symmetric() -> bool:
        for _ in range(iterations):
            v = gen()
            u = gen()
            if abs(inner_product(u, v) - inner_product(v, u)) > epsilon:
                return False
        return True

    def is_positive() -> bool:
        return all(inner_product(u, u) > 0 for _k in range(iterations) for u in [gen()])

    def is_definite() -> bool:
        zero = scale(0.0, gen())
        return inner_product(zero, zero) == 0.0

    def is_bilinear() -> bool:
        gen_float = randomize_float(-100.0, 100.0)

        for _ in range(iterations):
            alpha = gen_float()
            beta = gen_float()
            u = gen()
            v = gen()
            w = gen()
            ip1 = inner_product(add(scale(alpha, u), scale(beta, v)), w)
            ip2 = alpha * inner_product(u, w) + beta * inner_product(v, w)
            if abs(ip1 - ip2) > epsilon:
                return False
        return True

    return is_symmetric() and is_positive() and is_definite() and is_bilinear()


def is_norm(
    norm: Callable[[V], float],
    add: Callable[[V, V], V],
    scale: Callable[[float, V], V],
    zero: V,
    gen: Callable[[], V],
    iterations: int,
) -> bool:
    """This function tests whether the given function, norm, obeys the
    axioms that a real-valued norm should obey.  Note, that this does
    not work for an arbitrary vector space, with an arbitrary field, K.
    We are restricting K specifically to float, to simulate real
    vector spaces."""

    def is_positive() -> bool:
        return all(
            (norm(v) > 0) if v != zero else norm(v) == 0
            for _k in range(iterations)
            for v in [gen()]
        )

    def is_definite() -> bool:
        return norm(zero) == 0

    def is_scalable() -> bool:
        gen_float = randomize_float(-100.0, 100.0)
        epsilon = 0.0001
        return all(
            ns == an or abs(ns - an) < epsilon
            for _k in range(iterations)
            for v in [gen()]
            for s in [gen_float()]
            for ns in [norm(scale(s, v))]
            for an in [abs(s) * norm(v)]
        )

    def triangle_inequality_holds() -> bool:
        epsilon = 0.001

        def tri(a, b, c):
            return a <= b + c or a - (b + c) < epsilon

        return all(
            tri(norm(add(u, v)), norm(u), norm(v))
            for _k in range(iterations)
            for u in [gen()]
            for v in [gen()]
        )

    return (
        is_positive()
        and is_definite()
        and is_scalable()
        and triangle_inequality_holds()
    )


def gram_schmidt(vectors: List[Vector]) -> List[Vector]:
    """Given `vectors` which is a list of n Vectors each of dimension n,
    i.e., whatever the dimension of an element of vectors is, then we have
    that many vectors.   e.g, if len(vectors)=3, then each element of vectors
    has v.dim == 3.
    This function, gram_schmidt, performs the Gram-Schmidt process to generate
    a set of n orthogonal unit vectors.  The first vector in the returned
    list is a unit vector in the direction of vectors[0].   The second
    vector in the returned list is formed by starting with vectors[1],
    and subtracting from it the projection of the previous vector
    computed.   For the k'th (0 indexed) vector computed, we start with
    vectors[k] and subtract off the projections of each vector computed so
    far.   Finally, we have a list of vectors which might not be normalized,
    so we normalize them."""
    dim = len(vectors)

    assert all(v.dim == dim for v in vectors)
    assert all(isinstance(v, Vector) for v in vectors)

    def proj(u, v):
        return u.scale(u.inner_product(v) / u.inner_product(u))

    u = [vectors[0]] * dim
    for n in range(1, dim):
        u[n] = vectors[n] - sum(
            (proj(u[k], vectors[n]) for k in range(n)), Vector.zero(dim)
        )
    return [u[k].scale(1 / u[k].norm()) for k in range(dim)]


def find_coordinates(v: Vector, basis: List[Vector]) -> Optional[Vector]:
    """find the coordinates of Vector b in the given basis.
    return None if this is impossible."""
    assert v.dim == len(basis)
    assert all(b.dim == v.dim for b in basis)

    assert v.dim == len(basis)
    assert all(b.dim == v.dim for b in basis)

    m, det = SqMatrix([b.content for b in basis]).transpose().gauss_jordan_inverse()
    if det == 0:
        return None
    return m * v


def change_coordinates(
    c1: Vector, basis1: List[Vector], basis2: List[Vector]
) -> Optional[Vector]:
    """Given a Vector, c1, a coordinate vector with respect to basis1, compute and return
    its coordinate vector with respect to basis 2.   Return None if this is impossible.
    """
    assert c1.dim == len(basis1)
    assert c1.dim == len(basis2)
    assert all(b.dim == c1.dim for basis in [basis1, basis2] for b in basis)

    m1 = SqMatrix([b.content for b in basis1]).transpose()
    m2 = SqMatrix([b.content for b in basis2]).transpose()
    inv2, det2 = m2.gauss_jordan_inverse()
    if det2 == 0:
        return None
    return inv2 * (m1 * c1)
