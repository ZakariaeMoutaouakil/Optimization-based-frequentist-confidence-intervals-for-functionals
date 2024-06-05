import time
from typing import List


def get_unique_vectors(vectors: List[List[int]]) -> List[List[int]]:
    seen = set()
    unique_list = []
    for vec in vectors:
        vector_set = frozenset(vec)
        if vector_set not in seen:
            seen.add(vector_set)
            unique_list.append(vec)
    return unique_list


def unique_vector_indices(raw_vectors: List[List[int]], unique_vectors: List[List[int]]) -> List[int]:
    unique_map = {frozenset(vec): i for i, vec in enumerate(unique_vectors)}
    return [unique_map[frozenset(vec)] for vec in raw_vectors]


if __name__ == "__main__":
    raw_vectors_ = [
        [1, 2, 3],
        [3, 2, 1],
        [4, 5, 6],
        [1, 2, 3]
    ]

    unique_vectors_list = get_unique_vectors(raw_vectors_)

    start_time = time.time()
    indices = unique_vector_indices(raw_vectors_, unique_vectors_list)
    end_time = time.time()

    print("Indices:", indices)
    print("Time taken:", end_time - start_time, "seconds")
