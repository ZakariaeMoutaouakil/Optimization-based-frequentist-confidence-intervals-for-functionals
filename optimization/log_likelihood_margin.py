from time import time
from typing import List

from tqdm import tqdm

from optimization.optimize_posynomial_multiple import optimize_posynomial_multiple


def log_likelihood_grid(xs: List[List[int]], margins: List[float]) -> List[List[float]]:
    """
    Calculates the log likelihood for a given set of input data.

    Args: xs (List[List[float]]): A list of lists representing the input data. Each inner list contains the exponents
    for a specific input. threshold (float): The threshold value used in the maximization process. fixed_p2s (List[
    float]): A list of fixed values for p_2.

    Returns: List[List[float]]: A list of lists representing the log likelihood values for each combination of input
    data and fixed_p2s.

    This function calculates the log likelihood for a given set of input data by performing the following steps:
    1. Calculate the maximized product for each input data using the `maximize_product_list` function.
    2. Calculate the maximized product for each fixed p_2 value using the `maximize_product_grid` function.
    3. Combine the maximized product values for each input data and fixed p_2 value by adding them element-wise.
    4. Return the list of combined values.
    """
    results = []
    maximize_product_xs = optimize_posynomial_multiple(xs)
    maximize_product_margins = optimize_posynomial_multiple(xs, margins)
    for margin in tqdm(maximize_product_margins, desc="Calculating log likelihood"):
        results.append([x + y for x, y in zip(maximize_product_xs, margin)])
    return results


if __name__ == "__main__":
    # Example usage
    x_values = [
        [2, 5, 2, 1, 5],
        [1, 2, 5, 3, 7]
    ]
    margins_ = [1.1, 1.9]

    start_time = time()
    res = log_likelihood_grid(x_values, margins_)
    end_time = time()

    for i, row in enumerate(res):
        for j, value in enumerate(row):
            print(f"Result for xs[{i}] and margin[{j}]: {value}")

    print(f"Time taken: {end_time - start_time:.6f} seconds")