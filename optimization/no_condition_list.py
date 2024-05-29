from time import time
from typing import List

from optimization.maximize_product import maximize_product


def maximize_product_list(x: List[List[float]], threshold: float) -> list[float]:
    return [2 * maximize_product(x_i, threshold)[0] for x_i in x]


if __name__ == "__main__":
    # Example usage
    x_ = [[2, 1.5, 1.2, 1, 0.5, 0.1], [2, 1.5, 1.2, 1, 0.5, 0.1], [2, 1.5, 1.2, 1, 0.5, 0.1]]
    threshold_ = 0.1

    start_time = time()
    optimal_values = maximize_product_list(x_, threshold_)
    end_time = time()

    for value in optimal_values:
        print(value)

    print(f"Time taken: {end_time - start_time:.6f} seconds")
