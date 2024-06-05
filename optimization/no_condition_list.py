from time import time
from typing import List

from optimization.maximize_product import maximize_product


def maximize_product_list(x: List[List[int]]) -> list[float]:
    return [2 * maximize_product(x_i)[0] for x_i in x]


if __name__ == "__main__":
    # Example usage
    x_ = [
        [2, 1, 3],
        [2, 1, 3],
        [2, 1, 3]
    ]

    start_time = time()
    optimal_values = maximize_product_list(x_)
    end_time = time()

    for value in optimal_values:
        print(value)

    print(f"Time taken: {end_time - start_time:.6f} seconds")
