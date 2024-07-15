'''
Description: A module that contains a function to calculate the Fibonacci number.
'''

from functools import wraps


def caching_fibonacci(func: callable) -> callable:
    """
    Decorator to cache the results of the Fibonacci function.

    Parameters:
    - func (callable): The Fibonacci function.

    Returns:
    - callable: The wrapper function.
    """
    cache = {}
    @wraps(func)
    def wrapper(n: int) -> int:
        return cache.get(n, False) or cache.setdefault(n, func(n))
    return wrapper

@caching_fibonacci
def fibonacci(n: int) -> int:
    """
    Calculate the Fibonacci number.

    Parameters:
    - n (int): The index of the Fibonacci number to calculate.

    Returns:
    - int: The Fibonacci number.
    """
    if isinstance(n, int):
        if n < 2:
            return max(n, 0)
        return fibonacci(n - 1) + fibonacci(n - 2)
