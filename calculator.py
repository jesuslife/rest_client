"""
Write funcionalities
"""


def subtract(a: int, b: int) -> int:
    """Subtract two numbers

    Args:
        a (int): First number
        b (int): Second number

    Returns:
        int: Result of the subtraction of a and b
    """
    return a - b


def sum(x: int, y: int) -> int:
    """Sum two numbers

    Args:
        a (int): first number
        b (int): second number

    Returns:
        int: sum of a and b
    """
    if x is not isinstance(a, int) or y is not isinstance(b, int):
        raise ValueError("Both a and b must be integers")
    return x + y
