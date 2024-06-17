from math import sqrt
from typing import Tuple


def solve_quadratic(m: int) -> Tuple[float, float]:
    if m == 1:
        raise ValueError("m cannot be 1 because it would result in division by zero")

    a = 1
    b = -1
    c = 1 / (m - 1)

    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        raise ValueError("The equation has no real roots because the discriminant is negative.")

    root1 = (-b - sqrt(discriminant)) / (2 * a)
    root2 = (-b + sqrt(discriminant)) / (2 * a)

    return root1, root2


if __name__ == "__main__":
    # Example usage:
    m_ = 5
    print(solve_quadratic(m_))

    m_ = 6
    print(solve_quadratic(m_))
