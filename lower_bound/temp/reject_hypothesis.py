from time import time
from typing import List

from lower_bound.generate_list import generate_list
from lower_bound.multinomial_max_cdf_inverse import multinomial_max_cdf_inverse


def reject_hypothesis(x: List[int], q: float, alpha: float) -> bool:
    """
    Reject the null hypothesis if the p-value is less than the threshold.

    Parameters:
    x (List[int]): The list of observed frequencies.
    q (float): The expected probability for the first category.
    alpha (float): The significance level for rejecting the null hypothesis.

    Returns:
    bool: True if the null hypothesis is rejected, False otherwise.
    """
    m = len(x)
    n = sum(x)
    p = generate_list(m=m, q=q)
    quantile = multinomial_max_cdf_inverse(prob=alpha, n=n, p=p)
    # print(f"Quantile: {quantile}")
    return max(x) < quantile


if __name__ == "__main__":
    # Example usage
    observed_counts = [8, 2, 0, 0, 0]  # observed frequencies
    max_freq = max(observed_counts) / sum(observed_counts)
    print("Maximum observed frequency:", max_freq)
    q_ = 0.8  # expected probability for the first category
    alpha_ = 0.2  # significance level

    start_time = time()  # Start time
    result = reject_hypothesis(observed_counts, q_, alpha_)
    end_time = time()  # End time
    print(f"Null hypothesis: {max_freq} > {q_}")
    print(f"Reject the null hypothesis: {result}")
    print(f"Time taken: {end_time - start_time:.6f} seconds")
