from math import prod
from time import time
from typing import List


def calculate_multinomial_probability_grid(
        multinomial_coefficients: List[int],
        probability_vectors: List[List[float]],
        x_values: List[List[int]]
) -> List[List[float]]:
    """
    Calculate a 2D array where each list corresponds to a probability vector and contains
    the multinomial coefficient times p^x.

    Args:
    - multinomial_coefficients (List[int]): A list of multinomial coefficients.
    - probability_vectors (List[List[float]]): A list of probability vectors.
    - x_values (List[List[float]]): A list of x values.

    Returns:
    - List[List[float]]: A 2D array of results.
    """
    results = []
    for prob_vector in probability_vectors:
        row_results = []
        for c, x in zip(multinomial_coefficients, x_values):
            term = c * prod(pi ** xi for pi, xi in zip(prob_vector, x))
            row_results.append(term)
        results.append(row_results)
    return results


if __name__ == "__main__":
    # Example usage
    coefficients = [12, 60, 24]
    vectors = [
        [0.2, 0.3, 0.5],
        [0.1, 0.1, 0.8],
        [0.4, 0.4, 0.2]
    ]
    xs = [
        [2, 1, 1],
        [3, 2, 1],
        [1, 1, 1]
    ]

    start_time = time()
    res = calculate_multinomial_probability_grid(coefficients, vectors, xs)
    end_time = time()

    for i, row in enumerate(res):
        print(f"Results for probability vector {i}: {row}")
    print(f"Time taken: {end_time - start_time:.6f} seconds")
