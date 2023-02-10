"""Module for utility functions."""

from time import time
from typing import Any, Callable


def timer_decorator(func: Callable) -> Callable:
    """Decorator that prints the time it took to execute a function."""

    def wrapper_function(*args, **kwargs) -> Any:
        """Wrapper function that prints the time it took to execute a function.

        Returns:
            Any: the result of the function
        """
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(
            f"Method {func.__name__!r} of module {func.__module__!r} executed in {t2 - t1:.4f} seconds."
        )
        return result

    return wrapper_function
