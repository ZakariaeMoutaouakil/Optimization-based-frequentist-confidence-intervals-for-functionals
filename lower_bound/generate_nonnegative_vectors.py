import random
from typing import Iterator, List


def generate_nonnegative_vectors(num_iters: int, dim: int, max_coord: int, bias: float) -> Iterator[List[int]]:
    """
    Generate an iterator of vectors with nonnegative coordinates.

    Parameters:
    num_iters (int): The number of vectors to generate.
    dim (int): The dimension of each vector.
    max_coord (int): The maximum value for each coordinate.
    bias (float): A bias factor that controls how much one coordinate is bigger than the others.

    Returns:
    Iterator[List[int]]: An iterator that yields vectors of the specified dimension with nonnegative coordinates.
    """

    def vector_generator(num_iters: int, dim: int, max_coord: int, bias: float) -> Iterator[List[int]]:
        for _ in range(num_iters):
            vector = [random.randint(0, max_coord) for _ in range(dim)]
            biased_index = random.randint(0, dim - 1)
            vector[biased_index] = min(max_coord, int(vector[biased_index] * bias))
            yield vector

    return vector_generator(num_iters, dim, max_coord, bias)


if __name__ == "__main__":
    # Example usage
    num_iters = 10
    dim = 3
    max_coord = 50
    bias = 4.5
    iterator = generate_nonnegative_vectors(num_iters, dim, max_coord, bias)

    for vector in iterator:
        print(vector)
