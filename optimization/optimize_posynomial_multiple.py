from time import time
from typing import List

from tqdm import tqdm

from optimization.optimize_posynomial import optimize_posynomial


def optimize_posynomial_multiple(xs: List[List[int]], margins: List[float] = None) -> List[List[float]]:
    """
    Takes a list of x and a list of p_2 values and returns a 2D array of results
    from the optimize_posynomial function.
    :param xs:
    :param margins:
    :return:
    """
    return [[-2. * optimize_posynomial(x=x, margin=margin)[0] for x in xs] for margin in
            tqdm(margins, desc="Processing margins")] if margins else \
        [2. * optimize_posynomial(x=x)[0] for x in tqdm(xs, desc="Maximizing products without margin")]


if __name__ == "__main__":
    # Example usage with margin
    x_values = [
        [2, 5, 2, 1, 5],
        [1, 2, 5, 3, 7]
    ]
    margins_ = [1.1, 1.9]

    start_time = time()
    final_results = optimize_posynomial_multiple(x_values, margins_)
    end_time = time()

    for i, row in enumerate(final_results):
        for j, value in enumerate(row):
            print(f"Result for xs[{i}] and margins[{j}]:")
            print("  Optimal value:", value)

    print(f"Time taken: {end_time - start_time:.6f} seconds\n")

    # Example usage without margin
    x_values = [
        [2, 5, 2, 1, 5],
        [1, 2, 5, 3, 7]
    ]

    start_time = time()
    final_results = optimize_posynomial_multiple(x_values)
    end_time = time()

    for value in final_results:
        print("Optimal value:", value)

    print(f"Time taken: {end_time - start_time:.6f} seconds")
