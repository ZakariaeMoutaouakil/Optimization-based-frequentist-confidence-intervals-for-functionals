import itertools
import random
from typing import Iterator, Tuple


def generate_sorted_tuples(dimension: int, max_coord: int, max_iterations: int) -> Iterator[Tuple[int, ...]]:
    """
    Generates sorted tuples where the last coordinate is significantly larger than the others.

    Args:
        dimension (int): The number of coordinates in each tuple.
        max_coord (int): The maximum value for the initial coordinates.
        max_iterations (int): The maximum number of tuples to generate.

    Returns:
        Iterator[Tuple[int, ...]]: An iterator over sorted tuples.
    """
    if dimension < 2:
        raise ValueError("Dimension must be at least 2.")

    # Generate all possible tuples for the first (dimension-1) coordinates
    base_tuples = itertools.product(range(max_coord + 1), repeat=dimension - 1)

    # Randomize the multiplier for the last coordinate
    def add_random_large_last_coordinate(tup):
        multiplier = random.randint(5, 15)  # Random multiplier between 5 and 15
        return tup + (max_coord * multiplier,)

    # Create tuples with the significantly larger last coordinate
    result_tuples = (add_random_large_last_coordinate(tup) for tup in base_tuples)

    # Sort the tuples
    sorted_tuples = sorted(result_tuples)

    # Limit the number of tuples to max_iterations
    limited_tuples = itertools.islice(sorted_tuples, max_iterations)

    return iter(limited_tuples)


if __name__ == "__main__":
    # Example usage:
    dim = 3
    max_coord_ = 2
    max_iterations_ = 5
    result = generate_sorted_tuples(dim, max_coord_, max_iterations_)
    for t in result:
        print(t)
