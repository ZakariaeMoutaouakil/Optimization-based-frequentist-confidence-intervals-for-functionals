from typing import List


def unique_vectors(vectors: List[List[float]]) -> List[List[float]]:
    """
    Returns a list of unique vectors, where uniqueness is determined by converting each vector to a set.

    Args:
    - vectors (List[List[float]]): A list of vectors (each vector is a list of floats).

    Returns:
    - List[List[float]]: A list of unique vectors.
    """
    # Use a set to keep track of unique vectors
    seen = set()
    unique_list = []

    for vector in vectors:
        vector_set = frozenset(vector)  # Convert the vector to a frozenset
        if vector_set not in seen:
            seen.add(vector_set)
            unique_list.append(vector)

    return unique_list


if __name__ == "__main__":
    # Example usage
    vecs = [
        [0.1, 0.2, 0.3],
        [0.3, 0.2, 0.1],
        [0.5, 0.4, 0.6],
        [0.7, 0.8, 0.9],
        [0.2, 0.1, 0.3]
    ]

    unique_vectors_list = unique_vectors(vecs)
    print("Unique vectors:", unique_vectors_list)
