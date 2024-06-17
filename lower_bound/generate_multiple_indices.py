from typing import Tuple

from tqdm import tqdm

from lower_bound.generate_indices import generate_indices


def generate_multiple_indices(maximum: int, dimension: int) -> Tuple[Tuple[Tuple[int, ...]], ...]:
    return tuple(generate_indices(maxi, dimension) for maxi in tqdm(range(maximum + 1), desc="Generating indices"))


if __name__ == "__main__":
    # Example usage
    maxi_ = 5  # maximum count to consider
    dim = 3  # number of different outcomes (length of p)

    indices = generate_multiple_indices(maxi_, dim)
    for i in range(len(indices)):
        print(f"Indices for {i}-th dimension:")
        print(indices[i])
