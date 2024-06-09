import itertools
from typing import List, Iterator


def generate_permutations(data: List[int]) -> Iterator[List[int]]:
    """
    Generate all possible permutations of a list of integers.

    :param data: List of integers to permute.
    :return: An iterator of permutations, each permutation is a list of integers.
    """
    return (list(permutation) for permutation in itertools.permutations(data))


if __name__ == "__main__":
    # Example usage:
    vector = [1, 2, 3]
    permutations_iterator = generate_permutations(vector)

    # Print all permutations
    for perm in permutations_iterator:
        print(perm)
