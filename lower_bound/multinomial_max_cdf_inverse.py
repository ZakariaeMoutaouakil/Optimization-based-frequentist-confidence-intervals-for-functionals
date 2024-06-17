from typing import Tuple

from lower_bound.generate_multiple_indices import generate_multiple_indices
from lower_bound.multinomial_max_cdf import multinomial_max_cdf


def multinomial_max_cdf_inverse(prob: float,
                                n: int,
                                p: Tuple[float, ...],
                                indices: Tuple[Tuple[Tuple[int, ...]], ...]) -> int:
    """
    Compute the inverse cumulative distribution function (quantile function) of the maximum of the multinomial counts.

    Parameters:
    prob (float): The probability threshold for the CDF.
    n (int): The number of trials.
    p (List[float]): The list of probabilities of the different outcomes.

    Returns:
    int: The maximum count value such that the CDF is equal to or exceeds the given probability.
    """
    # Ensure the probability is within valid range
    assert 0 <= prob <= 1, "Probability must be between 0 and 1"

    # Initialize k_max
    k_max = 0

    # Iterate until the CDF meets or exceeds the desired probability
    while True:
        cdf_value = multinomial_max_cdf(k_max, n, p, indices)
        if cdf_value >= prob:
            break
        k_max += 1

    return k_max


if __name__ == "__main__":
    # Example usage and assertions
    proba = 0.95  # probability threshold
    n_ = 4  # number of trials
    p_ = (0.2, 0.5, 0.3)  # probabilities of the different outcomes
    indices_ = generate_multiple_indices(n_, len(p_))

    k_max_value = multinomial_max_cdf_inverse(proba, n_, p_, indices_)
    print(f"Inverse CDF value (quantile) for probability {proba}: {k_max_value}")

    # Assertions to verify the correctness
    assert multinomial_max_cdf(k_max_value - 1, n_,
                               p_, indices_) < proba, "CDF value should be less than the probability for k_max - 1"
    assert multinomial_max_cdf(k_max_value, n_,
                               p_,
                               indices_) >= proba, \
        "CDF value should be greater than or equal to the probability for k_max"

    # Additional test cases
    proba_test = 0.5
    n_test = 5
    p_test = (0.1, 0.2, 0.3, 0.4)
    indices_ = generate_multiple_indices(n_, len(p_test))

    k_max_test_value = multinomial_max_cdf_inverse(proba_test, n_test, p_test, indices_)
    print(f"Inverse CDF value (quantile) for probability {proba_test}: {k_max_test_value}")

    assert multinomial_max_cdf(k_max_test_value - 1, n_test,
                               p_test,
                               indices_) < proba_test, "CDF value should be less than the probability for k_max - 1"
    assert multinomial_max_cdf(k_max_test_value, n_test,
                               p_test, indices_) >= proba_test, (
        "CDF value should be greater than or equal to the probability "
        "for k_max")
