from time import time
from typing import List

from optimization.no_condition_list import maximize_product_list
from optimization.with_condition_multiple import maximize_product_grid


def log_likelihood_grid(xs: List[List[float]], threshold: float, fixed_p2s: List[float]) -> List[List[float]]:
    results = []
    maximize_product_xs = maximize_product_list(xs, threshold)
    maximize_product_fixed_p2 = maximize_product_grid(xs, threshold, fixed_p2s)
    for fixed_p2_list in maximize_product_fixed_p2:
        results.append([x + y for x, y in zip(maximize_product_xs, fixed_p2_list)])
    return results


if __name__ == "__main__":
    # Example usage
    x_values = [
        [2, 1.5, 1.2, 1, 0.5],
        [1, 2, 1.5, 1.3, 0.7]
    ]
    fixed_p2_values = [0.1, 0.05, 0.01]
    thresh = 0.8

    start_time = time()
    res = log_likelihood_grid(x_values, thresh, fixed_p2_values)
    end_time = time()

    for i, row in enumerate(res):
        for j, value in enumerate(row):
            print(f"Result for xs[{i}] and fixed_p2s[{j}]: {value}")

    print(f"Time taken: {end_time - start_time:.6f} seconds")
