from itertools import combinations_with_replacement
from time import time
from typing import List


def discrete_simplex(k: int, n: int, normalize: bool = True) -> List[List[float]] | List[List[int]]:
    """
    Generate the discrete simplex for k coordinates and common denominator n.

    Args:
    k (int): The number of coordinates.
    n (int): The common denominator.

    Returns:
    List[List[float]]: A list of lists representing the discrete simplex points.
    """
    # Generate all combinations of k integers that sum to n
    combs = combinations_with_replacement(range(n + 1), k - 1)

    simplex = []

    for comb in combs:
        # Compute the differences between successive elements and append 0 at the start and n at the end
        point = [0] + list(comb) + [n]
        diffs = [point[i + 1] - point[i] for i in range(len(point) - 1)]

        if normalize:
            # Normalize the point to make the sum equal to 1
            normalized_point = [x / n for x in diffs]
            simplex.append(normalized_point)
        else:
            simplex.append(diffs)

    return simplex


if __name__ == "__main__":
    # Example usage:
    k_ = 5
    n_ = 7

    start_time = time()
    example_simplex = discrete_simplex(k_, n_, normalize=False)
    end_time = time()

    for p in example_simplex:
        print(p)

    print(f"Time taken: {end_time - start_time:.6f} seconds")
