from math import log
from time import time
from typing import List

from tqdm import tqdm

from optimization.maximize_product import maximize_product


def second_largest(numbers: List[float]) -> float:
    if len(numbers) < 2:
        raise ValueError("List must contain at least two elements")

    first, second = float('-inf'), float('-inf')
    for number in numbers:
        if number > first:
            first, second = number, first
        elif first > number > second:
            second = number

    if second == float('-inf'):
        raise ValueError("All elements are the same in the list")

    return second


def second_largest_of_vectors(vectors: List[List[float]]) -> List[float]:
    return [second_largest(vector) for vector in vectors]


def final_filter(vectors: List[List[float]],
                 quantiles: List[float],
                 x: List[int],
                 threshold: float) -> float:
    maximum_likelihood = -2 * maximize_product(x=x, threshold=threshold)[0]
    final_candidates = []
    for i in tqdm(range(len(vectors)), desc="Filtering vectors"):
        likelihood = -2 * sum([xi * log(pi) for pi, xi in zip(vectors[i], x) if pi != 0])
        print("likelihood:", likelihood)
        if likelihood <= quantiles[i] + maximum_likelihood:
            final_candidates.append(vectors[i])
    second_largest_values = second_largest_of_vectors(final_candidates)
    return max(second_largest_values)


if __name__ == "__main__":
    # Example usage
    vecs = [
        [0.1, 0.5, 0.4],
        [0.2, 0.3, 0.5],
        [0.3, 0.3, 0.4],
        [0.1, 0.2, 0.7]
    ]
    quants = [0.5, 0.6, 0.4, 0.7]
    x_ = [1, 2, 3]
    thresh = 0.5

    start_time = time()
    result = final_filter(vecs, quants, x_, thresh)
    end_time = time()
    print("Final result:", result)
    print(f"Time taken: {end_time - start_time:.6f} seconds")
