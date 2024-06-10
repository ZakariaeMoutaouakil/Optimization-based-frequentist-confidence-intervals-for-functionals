from time import time
from typing import List

from tqdm import tqdm

from optimization.solve_gp_permutations import solve_gp_permutations


def solve_gp_no_condition(xs: List[List[int]], debug: bool = False) -> List[float]:
    return [2. * solve_gp_permutations(x=x, debug=debug) for x in
            tqdm(xs, desc="Maximizing products without level set")]


if __name__ == "__main__":
    # Example usage
    x_ = [
        [2, 1, 3],
        [2, 1, 3],
        [2, 1, 3]
    ]

    start_time = time()
    optimal_values = solve_gp_no_condition(x_)
    end_time = time()

    for value in optimal_values:
        print(value)

    print(f"Time taken: {end_time - start_time:.6f} seconds")
