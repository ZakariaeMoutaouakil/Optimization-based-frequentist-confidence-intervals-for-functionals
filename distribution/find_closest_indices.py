from typing import List


def find_closest_indices(vectors: List[List[float]], values: List[float]) -> List[int]:
    def second_largest(numbers: List[float]) -> float:
        first, second = float('-inf'), float('-inf')
        for number in numbers:
            if number > first:
                first, second = number, first
            elif first > number > second:
                second = number
        return second

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
    for vector in vectors:
        sec_largest = second_largest(vector)
        index = closest_index(sec_largest, values)
        result.append(index)

    return result


if __name__ == "__main__":
    # Example usage
    vecs: List[List[float]] = [[4, 2, 5], [1, 3, 2], [8, 7, 6]]
    vals: List[float] = [2.5, 4.1, 6.0, 7.5]

    print(find_closest_indices(vecs, vals))
