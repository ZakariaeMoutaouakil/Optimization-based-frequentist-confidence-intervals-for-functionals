from time import time
from typing import List, Callable

from cvxpy import Variable
from tqdm import tqdm

from optimization.solve_gp import solve_gp
from optimization.solve_gp_no_condition import solve_gp_no_condition


def solve_gp_multiple(sample_space: List[List[int]],
                      phi: Callable[[Variable], float],
                      level_sets: List[float],
                      second_terms: List[float],
                      debug: bool = False) -> List[List[float]]:
    first_terms = [
        [
            -2. * solve_gp(x=x, phi=phi, level_set=level_set, debug=debug)
            for x in tqdm(sample_space, desc=f"Processing level set {level_set}", leave=False)
        ]
        for level_set in tqdm(level_sets, desc="Processing level sets")
    ]

    results: List[List[float]] = []
    for level_set in tqdm(first_terms, desc="Calculating log likelihood"):
        results.append([x + y for x, y in zip(second_terms, level_set)])

    return results


if __name__ == "__main__":
    # Example usage with margin
    x_values = [
        [2, 5, 2, 1, 5],
        [1, 2, 5, 3, 7]
    ]
    margins = [1.1, 1.9]
    func: Callable[[Variable], float] = lambda p: p[0] * (p[1] ** (-1))
    second_terms_ = solve_gp_no_condition(x_values)

    start_time = time()
    final_results = solve_gp_multiple(x_values, phi=func, level_sets=margins, second_terms=second_terms_, debug=True)
    end_time = time()

    for i, row in enumerate(final_results):
        for j, value in enumerate(row):
            print(f"Result for xs {x_values[i]} and level_set [{margins[j]}]: {value}")

    print(f"Time taken: {end_time - start_time:.6f} seconds\n")