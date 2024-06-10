from typing import List, Callable, Iterator

from cvxpy import Variable

from optimization.generate_permutations import generate_permutations
from optimization.solve_gp import solve_gp


def solve_gp_permutations(x: List[int],
                          phi: Callable[[Variable], float] = None,
                          level_set: float = None,
                          debug: bool = False) -> float:
    permutations_iterator: Iterator[List[int]] = generate_permutations(data=x)
    return max(
        solve_gp(x=permutation, phi=phi, level_set=level_set, debug=debug) for permutation in permutations_iterator
    )


if __name__ == "__main__":
    # Example usage
    x_ = [1, 2, 3]

    # Using the solve_gp_permutations function
    result = solve_gp_permutations(x_, debug=True)
    print(f'The result is: {result}')
