def compute_expression(x):
    """
    >>> compute_expression(1)
    5
    >>> compute_expression(2)
    32
    >>> compute_expression(3)
    145
    >>> compute_expression(0)
    1
    """
    return x**4 + 4**x

if __name__ == "__main__":
    import doctest
    doctest.testmod()
