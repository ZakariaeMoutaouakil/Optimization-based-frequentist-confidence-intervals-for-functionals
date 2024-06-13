from typing import List, Tuple

import numpy as np
from scipy.stats import multinomial


def multinomial_cdf(x: List[int], p: Tuple[float, ...]) -> float:
    """
    Compute the cumulative distribution function of the multinomial distribution.

    Parameters:
    k (List[int]): The list of observed frequencies.
    n (int): The number of trials.
    p (List[float]): The list of probabilities of the different outcomes.

    Returns:
    float: The CDF value for the given parameters.
    """
    x = np.array(x)
    n = sum(x)
    p = np.array(p)
    # Ensure that the probabilities sum correctly
    assert np.isclose(np.sum(p), 1), "Probabilities must sum to 1"

    # Calculate the probability mass function (PMF) for all combinations up to k
    cdf = 0.0
    for comb in np.ndindex(tuple(x + 1)):
        if np.sum(comb) == n:
            cdf += multinomial.pmf(comb, n, p)
    return cdf


if __name__ == "__main__":
    # Example usage
    k = [1, 1, 0]  # observed frequencies
    proba = (0.2, 0.5, 0.3)  # probabilities of the different outcomes

    cdf_value = multinomial_cdf(k, proba)
    print(f"CDF value: {cdf_value}")
