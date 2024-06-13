from typing import List

from certify.partition_iterator import partition_iterator


def smallest_subset(vector: List[float], num_partitions: int, debug: bool = False) -> List[float]:
    """
    Finds the smallest subset of the given vector such that the sum of the subset is
    greater than or equal to the sum of each partition of the remaining elements.

    Args:
        vector (List[float]): A list of floating-point numbers.
        num_partitions (int): The number of partitions to divide the remaining elements into.
        debug (bool, optional): If True, prints debug information. Defaults to True.

    Returns: List[float]: A list containing the sum of the smallest subset and the sums of the partitions of the
    remaining elements.

    Raises:
        ValueError: If the number of partitions is greater than the length of the vector.

    Example:
        >>> vect = [1.0, 2.0, 2.0, 3.0, 4.0, 5.0]
        >>> num = 3
        >>> smallest_subset(vect, num)
        [8.0, 4.0, 5.0]
    """
    i = 0
    while True:
        i += 1
        subset = vector[:i]
        rest = vector[i:]
        if len(rest) < num_partitions:
            if debug:
                print("Cannot partition rest:", rest)
            return [sum(subset)] + rest
        partitions = partition_iterator(num_partitions=num_partitions - 1, float_list=rest)
        if debug:
            print("subset:", subset)
            print("Partitioning rest:", rest)
        for partition in partitions:
            if debug:
                print("partition:", partition)
            if all(sum(subset) >= sum(element) for element in partition):
                if debug:
                    print("subset:", subset, "partition:", partition)
                    print("len(subset):", len(subset), "len(partition):", len(partition))
                return [sum(subset)] + [sum(element) for element in partition]


if __name__ == "__main__":
    # Example usage of smallest_subset
    vec = [1.0, 2.0, 2.0, 3.0, 4.0, 5.0]
    num_partitions_ = 3
    result = smallest_subset(vec, num_partitions_)
    print("Smallest subset index:", result, "\n")
    assert len(result) == num_partitions_, f"Expected {num_partitions_} elements, got {len(result)}"

    # Example usage of smallest_subset
    vec = [0.1, 0.1, 0.1, 0.11]
    num_partitions_ = 2
    result = smallest_subset(vec, num_partitions_, debug=True)
    print("Smallest subset index:", result, "\n")
    assert len(result) == num_partitions_, f"Expected {num_partitions_} elements, got {len(result)}"

    # Example usage of smallest_subset
    vec = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
    num_partitions_ = 2
    result = smallest_subset(vec, num_partitions_, debug=True)
    print("Smallest subset index:", result, "\n")
    assert len(result) == num_partitions_, f"Expected {num_partitions_} elements, got {len(result)}"

    # Example usage of smallest_subset
    vec = [0.1, 0.1, 0.1, 0.1, 0.1, 10]
    num_partitions_ = 2
    result = smallest_subset(vec, num_partitions_, debug=True)
    print("Smallest subset index:", result)
    assert len(result) == num_partitions_, f"Expected {num_partitions_} elements, got {len(result)}"

    # Example usage of smallest_subset
    vec = [0.1, 0.1, 0.1, 0.2, 0.2, 0.3, 0.3, 0.4]
    num_partitions_ = 4
    result = smallest_subset(vec, num_partitions_, debug=True)
    print("Smallest subset index:", result)
    assert len(result) == num_partitions_, f"Expected {num_partitions_} elements, got {len(result)}"
