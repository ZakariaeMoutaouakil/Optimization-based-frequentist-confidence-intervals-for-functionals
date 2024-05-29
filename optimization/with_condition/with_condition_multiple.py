from time import time
from typing import List

from optimization.with_condition.with_condition import maximize_product_under_condition


def maximize_product_grid(xs: List[List[float]], fixed_p2s: List[float]) -> List[List[float]]:
    """
    Takes a list of x and a list of fixed_p2 values and returns a 2D array of results
    from the maximize_product_under_condition function.

    Args:
    - xs (List[List[float]]): A list of lists of fixed exponents x_i.
    - fixed_p2s (List[float]): A list of fixed values for p_2.

    Returns:
    - List[List[float]]: A 2D array of results.
    """
    return [[-2. * maximize_product_under_condition(x, fixed_p2)[0] for x in xs] for fixed_p2 in fixed_p2s]


if __name__ == "__main__":
    # Example usage
    x_values = [
        [2, 1.5, 1.2, 1, 0.5],
        [1, 2, 1.5, 1.3, 0.7]
    ]
    p2_values = [0.3, 0.4]

    start_time = time()
    final_results = maximize_product_grid(x_values, p2_values)
    end_time = time()

    for i, row in enumerate(final_results):
        for j, value in enumerate(row):
            print(f"Result for xs[{i}] and fixed_p2s[{j}]:")
            print("  Optimal value:", value)

    print(f"Time taken: {end_time - start_time:.6f} seconds")
