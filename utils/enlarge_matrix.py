from time import time
from typing import List

from utils.unique_vector_indices import unique_vector_indices
from utils.unique_vector_indices import get_unique_vectors


def enlarge_matrix(unique_matrix: List[List[float]], mapping: List[int]) -> List[List[float]]:
    print("Mapping:", mapping)
    print("len(mapping):", len(mapping))
    print("Unique Matrix:", unique_matrix)
    print("len(unique_matrix):", len(unique_matrix))
    if not unique_matrix or not mapping:
        return []

    num_rows = len(unique_matrix)
    num_cols = len(mapping)

    enlarged_matrix = [[unique_matrix[i][mapping[j]] for j in range(num_cols)] for i in range(num_rows)]
    return enlarged_matrix


if __name__ == "__main__":
    raw_vectors = [
        [1, 2, 3],
        [3, 2, 1],
        [4, 5, 6],
        [1, 2, 3]
    ]

    unique_vectors_list = get_unique_vectors(raw_vectors)
    indices = unique_vector_indices(raw_vectors, unique_vectors_list)

    # Example unique matrix where each unique vector has associated values
    unique_matrix_ = [
        [10.0, 20.0],
        [30.0, 40.0]
    ]
    start_time = time()
    enlarged_matrix_ = enlarge_matrix(unique_matrix_, indices)
    end_time = time()

    print("Enlarged Matrix:")
    for row in enlarged_matrix_:
        print(" ".join(map(str, row)))

    print(f"Time taken: {end_time - start_time:.6f} seconds")
