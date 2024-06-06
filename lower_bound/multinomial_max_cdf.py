from typing import List

import numpy as np
from scipy.stats import multinomial

from lower_bound.multinomial_cdf import multinomial_cdf


def multinomial_max_cdf(x: int, n: int, p: List[float]) -> float:
    """
    Compute the cumulative distribution function of the maximum of the multinomial counts.

    Parameters:
    k_max (int): The maximum count to consider.
    n (int): The number of trials.
    p (List[float]): The list of probabilities of the different outcomes.

    Returns:
    float: The CDF value for the given parameters.
    """
    p = np.array(p)
    assert np.isclose(np.sum(p), 1), "Probabilities must sum to 1"

    # Initialize the CDF value
    cdf = 0.0

    # Iterate over all possible combinations of counts such that the maximum count is <= k_max
    for comb in np.ndindex(*(x + 1 for _ in range(len(p)))):
        if np.sum(comb) == n and max(comb) <= x:
            cdf += multinomial.pmf(comb, n, p)

    return cdf


if __name__ == "__main__":
    # Example usage
    k_max = 2  # maximum count to consider
    n_ = 6  # number of trials
    proba = [0.2, 0.5, 0.3]  # probabilities of the different outcomes

    max_cdf_value = multinomial_max_cdf(k_max, n_, proba)
    x_ = [k_max] * len(proba)
    assert max_cdf_value == multinomial_cdf(x_, proba), "CDF values do not match"
    print(f"CDF value of the maximum count: {max_cdf_value}")
