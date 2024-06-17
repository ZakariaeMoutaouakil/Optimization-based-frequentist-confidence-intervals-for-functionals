from typing import Tuple


def generate_indices(maximum: int, dimension: int, n: int) -> Tuple[Tuple[int, ...], ...]:
    """
    Generate indices for ndindex to be used in multinomial_max_cdf.

    Parameters:
    x (int): The maximum count to consider.
    dimensions (int): The number of different outcomes (length of p).

    Returns:
    Iterable[Tuple[int, ...]]: The precomputed indices.
    """
    from numpy import ndindex
    return tuple(
        comb for comb in ndindex(*(maximum + 1 for _ in range(dimension))) if sum(comb) == n and max(comb) <= maximum
    )


if __name__ == "__main__":
    # Example usage
    maxi = 2  # maximum count to consider
    dim = 3  # number of different outcomes (length of p)
    num = 3  # number of trials

    indices = generate_indices(maxi, dim, num)
    print(indices)
    assert all(len(index) == dim for index in indices)
    assert all(all(0 <= i <= maxi for i in index) for index in indices)
