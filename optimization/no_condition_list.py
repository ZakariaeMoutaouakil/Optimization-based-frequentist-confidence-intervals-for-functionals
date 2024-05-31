from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time
from typing import List

from optimization.maximize_product import maximize_product


def maximize_product_list(x: List[List[float]], threshold: float) -> List[float]:
    results = []

    with ThreadPoolExecutor() as executor:
        future_to_x = {executor.submit(maximize_product, x_i, threshold): x_i for x_i in x}

        for future in as_completed(future_to_x):
            x_i = future_to_x[future]
            try:
                result = future.result()
                results.append(2 * result[0])
            except Exception as exc:
                print(f'An error occurred for input {x_i}: {exc}')

    return results


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
