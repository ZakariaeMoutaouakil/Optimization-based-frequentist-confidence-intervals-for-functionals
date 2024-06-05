from math import factorial
from time import time
from typing import List

from tqdm import tqdm


def multinomial_coefficient(vectors: List[List[int]], factorials: List[int]) -> List[int]:
    """
    Calculate the multinomial coefficients for a list of vectors.

    Args:
    - vectors (List[List[int]]): A list of vectors (each vector is a list of integers).
    - factorials (List[int]): A list of precomputed factorials.

    Returns:
    - List[int]: A list of multinomial coefficients.
    """

    def multinomial(vector: List[int]) -> int:
        n = sum(vector)
        numerator = factorials[n]
        denominator = 1
        for k in vector:
            denominator *= factorials[k]
        return numerator // denominator

    return [multinomial(vector) for vector in tqdm(vectors, desc="Calculating multinomial coefficients")]


if __name__ == "__main__":
    # Example usage
    vecs = [
        [2, 1, 1],
        [3, 2, 1],
        [1, 1, 1, 1]
    ]

    # Precompute factorials up to the maximum value needed
    max_value = max(sum(vector) for vector in vecs)
    factorial_list = [factorial(i) for i in range(max_value + 1)]

    start_time = time()
    results = multinomial_coefficient(vecs, factorial_list)
    end_time = time()

    print(results)  # Output: [12, 60, 24]
    print(f"Time taken: {end_time - start_time:.6f} seconds")
