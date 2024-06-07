from time import time
from typing import List

from tqdm import tqdm


def find_closest_indices(vectors: List[List[float]], margins: List[float]) -> List[int]:
    def margin_of_vector(numbers: List[float]) -> float:
        if len(numbers) < 2:
            return float('inf')
        first, second = float('-inf'), float('-inf')
        for number in numbers:
            if number > first:
                first, second = number, first
            elif first > number > second:
                second = number
        return first / second if second != 0 else float('inf')

    def closest_index(target: float, floats: List[float]) -> int:
        closest_idx = 0
        min_diff = abs(floats[0] - target)
        for i in range(1, len(floats)):
            diff = abs(floats[i] - target)
            if diff < min_diff:
                closest_idx = i
                min_diff = diff
        return closest_idx

    result: List[int] = []
    for vector in tqdm(vectors, desc="Finding closest indices"):
        margin = margin_of_vector(vector)
        index = closest_index(margin, margins)
        result.append(index)

    return result


if __name__ == "__main__":
    # Example usage
    vecs: List[List[float]] = [[4, 2, 5], [1, 3, 2], [8, 7, 6], [1, 2, 4], [1, 2.5, 1]]
    margins_: List[float] = [1.5, 2.0, 1.1, 2.5]

    start_time = time()
    print(find_closest_indices(vecs, margins_))
    end_time = time()
    print(f"Time taken: {end_time - start_time:.6f} seconds")
