import sys
from time import time
from typing import List, Union

from tqdm import tqdm


def get_total_size(obj, seen=None):
    """Recursively finds the total memory size of an object."""
    if seen is None:
        seen = set()

    obj_id = id(obj)
    if obj_id in seen:
        return 0

    seen.add(obj_id)
    size = sys.getsizeof(obj)

    if isinstance(obj, dict):
        size += sum([get_total_size(v, seen) for v in obj.values()])
        size += sum([get_total_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_total_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_total_size(i, seen) for i in obj])

    return size / (1024 ** 2)


def discrete_simplex(k: int, n: int, normalize: bool = True) -> Union[List[List[float]], List[List[int]]]:
    """
    Generate the discrete simplex for k coordinates and common denominator n.

    Args:
    k (int): The number of coordinates.
    n (int): The common denominator.

    Returns:
    List[List[float]]: A list of lists representing the discrete simplex points.
    """

    def generate_combinations(dim, num):
        if dim == 1:
            yield [num]
        else:
            for i in range(num + 1):
                for sub_comb in generate_combinations(dim - 1, num - i):
                    yield [i] + sub_comb

    simplex = []

    for comb in tqdm(generate_combinations(k, n), desc="Generating simplex"):
        if normalize:
            normalized_point = [x / n for x in comb]
            simplex.append(normalized_point)
        else:
            simplex.append(comb)

    return simplex


if __name__ == "__main__":
    # Example usage:
    k_ = 3
    n_ = 5

    start_time = time()
    example_simplex = discrete_simplex(k_, n_, normalize=False)
    end_time = time()

    for p in example_simplex:
        print(p)
    print(f"Total size: {get_total_size(example_simplex):.6f} MB")

    print(f"Time taken: {end_time - start_time:.6f} seconds")
