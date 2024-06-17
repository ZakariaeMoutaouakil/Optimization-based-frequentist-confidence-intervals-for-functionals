from typing import Tuple


def comparator_formula(p1: float, q: float, m: int) -> Tuple[float, ...]:
    assert p1 + q <= 1, "p1 + q must be less than or equal to 1"
    assert m > 2, "m must be greater than 2"
    return (p1,) + (q,) + ((1 - p1 - q) / (m - 2),) * (m - 2)


if __name__ == "__main__":
    # Example usage:
    p1 = 0.9
    q = 0.1
    m = 3

    result = comparator_formula(p1, q, m)
    print(result)
    print(sum(result))
