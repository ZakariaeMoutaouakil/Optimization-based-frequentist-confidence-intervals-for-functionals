import random
from typing import Tuple


def generate_random_tuple(length: int) -> Tuple[float, ...]:
    if length <= 0:
        raise ValueError("Length must be a positive integer")

    # Generate n-1 random points
    points = sorted([random.random() for _ in range(length - 1)])

    # Include the start (0) and end (1) points
    points = [0] + points + [1]

    # Calculate the differences between consecutive points
    tuple_elements = [points[i + 1] - points[i] for i in range(length)]

    return tuple(tuple_elements)


if __name__ == "__main__":
    # Example usage:
    dim = 5
    random_tuple = generate_random_tuple(dim)
    assert sum(random_tuple) == 1, "The sum of the elements must be 1"
    assert len(random_tuple) == dim, f"The length of the tuple must be {dim}"
    assert all(x > 0 for x in random_tuple), "All elements must be positive"
    print(random_tuple)  # Outputs a tuple of 5 positive numbers that sum to 1
