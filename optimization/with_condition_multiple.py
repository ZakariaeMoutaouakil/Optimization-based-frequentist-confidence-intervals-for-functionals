from time import time
from typing import List

from tqdm import tqdm

from optimization.maximize_product import maximize_product


def maximize_product_grid(xs: List[List[int]], threshold: float, fixed_p2s: List[float]) -> List[List[float]]:
    """
    Takes a list of x and a list of p_2 values and returns a 2D array of results
    from the maximize_product function.

    :param xs: A list of lists of fixed exponents x_i.
    :param threshold: Predefined threshold for p_i.
    :param threshold: Predefined threshold for p_1.
    :param fixed_p2s: A list of fixed values for p_2.
    :return: A 2D array of results.
    """
    return [[-2. * maximize_product(x, threshold, fixed_p2)[0] for x in xs] for fixed_p2 in
            tqdm(fixed_p2s, desc="Processing fixed_p2s")]


if __name__ == "__main__":
    # Example usage
    x_values = [
        [2, 5, 2, 1, 5],
        [1, 2, 5, 3, 7]
    ]
    p2_values = [0.1, 0.09]
    threshold_ = 0.8

    start_time = time()
    final_results = maximize_product_grid(x_values, threshold_, p2_values)
    end_time = time()

    for i, row in enumerate(final_results):
        for j, value in enumerate(row):
            print(f"Result for xs[{i}] and fixed_p2s[{j}]:")
            print("  Optimal value:", value)

    print(f"Time taken: {end_time - start_time:.6f} seconds")
