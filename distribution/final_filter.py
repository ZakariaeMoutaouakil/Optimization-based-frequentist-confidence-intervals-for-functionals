from math import log
from typing import List

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
                 x: List[float],
                 multinomial_coefficients: List[int],
                 index_of_sample: int,
                 probabilities: List[List[float]],
                 threshold: float) -> float:
    maximum_likelihood = -2 * maximize_product(x=x, threshold=threshold)[0]
    final_candidates = []
    for i in range(len(vectors)):
        # if 0 in vectors[i]:
        #     continue
        probability = -2 * log(multinomial_coefficients[index_of_sample]) -2 * sum(
            [xi * log(pi) for pi, xi in zip(vectors[i], x) if pi != 0])
        print("probability:", probability)
        if not probability:
            continue
        likelihood = probability
        print("likelihood:", likelihood)
        if likelihood <= quantiles[i] + maximum_likelihood:
            final_candidates.append(vectors[i])
    second_largest_values = second_largest_of_vectors(final_candidates)
    return max(second_largest_values)
