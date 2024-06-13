from time import time
from typing import Tuple, Callable

from tqdm import tqdm

from distribution.sort_callable_values import margin_of_vector, second_largest


def find_closest_indices(vectors: Tuple[Tuple[float, ...], ...],
                         values: Tuple[float, ...],
                         func: Callable[[Tuple[float, ...]], float]) -> Tuple[int, ...]:
    """
    Finds the indices of the closest values in the 'values' tuple to the values computed
    by applying the given function to each vector in the 'vectors' tuple.

    Args:
    - vectors (Tuple[Tuple[float, ...], ...]): A tuple of vectors (each vector is a tuple of floats).
    - values (Tuple[float, ...]): A tuple of values to compare against.
    - func (Callable[[Tuple[float, ...]], float]): A function that computes a value from a vector.

    Returns:
    - Tuple[int, ...]: A tuple of indices corresponding to the closest values in 'values' for each computed value.
    """

    def closest_index(target: float, floats: Tuple[float, ...]) -> int:
        """
        Finds the index of the closest value in 'floats' to the 'target' value.

        Args:
        - target (float): The target value to compare against.
        - floats (Tuple[float, ...]): A tuple of float values to search within.

        Returns:
        - int: The index of the closest value in 'floats' to the 'target' value.
        """
        closest_idx = 0
        min_diff = abs(floats[0] - target)
        for i in range(1, len(floats)):
            diff = abs(floats[i] - target)
            if diff < min_diff:
                closest_idx = i
                min_diff = diff
        return closest_idx

    result = []
    for vector in tqdm(vectors, desc="Finding closest indices"):
        computed_value = func(vector)
        index = closest_index(computed_value, values)
        result.append(index)

    return tuple(result)


if __name__ == "__main__":
    # Example usage for margin_of_vector:
    vecs_margin: Tuple[Tuple[float, ...], ...] = (
        (4, 2, 5),  # Margin = 5 / 4 = 1.25
        (1, 3, 2),  # Margin = 3 / 2 = 1.5
        (8, 7, 6),  # Margin = 8 / 7 ≈ 1.14
        (1, 2, 4),  # Margin = 4 / 2 = 2.0
        (1, 2.5, 1)  # Margin = 2.5 / 1 = 2.5
    )
    vals_margin: Tuple[float, ...] = (1.5, 2.0, 1.1, 2.5)

    start_time = time()
    print("Using margin_of_vector:")
    closest_indices_margin = find_closest_indices(vecs_margin, vals_margin, margin_of_vector)
    print(closest_indices_margin)  # Expected output: indices of the closest margins
    end_time = time()
    print(f"Time taken: {end_time - start_time:.6f} seconds")

    # Example usage for second_largest:
    vecs_second_largest: Tuple[Tuple[float, ...], ...] = (
        (4, 2, 5),  # Second largest = 4
        (1, 3, 2),  # Second largest = 2
        (8, 7, 6),  # Second largest = 7
        (1, 2, 4),  # Second largest = 2
        (1, 2.5, 1)  # Second largest = 1
    )
    vals_second_largest: Tuple[float, ...] = (2.5, 4.1, 6.0, 7.5)

    start_time = time()
    print("Using second_largest:")
    closest_indices_second_largest = find_closest_indices(vecs_second_largest, vals_second_largest, second_largest)
    print(closest_indices_second_largest)  # Expected output: indices of the closest second-largest values
    end_time = time()
    print(f"Time taken: {end_time - start_time:.6f} seconds")
