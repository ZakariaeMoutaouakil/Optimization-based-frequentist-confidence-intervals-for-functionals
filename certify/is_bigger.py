from typing import List


def is_bigger(value: float, partition: List[List[float]]) -> bool:
    return all(value >= sum(vector) for vector in partition)


if __name__ == "__main__":
    # Example usage
    partition_ = [[1, 2, 3], [4, 5, 6]]
    print(is_bigger(16, partition_))
    print(is_bigger(15, partition_))
    print(is_bigger(14, partition_))
