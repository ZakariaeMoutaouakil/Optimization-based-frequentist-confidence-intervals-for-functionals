from math import prod
from typing import Tuple

from p2.phi_sample import phi_sample


def p_value(q: Tuple[float, ...],
            x: Tuple[int, ...],
            sample_space: Tuple[Tuple[int, ...], ...],
            multinomial_coefficients: Tuple[int, ...]) -> float:
    value = phi_sample(x=x, q=q)
    proba = 0.
    for i in range(len(sample_space)):
        if phi_sample(x=sample_space[i], q=q) >= value:
            proba += multinomial_coefficients[i] * prod(pi ** xi for pi, xi in zip(q, sample_space[i]))
    return proba


if __name__ == "__main__":
    # Example usage
    q1 = (0.2, 0.3, 0.5)
    x1 = (2, 3, 5)
    sample_space = ((2, 3, 5), (1, 4, 5), (3, 2, 5))
    multinomial_coefficients = (10, 20, 30)

    result = p_value(q=q1, x=x1, sample_space=sample_space, multinomial_coefficients=multinomial_coefficients)
    print(f"probability(q={q1}, x={x1}, sample_space={sample_space}, "
          f"multinomial_coefficients={multinomial_coefficients}) = {result}")

    # Another example
    q2 = (0.3, 0.3, 0.4)
    x2 = (3, 3, 4)
    sample_space2 = ((3, 3, 4), (2, 4, 4), (4, 2, 4))
    multinomial_coefficients2 = (15, 25, 35)

    result2 = p_value(q=q2, x=x2, sample_space=sample_space2, multinomial_coefficients=multinomial_coefficients2)
    print(f"probability(q={q2}, x={x2}, sample_space={sample_space2},"
          f" multinomial_coefficients={multinomial_coefficients2}) = {result2}")
