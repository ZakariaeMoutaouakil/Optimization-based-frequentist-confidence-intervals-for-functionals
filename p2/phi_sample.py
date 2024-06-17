from typing import Tuple

from p2.phi import phi


def phi_sample(x: Tuple[int, ...], q: Tuple[float, ...]) -> float:
    assert len(x) == len(q), "x and q must have the same length"
    n = sum(x)
    a = tuple(xi / n for xi in x)
    return phi(p=q, q=a)


if __name__ == "__main__":
    # Example usage
    x1 = (1, 2, 3, 4)
    q1 = (0.25, 0.25, 0.25, 0.25)
    result = phi_sample(x1, q1)
    print(f"phi_sample({x1}, {q1}) = {result}")

    # Another example
    x2 = (5, 15, 10, 20)
    q2 = (0.3, 0.4, 0.2, 0.1)
    result2 = phi_sample(x2, q2)
    print(f"phi_sample({x2}, {q2}) = {result2}")
