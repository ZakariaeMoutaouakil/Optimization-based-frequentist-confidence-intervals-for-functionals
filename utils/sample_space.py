from time import time
from typing import List


def sample_space(k: int, n: int) -> List[List[int]]:
    def backtrack(start, dim, num, path, res):
        if dim == 0:
            if num == 0:
                res.append(path[:])
            return
        for i in range(start, num + 1):
            path.append(i)
            backtrack(i, dim - 1, num - i, path, res)
            path.pop()

    result = []
    backtrack(0, k, n, [], result)
    return result


if __name__ == "__main__":
    # Example usage:
    k_ = 3
    n_ = 5
    start_time = time()
    vectors = sample_space(k_, n_)
    end_time = time()
    print(vectors)
    print(f"Time taken: {end_time - start_time:.6f} seconds")
