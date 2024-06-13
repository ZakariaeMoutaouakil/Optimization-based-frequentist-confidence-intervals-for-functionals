import time
from typing import Tuple

from tqdm import tqdm


def get_unique_vectors(vectors: Tuple[Tuple[int, ...], ...]) -> Tuple[Tuple[int, ...], ...]:
    seen = set()
    unique_list = []
    for vec in vectors:
        vector_set = frozenset(vec)
        if vector_set not in seen:
            seen.add(vector_set)
            unique_list.append(tuple(vec))  # Ensure it's a tuple
    return tuple(unique_list)


def unique_vector_indices(raw_vectors: Tuple[Tuple[int, ...], ...], unique_vectors: Tuple[Tuple[int, ...], ...]) \
        -> Tuple[int, ...]:
    unique_map = {frozenset(vec): i for i, vec in tqdm(enumerate(unique_vectors), desc="Building unique map")}
    return tuple(unique_map[frozenset(vec)] for vec in raw_vectors)


if __name__ == "__main__":
    raw_vectors_ = (
        (1, 2, 3),
        (3, 2, 1),
        (4, 5, 6),
        (1, 2, 3)
    )

    unique_vectors_list = get_unique_vectors(raw_vectors_)

    start_time = time.time()
    indices = unique_vector_indices(raw_vectors_, unique_vectors_list)
    end_time = time.time()

    print("Indices:", indices)
    print("Time taken:", end_time - start_time, "seconds")
