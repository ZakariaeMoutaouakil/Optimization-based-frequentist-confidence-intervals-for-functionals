from typing import Tuple


def remove_zeros(coords: Tuple[float, ...], min_dimension: int) -> Tuple[float, ...]:
    """
    Sorts and removes zeros from a tuple of coordinates.
    Args:
    - coords (Tuple[float, ...]): A tuple of coordinates.
    - min_dimension (int): The minimum dimension of the processed coordinates.

    Returns:
    - Tuple[float, ...]: A tuple of processed coordinates.
    """
    # Sort the tuple in non-decreasing order
    sorted_coords = sorted(coords)

    # Count the number of zeros in the sorted list
    zero_count = sorted_coords.count(0.0)

    # Calculate the number of elements to remove (zeros) while respecting the min_dimension
    num_to_remove = min(zero_count, len(sorted_coords) - min_dimension)

    # Remove the zeros
    processed_coords = sorted_coords[num_to_remove:]

    return tuple(processed_coords)


if __name__ == "__main__":
    # Example usage:
    vec = (0.0, 2.3, 0.0, 5.1, 0.0, 1.2)
    dim = 3
    result = remove_zeros(vec, dim)
    print(result)  # Output: (1.2, 2.3, 5.1)

    vec = (0.0, 2.3, 0.0, 5.1, 0.0, 1.2)
    dim = 5
    result = remove_zeros(vec, dim)
    print(result)  # Output: (0.0, 0.0, 1.2, 2.3, 5.1)

    vec = (2.0, 2.3, 1.0, 5.1, 0.1, 1.2)
    dim = 5
    result = remove_zeros(vec, dim)
    print(result)  # Output: (2.0, 2.3, 1.0, 5.1, 0.1, 1.2)
