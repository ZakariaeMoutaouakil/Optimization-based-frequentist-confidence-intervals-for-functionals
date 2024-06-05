from time import time
from typing import List


def backtrack(start: int, dim: int, num: int, path: List[int], res: List[List[int]]) -> None:
    if dim == 0:
        if num == 0:
            res.append(path.copy())
        return
    for i in range(start, num + 1):
        path.append(i)
        backtrack(i, dim - 1, num - i, path, res)
        path.pop()


def sample_space(k: int, n: int) -> List[List[int]]:
    result: List[List[int]] = []
    backtrack(0, k, n, [], result)
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
