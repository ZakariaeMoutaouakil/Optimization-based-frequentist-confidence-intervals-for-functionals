from math import prod
from time import time
from typing import Tuple

from tqdm import tqdm


def calculate_multinomial_probability_grid(
        multinomial_coefficients: Tuple[int, ...],
        probability_vectors: Tuple[Tuple[float, ...], ...],
        x_values: Tuple[Tuple[int, ...], ...]
) -> Tuple[Tuple[float, ...], ...]:
    """
    Calculate a 2D array where each tuple corresponds to a probability vector and contains
    the multinomial coefficient times p^x.

    Args:
    - multinomial_coefficients (Tuple[int, ...]): A tuple of multinomial coefficients.
    - probability_vectors (Tuple[Tuple[float, ...], ...]): A tuple of probability vectors.
    - x_values (Tuple[Tuple[int, ...], ...]): A tuple of x values.

    Returns:
    - Tuple[Tuple[float, ...], ...]: A 2D tuple of results.
    """
    results = []
    for prob_vector in tqdm(probability_vectors, desc="Calculating probabilities"):
        row_results = []
        for c, x in zip(multinomial_coefficients, x_values):
            term = c * prod(pi ** xi for pi, xi in zip(prob_vector, x))
            row_results.append(term)
        results.append(tuple(row_results))
    return tuple(results)


if __name__ == "__main__":
    # Example usage
    coefficients = (12, 60, 24)
    vectors = (
        (0.2, 0.3, 0.5),
        (0.1, 0.1, 0.8),
        (0.4, 0.4, 0.2)
    )
    xs = (
        (2, 1, 1),
        (3, 2, 1),
        (1, 1, 1)
    )

    start_time = time()
    res = calculate_multinomial_probability_grid(coefficients, vectors, xs)
    end_time = time()

    for i, row in enumerate(res):
        print(f"Results for probability vector {i}: {row}")
    print(f"Time taken: {end_time - start_time:.6f} seconds")
