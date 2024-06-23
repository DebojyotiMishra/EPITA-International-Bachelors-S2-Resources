# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from collections import OrderedDict
from functools import reduce  # import needed for python3; builtin in python2
from collections import defaultdict
from typing import TypeVar, Callable, List, Union, Dict, Tuple, Optional, Iterable

T = TypeVar('T')  # Declare type variable
S = TypeVar('S')  # Declare type variable
V = TypeVar('V')  # Declare type variable
L = TypeVar('L')  # Declare type variable


def generate_lazy_val(func: Callable[[], T]) -> Callable[[], T]:
    """Returns a zero-ary function which when called the first time, will evaluate
    the function, func.  However, when called second (third etc.) time will return
    the same value, without re-calling func."""
    saved_value = None
    called = False

    def lazy_holder():
        nonlocal called, saved_value
        if called:
            return saved_value
        else:
            saved_value = func()
            called = True
            return saved_value

    return lazy_holder


def fixed_point(v: T,
                f: Callable[[T], T],
                good_enough: Callable[[T, T], bool],
                invariant: Union[None, Callable[[T], bool]] = None) -> T:
    """Call the given function, `f`, on the given value `v`, and
    again on the return value as long as the input and output values are different.
    *different* is determined by the `good_enough` function, which is something
    like equal or difference-less-than-epsilon.
    If `invariant` is given, it should be a function we can call on the
       input v, and also on the computed result, f(v).
       If the invariant fails to return True, then an exception will be thrown.
    This function may be inefficient if `f` needs to be called a *large* number
    of times, because the function has loop detection.  The list of return
    values of `f` is recorded, and a linear membership check is performed each
    time though the loop.  If a loop is detected, an exception is raised.
    """
    history = []
    if invariant:
        assert invariant(v), f"invariant failed on initial value v={v}"
    while True:
        v2 = f(v)
        if invariant:
            assert invariant(v2), \
                f"invariant failed on computed value\n  starting v={v}\n computed v2={v2}"
        if good_enough(v, v2):
            return v
        if v2 in history:
            for debug_v2 in history:
                print(debug_v2)
            raise AssertionError("Failed: fixedPoint encountered the same value twice:", v2)
        else:
            history.append(v)
            v = v2


def uniquify(seq: List[T]) -> List[T]:
    """remove duplicates from a list, but preserve the order.
    If duplicates occur in the given list, then left-most occurrences
    are removed, so that the right-most occurrence remains.
    E.g., uniquify([1,2,3,2]) --> [1,3,2]"""
    return list(reversed(list(OrderedDict.fromkeys(reversed(seq)))))


def flat_map(f: Callable[[T], List[T]],
             xs: Iterable[T]) -> List[T]:
    """Call `f` on each element of a given list.  The function, `f` will return
    a sequence of zero or more values, these values (if any) are concatenated together
    to form the return list of the call to flat_map."""
    return [y for z in xs for y in f(z)]


def search_replace_splice(xs: Iterable[T],
                          search: T,
                          replace: Iterable[T]) -> List[T]:
    """Search for an element, `search`, in a list `xs`, and if found
    replace with the given sequence of zero or more elements.   If the
    element is found multiple times, then replace each time it occurs.
    This search IS NOT recursive.  I.e., if the element `search` is found
    in the `replace` sequence, this does not trigger another replacement."""

    def select(x):
        if x == search:
            return replace
        else:
            return [x]

    return flat_map(select, xs)


def search_replace(xs: Iterable[T],
                   search: T,
                   replace: T) -> List[T]:
    """Replace the element `search` with `replace` in the given list `xs`,
    every time it occurs."""
    return search_replace_splice(xs, search, [replace])


def remove_element(xs: Iterable[T],
                   search: T) -> List[T]:
    """remove a given element from a list every time it occurs"""
    return search_replace_splice(xs, search, [])


def find_first(pred: Callable[[T], bool],
               xs: Iterable[T],
               default: S = None) -> Union[T, S]:
    """
    find first element of list which makes the predicate true.
    if no such element is found, return the given default or None
    """
    return next(filter(pred, xs), default)


def trace_graph(v0: V,
                edges: Callable[[V], List[Tuple[L, V]]]
                ) -> Tuple[List[V], List[List[Tuple[L, int]]]]:
    # v0 type V
    # edges V => List[(L,V)]
    # if V is te type of vertex
    # and L is the type of label

    current_state_id = 0  # int
    next_available_state = 1  # int
    es = edges(v0)  # List[(L,V)]
    int_to_v = [v0]  # List[V]
    v_to_int = {v0: 0}  # Map[V -> int]
    m = [[]]  # List[List[int]]
    esi = 0  # index into es[...]
    while True:
        if esi == len(es):
            nxt = current_state_id + 1
            if nxt < next_available_state:
                v2 = int_to_v[nxt]
                current_state_id = nxt
                es = edges(v2)
                esi = 0
                m.append([])
                continue
            else:
                return int_to_v, m
        else:
            label, v1 = es[esi]
            if v1 not in v_to_int:
                v_to_int[v1] = next_available_state
                next_available_state += 1
                int_to_v += [v1]
                continue
            else:
                # non-destructively update the list held at m[current_state_id]
                #   by adding a new pair at the end (label,v_to_int[v1])
                m[current_state_id] += [(label, v_to_int[v1])]
                esi += 1
                continue


# this implementation comes directly from stackoverflow
#   https://stackoverflow.com/users/1056941/ronen
# thanks to ronen user:1056941 for the code sample
def group_by(key: Callable[[T], S],
             seq: Iterable[T]) -> Dict[S, List[T]]:
    return reduce(lambda grp, val: grp[key(val)].append(val) or grp, seq, defaultdict(list))


def group_map(key: Callable[[T], S],
              seq: Iterable[T],
              store: Callable[[T], V]
              ) -> Dict[S, List[V]]:
    """
    Build a Dict which maps keys to value.
    For each element of the input sequence, we call the key function on
      the element.  That gives us the key for the dictionary.
      The value is a list of values, one for each element of the input sequence
      for which key returns that key.  The values in the list are not necessarily
      the value from the sequence, but return value of the store function.
     E.g., to mtransform [(1,"a"), (2, "b"), (1, "c"), (3, "d")]
       to { 1: [(1,"a"), (1, "c")],
            2: [(2, "b")],
            3: [(3, "d")]}
     use group_by, group_by(lambda x: x[0],
                            sequence)

     but to mtransform [(1,"a"), (2, "b"), (1, "c"), (3, "d")]
      to { 1: ["a" "c"],
           2: ["b"],
           3: ["d"]}
    use group_map(lambda x: x[0],
                  sequence,
                  lambda x: x[1])
    """
    grouped = {}
    for q in seq:
        k = key(q)
        if k in grouped:
            grouped[k].append(store(q))
        else:
            grouped[k] = [store(q)]
    return grouped


def make_counter(init: int = 0, delta: int = 1) -> Callable[[], int]:
    """Return a zero-ary function which will *count*.  I.e., when
    the zero-ary function is called the first time, will return `init`;
    when called the second time, will return `init + delta`,
    when called the third time, will return `init + 2*delta`, etc.
    Args:
        init: int, default=0
        delta: int, the difference between successive values
    """
    c = init - delta

    def count() -> int:
        nonlocal c
        c += delta
        return c

    return count


def randomize_int(lower=-100, upper=100) -> Callable[[], int]:
    """returns a function of zero arguments, which when called
    will return an int between lower and upper inclusive
    """
    import random
    assert isinstance(lower, int)
    assert isinstance(upper, int)
    return lambda: random.randint(lower, upper)


def randomize_float(lower=-100.0, upper=100.0) -> Callable[[], float]:
    """returns a function of zero arguments; which when called
    will return a float between lower and upper inclusive
    """
    import random
    assert isinstance(lower, float)
    assert isinstance(upper, float)
    return lambda: random.uniform(lower, upper)


def interpolate_curve(lower: float,
                      upper: float,
                      min_dt: float,
                      max_dt: float,
                      max_dx: float,
                      f: Callable[[float], Tuple[float, ...]]) -> List[Tuple[float, ...]]:
    """
    Returns an iterable of tuples, each a return value of f,
    called at some float between lower, and upper inclusive.
    These tuples designate a curve, parameterized by t,
    where delta-t (difference between successive values of t)
    are no further apart than max_dt, and no closer than min_dt,
    but otherwise sufficiently close so that the euclidian distance
    between successive tuples is < max_dx.
    """
    assert abs(upper - lower) > min_dt

    def sqr(x):
        return x * x

    max_dist_sq = sqr(max_dx)

    def dist_sq(p1: Tuple[float, ...], p2: Tuple[float, ...]) -> float:
        return sum(sqr(p1[k] - p2[k]) for k in range(len(p1)))

    def finer(fa: Tuple[float, ...], left: float, right: float) -> List[Tuple[float, ...]]:
        if abs(right - left) < min_dt:
            return [fa]
        mid = left + (right - left) / 2.0
        if abs(right - left) > max_dt:
            return finer(fa, left, mid) + finer(f(mid), mid, right)
        if dist_sq(fa, f(right)) < max_dist_sq:
            return [fa]
        else:
            return finer(fa, left, mid) + finer(f(mid), mid, right)

    return finer(f(lower), lower, upper) + [f(upper)]


def interpolate(lower: float,
                upper: float,
                min_dx: float,
                max_dx: float,
                max_dy: float,
                f: Callable[[float], float]) -> List[Tuple[float, float]]:
    """Return a list of (x,y) pairs, where y=f(x).
    Successive x values are perhaps unevenly spaced so as to satisfy mindx, max_dx, and
    mindy.   Successive x values are at least mindx apart, but no less than max_dx apart.
    Successive x values are close enough to assure that the corresponding y values
    differ by no more than max_dy.
    The idea is that the function keeps refining the x values until the corresponding
    y values are within epsilon=max_dy of each other.  However, this may not be possible
    in some cases where the function is either discontinuous, or has a very high
    derivative, thus mindx is also respected to avoid infinite (or very deep) recursion.
    """
    from math import sqrt
    return interpolate_curve(lower=lower,
                             upper=upper,
                             min_dt=min_dx,
                             max_dt=max_dx,
                             max_dx=sqrt(max_dy * max_dy + max_dx * max_dx),
                             f=lambda t: (t, f(t)))


def plot_xys(xys: List[Tuple[float, float]], scatter: bool = False):
    """
    Make a line plot (or scatter plot if scatter=True), of the data
    presented in the given list of xy-pairs.
    """
    # this solution comes from https://stackoverflow.com/a/44062487
    # thanks to https://stackoverflow.com/users/2631559/zweedeend
    import numpy as np
    from matplotlib import pyplot as plt

    data = np.array(xys)
    x, y = data.T
    plt.figure(figsize=(7.0, 7.0))  # height,width in inches

    if scatter:
        plt.scatter(x, y, s=1)
    else:
        plt.plot(x, y)
    plt.show()


def float_range(start, stop, step):
    """Generate a range of floating point numbers.
    Code copied from:
    https://stackoverflow.com/questions/477486/how-do-i-use-a-decimal-step-value-for-range
    Thanks: https://stackoverflow.com/users/6491/gimel"""
    r = start
    while r < stop:
        yield r
        r += step


def argmax(f: Callable[[T], S], data: List[T]) -> T:
    """Apply the given function to every element of `data`.
    `f` is expected to return a number-like value for which v1 > v2 is defined.
    The argmax function returns the element of data for which `f` returns
    the maximum value in the sense that v1 > v2.
    It is blindly supposed that data has at least one element.
    """
    if not data:
        return None
    v, d = (f(data[0]), data[0])
    for d2 in data[1:]:
        v2 = f(d2)
        if v2 > v:
            v, d = (v2, d2)
    return d


def argmin(f: Callable[[T], S], data: List[T]) -> T:
    """Apply the given function to every element of `data`.
    `f` is expected to return a number-like value for which v1 > v2 is defined.
    The argmax function returns the element of data for which `f` returns
    the maximum value in the sense that v1 > v2.
    It is blindly supposed that data has at least one element.
    """
    return argmax(lambda x: -f(x), data)


def trace(func):
    """Declaration of annotation.
    @trace can be placed before a function (global, local, or method) definition
    to cause diagnostic information to be printed when the function is called,
    and when the function returns.
    """

    def wrapper(*args, **kwargs):
        print(f"> {func.__name__} with {args} {kwargs}")
        val = func(*args, **kwargs)
        print(f"< {func.__name__} returns {val}")
        return val

    return wrapper


def fast_power(base: T,
               mult: Callable[[T, T], T],
               p: int,
               identity: Optional[T] = None):
    """Raise the given `base` to the p'th power using approximately
    log p multiplications.
    Args:
        base: the value to be raised to the given power
        mult: binary function to multiply two values together
        p: an integer >= 0
        identity:  is only used if p==0, in which case identity is returned.
                   identity defaults to None.
    """
    assert isinstance(p, int)
    assert p >= 0

    if p == 0:
        return identity
    elif p == 1:
        return base
    elif p % 2 == 0:  # if p is even
        tmp = fast_power(base, mult, p // 2, None)
        return mult(tmp, tmp)
    else:  # if p is odd
        tmp = fast_power(base, mult, p - 1, None)
        return mult(base, tmp)


def pip_install(package):
    """running pip install from the shell will install libraries according to the
    unix environment, which might be different than the particular python
    being used.   using something like pip_install('typing_extensions') from
    the python console seems to install the *correct* place, so it can
    be referenced by the python being run.
    """
    import pip

    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])


def shuffle(seq):
    """return a shuffled copy of the given list"""
    import random
    seq = list(seq[:])
    random.shuffle(seq)
    return seq
