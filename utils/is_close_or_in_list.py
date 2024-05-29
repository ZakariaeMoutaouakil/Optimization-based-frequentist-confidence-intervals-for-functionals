import math
from typing import List

from algorithm.s_double_star import calculate_s_double_star


def is_close_or_in_list(p_hat: List[float], s_double_star: List[List[float]], margin: float = 0.0) -> bool:
    """
    Check if p_hat is close to any element in s_double_star within a certain margin.

    Args:
    p_hat (List[float]): The vector to check.
    s_double_star (List[List[float]]): The list of vectors to check against.
    margin (float): The allowed margin for closeness. Default is 0.0.

    Returns:
    bool: True if p_hat is close to any element in s_double_star within the margin, False otherwise.
    """
    for s in s_double_star:
        if all(abs(ph - sh) <= margin for ph, sh in zip(p_hat, s)):
            return True
    return False


# Example usage
if __name__ == "__main__":
    p = [0.2, 0.3, 0.5]
    discrete_simplex = [
        [0.1, 0.2, 0.7],
        [0.3, 0.3, 0.4],
        [0.2, 0.3, 0.5]
    ]
    n = 10
    delta = 0.1

    # Precompute factorials from 0! to n!
    factorials = [math.factorial(i) for i in range(n + 1)]

    s_double_star_ = calculate_s_double_star(p, discrete_simplex, n, factorials, delta)
    print("S** set:")
    for p_hat_ in s_double_star_:
        print(p_hat_)

    # Check if a p_hat is close to any element in S**
    p_hat_to_check = [0.2, 0.3, 0.5]
    error_margin = 0.
    result = is_close_or_in_list(p_hat_to_check, s_double_star_, error_margin)
    print(f"Is p_hat {p_hat_to_check} close to any element in S** within a margin of {error_margin}? {result}")
