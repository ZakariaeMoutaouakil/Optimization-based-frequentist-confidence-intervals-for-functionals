from time import time
from typing import List

from utils.sample_space import sample_space


def discrete_simplex(k: int, n: int) -> List[List[float]]:
    result = sample_space(k, n)

    result = [[x / n for x in vector] for vector in result]

    return result


if __name__ == "__main__":
    # Example usage:
    k_ = 3
    n_ = 5
    start_time = time()
    normalized_vectors = discrete_simplex(k_, n_)
    end_time = time()
    print("Normalized vectors:")
    print(normalized_vectors)
    print(f"Time taken: {end_time - start_time:.6f} seconds")
