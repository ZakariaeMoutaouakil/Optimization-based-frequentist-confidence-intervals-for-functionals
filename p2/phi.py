from typing import Tuple, List

from numpy import isclose


def phi(p: Tuple[float, ...], q: Tuple[float, ...]) -> float:
    assert len(p) == len(q), "p and q must have the same length"
    assert isclose(sum(p), sum(q)), "p and q must have the same sum"
    x = sorted(p, reverse=True)
    y = sorted(q, reverse=True)
    m = len(p)
    max_values: List[float] = []
    for i in range(1, m):
        max_values.append(sum(x[:i]) - sum(y[:i]))
    max_value = max(max_values)
    return max_value


if __name__ == "__main__":
    # Example usage
    a = (0.1, 0.2, 0.3, 0.4)
    b = (0.5, 0.2, 0.2, 0.1)
    result = phi(a, b)
    print(result)

    # Another example
    c = (0.3, 0.3, 0.2, 0.2)
    d = (0.4, 0.4, 0.1, 0.1)
    result2 = phi(c, d)
    print(result2)  # This should also print a value greater than 0
