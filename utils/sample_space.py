from time import time
from typing import List

from tqdm import tqdm


def backtrack(start: int, dim: int, num: int, path: List[int], res: List[List[int]], progress_bar=None) -> None:
    if dim == 0:
        if num == 0:
            res.append(path.copy())
        return
    for i in range(start, num + 1):
        if progress_bar:
            progress_bar.update(1)
        path.append(i)
        backtrack(i, dim - 1, num - i, path, res, progress_bar)
        path.pop()


def sample_space(k: int, n: int) -> List[List[int]]:
    result: List[List[int]] = []
    total_steps = sum(range(n + 1))  # Approximation of total steps for tqdm
    with tqdm(total=total_steps, desc="Generating sample space") as progress_bar:
        backtrack(0, k, n, [], result, progress_bar)
    return result


if __name__ == "__main__":
    k_ = 3
    n_ = 5
    start_time = time()
    space = sample_space(k_, n_)
    end_time = time()

    for p in space:
        print(p)

    print(f"Time taken: {end_time - start_time:.6f} seconds")
