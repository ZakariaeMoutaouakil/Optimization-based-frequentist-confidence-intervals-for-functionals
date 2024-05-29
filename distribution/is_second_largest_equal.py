import math
from typing import List


def is_second_largest_equal(prob_vectors: List[List[float]], value: float, precision: float) -> List[bool]:
    """
    Check if the second largest value of each probability vector is equal to the given value up to the specified
    precision.

    Args:
    - prob_vectors (List[List[float]]): A list of probability vectors.
    - value (float): The target value to compare against.
    - precision (float): The precision for the comparison.

    Returns:
    - List[bool]: A list of booleans indicating if the second largest value is equal to the value up to the precision.
    """
    result = []
    for vector in prob_vectors:
        second_largest = sorted(vector)[-2]
        result.append(math.isclose(second_largest, value, abs_tol=precision))
    return result


if __name__ == "__main__":
    # Example usage
    vectors = [
        [0.1, 0.2, 0.3, 0.4],
        [0.25, 0.25, 0.25, 0.25],
        [0.4, 0.3, 0.2, 0.1],
        [0.05, 0.05, 0.05, 0.85]
    ]
    val = 0.3
    accuracy = 0.01

    res = is_second_largest_equal(vectors, val, accuracy)
    print("Is second largest value equal to", val, "up to precision", accuracy, ":", res)
