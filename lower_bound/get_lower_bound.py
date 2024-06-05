from time import time
from typing import List

from lower_bound.find_threshold import find_threshold
from lower_bound.reject_hypothesis import reject_hypothesis


def get_lower_bound(x: List[int], alpha: float) -> float:
    reject = lambda q: reject_hypothesis(x=x, q=q, alpha=alpha)
    return find_threshold(reject)


if __name__ == "__main__":
    # Example usage
    observed_counts = [3, 2, 4, 1, 0]  # observed frequencies
    alpha_ = 0.05  # significance level
    start_time = time()  # Start time
    bound = get_lower_bound(observed_counts, alpha_)
    end_time = time()  # End time
    print("Maximum observed frequency:", max(observed_counts) / sum(observed_counts))
    print(f"Lower bound: {bound}")
    print(f"Time taken: {end_time - start_time:.6f} seconds")
