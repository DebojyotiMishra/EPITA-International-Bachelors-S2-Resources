from typing import TypeVar, Callable, List


def hello(name: str) -> str:
    """Return a string which prepends 'Hello, ', including a comma
    and a space before the given name, and appends a period at the end.
    E.g., hello('gertrude') returns 'Hello, gertrude.'
    """
    return f"Hello, {name}."
