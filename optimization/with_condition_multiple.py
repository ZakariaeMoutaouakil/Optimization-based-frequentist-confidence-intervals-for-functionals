from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time
from typing import List

from optimization.maximize_product import maximize_product


def maximize_product_grid(xs: List[List[float]], threshold: float, fixed_p2s: List[float]) -> List[List[float]]:
    results = []

    def task(x, fixed_p2):
        return -2. * maximize_product(x, threshold, fixed_p2)[0]

    with ThreadPoolExecutor() as executor:
        future_to_params = {(executor.submit(task, x, fixed_p2)): (x, fixed_p2) for fixed_p2 in fixed_p2s for x in xs}

        grid = {fixed_p2: [] for fixed_p2 in fixed_p2s}
        for future in as_completed(future_to_params):
            x, fixed_p2 = future_to_params[future]
            try:
                result = future.result()
                grid[fixed_p2].append(result)
            except Exception as exc:
                print(f'An error occurred for input (x={x}, fixed_p2={fixed_p2}): {exc}')

        # Convert the grid dictionary to a list of lists
        results = [grid[fixed_p2] for fixed_p2 in fixed_p2s]

    return results


if __name__ == "__main__":
    # Example usage
    x_values = [
        [2, 1.5, 1.2, 1, 0.5],
        [1, 2, 1.5, 1.3, 0.7],
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
