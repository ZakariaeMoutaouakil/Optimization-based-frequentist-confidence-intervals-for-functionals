from time import time
from typing import Tuple

from tqdm import tqdm

from optimization.solve_gp import solve_gp


def solve_gp_no_condition(sample_space: Tuple[Tuple[int, ...], ...], debug: bool = False) -> Tuple[float, ...]:
    return tuple(
        2. * solve_gp(x=x, debug=debug)
        for x in tqdm(sample_space, desc="Maximizing products without level set")
    )


if __name__ == "__main__":
    # Example usage
    x_ = (
        (2, 1, 3),
        (2, 1, 3),
        (2, 1, 3)
    )

    start_time = time()
    optimal_values = solve_gp_no_condition(x_, debug=True)
    end_time = time()

    for value in optimal_values:
        print(value)

    print(f"Time taken: {end_time - start_time:.6f} seconds")
