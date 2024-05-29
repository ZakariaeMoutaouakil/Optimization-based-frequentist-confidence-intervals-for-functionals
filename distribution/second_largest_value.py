from typing import List


def bin_second_largest_values(prob_vectors: List[List[float]], bin_width: float) -> List[float]:
    """
    Bin the second largest value of each probability vector and return the list of binned values.

    Args:
    - prob_vectors (List[List[float]]): A list of probability vectors.
    - bin_width (float): The width of each bin.

    Returns:
    - List[float]: A list of binned second largest values.
    """
    # Find the second largest value for each vector
    second_largest_values = [sorted(vector)[-2] for vector in prob_vectors]

    # Bin the second largest values
    binned_values = [((value // bin_width) * bin_width) for value in second_largest_values]

    # Remove zero values
    non_zero_binned_values = [value for value in binned_values if value != 0]

    return sorted(set(non_zero_binned_values))  # Remove duplicates and sort non_zero_binned_values


if __name__ == "__main__":
    # Example usage
    vectors = [
        [0.1, 0.2, 0.3, 0.4],
        [0.25, 0.25, 0.25, 0.25],
        [0.4, 0.3, 0.2, 0.1],
        [0.05, 0.05, 0.05, 0.85]
    ]
    width = 0.1

    results = bin_second_largest_values(vectors, width)
    print("Binned second largest values:", results)
