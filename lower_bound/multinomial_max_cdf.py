from time import time
from typing import Tuple

from numpy import array, sum, isclose
from scipy.stats import multinomial

from lower_bound.generate_multiple_indices import generate_multiple_indices
from lower_bound.multinomial_cdf import multinomial_cdf


def multinomial_max_cdf(x: int, n: int, p: Tuple[float, ...], indices: Tuple[Tuple[Tuple[int, ...], ...], ...]) \
        -> float:
    """
    Compute the cumulative distribution function of the maximum of the multinomial counts.

    Parameters:
    k_max (int): The maximum count to consider.
    n (int): The number of trials.
    p (List[float]): The list of probabilities of the different outcomes.

    Returns:
    float: The CDF value for the given parameters.
    """
    p = array(p)
    assert isclose(sum(p), 1), "Probabilities must sum to 1"
    # assert n > 0, "Number of trials must be positive"

    # Initialize the CDF value
    cdf = 0.
    if x >= n:
        return 1.
    elif x <= 0:
        return 0.
    else:
        # Iterate over all possible combinations of counts such that the maximum count is <= k_max
        for comb in indices[x]:
            # print(comb)
            cdf += multinomial.pmf(comb, n, p)
            # print(cdf, comb, n, p)

    return cdf


if __name__ == "__main__":
    # Example usage
    k_max = 2  # maximum count to consider
    n_ = 6  # number of trials
    proba = (0.2, 0.5, 0.3)  # probabilities of the different outcomes
    indices_ = generate_multiple_indices(k_max, len(proba), n_)

    start_time = time()
    max_cdf_value = multinomial_max_cdf(k_max, n_, proba, indices_)
    end_time = time()
    x_ = [k_max] * len(proba)
    assert max_cdf_value == multinomial_cdf(x_, proba), "CDF values do not match"
    print(f"CDF value of the maximum count: {max_cdf_value}")
    print(f"Time taken: {end_time - start_time:.6f} seconds")
