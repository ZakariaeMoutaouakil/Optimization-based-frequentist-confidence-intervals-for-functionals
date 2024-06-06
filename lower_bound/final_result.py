from time import time
from typing import List, Callable

from lower_bound.find_largest_preimage import find_largest_preimage
from lower_bound.get_lower_bound import get_lower_bound


def final_result(alpha: float, x: List[int]) -> float:
    """
    Calculate the final result.

    Parameters:
    alpha (float): The significance level.
    x (List[int]): The list of observed frequencies.

    Returns:
    float: The final result.
    """
    n = sum(x)
    m = len(x)
    lower_bounds: Callable[[float], float] = lambda q: get_lower_bound(alpha=alpha, q=q, n=n, m=m)
    return find_largest_preimage(lower_bounds, max(x))


if __name__ == "__main__":
    # Example usage
    x_ = [10, 5, 1, 2]
    print("Maximum observed frequency:", max(x_) / sum(x_))
    start_time = time()  # Start time
    print("Final Result:", final_result(alpha=0.0001, x=x_))
    end_time = time()  # End time
    print(f"Time taken: {end_time - start_time:.6f} seconds")
