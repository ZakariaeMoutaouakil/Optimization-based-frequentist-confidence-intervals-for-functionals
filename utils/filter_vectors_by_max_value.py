from time import time
from typing import Tuple

from tqdm import tqdm


def filter_vectors_by_max_value(vectors: Tuple[Tuple[float, ...], ...], threshold: float) \
        -> Tuple[Tuple[float, ...], ...]:
    """
    Filters a tuple of tuples based on the condition that their largest value must be bigger than a certain threshold.

    Args:
    - vectors (Tuple[Tuple[float, ...], ...]): A tuple of vectors (each vector is a tuple of floats).
    - threshold (float): The threshold value.

    Returns:
    - Tuple[Tuple[float, ...], ...]: A filtered tuple of vectors.
    """
    return tuple(vector for vector in tqdm(vectors, desc="Filtering vectors") if max(vector) > threshold)


if __name__ == "__main__":
    # Example usage
    vecs = (
        (0.1, 0.2, 0.3),
        (0.5, 0.4, 0.6),
        (0.7, 0.8, 0.9),
        (0.2, 0.3, 0.1)
    )
    thresh = 0.5

    start_time = time()
    filtered_vectors = filter_vectors_by_max_value(vecs, thresh)
    end_time = time()
    print("Filtered vectors:", filtered_vectors)
    print(f"Time taken: {end_time - start_time:.6f} seconds")
