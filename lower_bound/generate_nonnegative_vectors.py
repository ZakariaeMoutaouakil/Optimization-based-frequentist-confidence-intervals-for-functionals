import random
from typing import Iterator, Tuple


def generate_nonnegative_vectors(num_iters: int, dim: int, max_coord: int, bias: float) -> Iterator[Tuple[int, ...]]:
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

    def vector_generator(num_iterations: int, dimension: int, max_: int, bias__: float) -> Iterator[Tuple[int, ...]]:
        for _ in range(num_iterations):
            vector = [random.randint(0, max_) for _ in range(dimension)]
            biased_index = random.randint(0, dimension - 1)
            vector[biased_index] = min(max_, int(vector[biased_index] * bias__))
            yield tuple(vector)

    return vector_generator(num_iters, dim, max_coord, bias)


if __name__ == "__main__":
    # Example usage
    num = 10
    dim_ = 3
    max_coord_ = 50
    bias_ = 4.5
    iterator = generate_nonnegative_vectors(num, dim_, max_coord_, bias_)

    for v in iterator:
        print(v)
