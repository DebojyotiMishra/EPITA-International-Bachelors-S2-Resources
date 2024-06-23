from common.utils import randomize_int
from typing import List


class Vector:
    def __init__(self, content):
        """
        self.dim is an integer indicating the dimension of the vector.  e.g.
            a 2-tuple has self.dim=2, a 3-tuple has self.dim=3
        self.content is a tuple containing dim-many numbers indicating
            the components of the vector
        """
        self.dim = len(content)
        self.content = tuple(content)

    def __repr__(self):
        """creates and returns a string giving a human-readable representation
        of the vector.  e.g., 'Vector[4]((3, 5, 2, -1))'
        """
        return f"Vector[{self.dim}]({self.content})"

    def __eq__(self, other):
        """Test whether the two objects are type compatible, (other is type Vector),
        and whether the content is equal using ==.
        """
        if not isinstance(other, Vector):
            return False
        return other.content == self.content

    def __getitem__(self, items):
        """Allow a Vector instance to be accessed like an array."""
        return self.content[items]

    @staticmethod
    def tabulate(dim, f):
        """Create and return a new Vector of dimension dim.
        Each of the components of the Vector is determined by a call
        to the given function with the index as argument.
        For example the k'th element is initialized with a call to f(k).
        E.g., Vector.tabulate(3, f) is equivalent to
              Vector(tuple(f(0), f(1), f(2)))
        """
        return Vector([f(k) for k in range(dim)])

    @staticmethod
    def random(dim, randomizer=randomize_int(-100, 100)):
        """Create and return a Vector having randomly selected
        elements for its components. The randomizer argument
        specifies a zero-ary argument which will return a
        random number.  If the call-site would like to fill
        the 5d Vector with random numbers between 0.5 and 1.5,
        use Vector.random(5,randomize_float(0.5, 1.5))
        """
        assert dim >= 1
        return Vector.tabulate(dim, lambda k: randomizer())

    @staticmethod
    def zero(dim):
        """Create a return a Vector of the given dimension consisting entirely
        of 0 (the integer 0)"""
        return Vector.tabulate(dim, lambda k: 0)

    def __add__(self, other):
        """create and return a new Vector which is the sum (addition) of the
        two given vectors, self and other. raise an error if the dimensions
        are not compatible to add."""
        assert isinstance(other, Vector)
        assert (
            self.dim == other.dim
        ), f"cannot add Vectors of different dimension: {self}, {other}"
        return Vector.tabulate(self.dim, lambda k: self[k] + other[k])
        # Prof solution 1: return Vector(self[i] + other[i] for i in range(self.dim))

    def scale(self, scalar):
        """create and return a new Vector, the same dimension as self, but with
        each component having been multiplied by the given scalar.
        If scalar fails to be a number, then a RuntimeError is raised."""
        import numbers

        if not isinstance(scalar, numbers.Number):
            raise RuntimeError(f"expecting number, got {type(scalar)}: {scalar}")
        return Vector.tabulate(self.dim, lambda k: self[k] * scalar)

    def __mul__(self, other):
        """Override the * operator to perform scalar multiplication.
        Note that we support Vector * scalar, but not scalar * Vector,
        as we do not attempt to override the __mul__ method on numbers."""
        return self.scale(other)

    def __sub__(self, other):
        """Return the subtraction (difference) of the given Vectors: self - other.
        This method also overrides the - operator to perform the subtraction."""
        return self + other.scale(-1)

    def norm(self):
        """Return the Euclidian length of the Vector"""
        import math

        return math.sqrt(sum(x**2 for x in self.content))

    def normalize(self):
        """If the norm of the vector is 0, then return None,
        otherwise return a unit vector parallel to the vector.
        I.e., scale the vector by 1.0/the-norm-of-the-vector"""
        return self.scale(1 / self.norm()) if self.norm() != 0 else None

    def distance(self, other):
        """Return the Euclidian distance between the two vectors."""
        assert other.dim == self.dim
        return (self - other).norm()

    def inner_product(self, other):
        """Return a number indicating the dot product of the two vectors,
        i.e., the sum of the products of the corresponding components.
        Raise an error of the Vector dimensions are not compatible"""
        assert other.dim == self.dim
        return sum(self[i] * other[i] for i in range(self.dim))

    def angle(self, other):
        """Return the angle (in radians) between the two Vectors.
        This angle is the same if measured from self to other or from
        other to self.  I.e., the angle is positive,
        between 0 and pi, inclusive."""
        assert other.dim == self.dim
        import math

        tmp = abs(self.inner_product(other)) / (self.norm() * other.norm())
        if -1 <= tmp <= 1:
            return math.acos(tmp)
        elif tmp > 1:
            return math.acos(1)
        else:
            return math.acos(-1)


def is_orthogonal(vectors: List[Vector]) -> bool:
    """Is the given list of Vectors pairwise orthogonal according to its
    inner product"""
    epsilon = 0.0001
    if len(vectors) < 2:
        return True
    elif vectors[0].dim != vectors[1].dim:
        return False
    else:
        return all(
            abs(vectors[i].inner_product(vectors[j])) < epsilon
            for i in range(len(vectors))
            for j in range(i + 1, len(vectors))
            if len(vectors) >= 2 and vectors[0].dim == vectors[1].dim
        )
