from time import time
from typing import List, Callable

from lower_bound.find_threshold import find_threshold
from lower_bound.reject_hypothesis import reject_hypothesis


def get_lower_bound(x: List[int], alpha: float) -> float:
    reject: Callable[[float], bool] = lambda q: reject_hypothesis(x=x, q=q, alpha=alpha)
    return find_threshold(boolean_function=reject, end=max(x) / sum(x))


if __name__ == "__main__":
    # Example usage
    observed_counts = [8, 2, 0, 0, 0]  # observed frequencies
    for alpha_ in [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99]: # significance level
        start_time = time()  # Start time
        bound = get_lower_bound(observed_counts, alpha_)
        end_time = time()  # End time
        print("Significance level:", alpha_)
        print("Maximum observed frequency:", max(observed_counts) / sum(observed_counts))
        print(f"Lower bound: {bound}")
        print(f"Time taken: {end_time - start_time:.6f} seconds")
