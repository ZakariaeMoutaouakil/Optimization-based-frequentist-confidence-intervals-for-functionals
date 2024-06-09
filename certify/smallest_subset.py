from typing import List

from certify.is_bigger import is_bigger
from certify.partition_list import partition_iterator


def smallest_subset(vector: List[float], num_partitions: int, debug: bool = True) -> int:
    i = 0
    while True:
        i += 1
        subset = vector[:i]
        rest = vector[i:]
        if len(rest) < num_partitions:
            if debug:
                print("rest:", rest)
            break
        partitions = partition_iterator(num_partitions=num_partitions - 1, float_list=rest)
        if debug:
            print("Partitioning rest:", rest)
        for partition in partitions:
            if debug:
                print("partition:", partition)
            if is_bigger(value=sum(subset), partition=partition):
                if debug:
                    print("subset:", subset, "partition:", partition)
                    print("len(subset):", len(subset), "len(partition):", len(partition))
                return i
    return i


if __name__ == "__main__":
    # Example usage of smallest_subset
    vec = [1.0, 2.0, 2.0, 3.0, 4.0, 5.0]
    num_partitions_ = 3
    result = smallest_subset(vec, num_partitions_)
    print("Smallest subset index:", result)
    print("Subset:", vec[:result], "\n")

    # Example usage of smallest_subset
    vec = [0.1, 0.1, 0.1, 0.11]
    num_partitions_ = 2
    result = smallest_subset(vec, num_partitions_)
    print("Smallest subset index:", result)
    print("Subset:", vec[:result], "\n")

    # Example usage of smallest_subset
    vec = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
    num_partitions_ = 2
    result = smallest_subset(vec, num_partitions_)
    print("Smallest subset index:", result)
    print("Subset:", vec[:result], "\n")

    # Example usage of smallest_subset
    vec = [0.1, 0.1, 0.1, 0.1, 0.1, 10]
    num_partitions_ = 2
    result = smallest_subset(vec, num_partitions_)
    print("Smallest subset index:", result)
    print("Subset:", vec[:result])
