from typing import List, Iterator, Tuple


def partition_iterator(num_partitions: int, float_list: List[float]) -> Iterator[List[List[float]]]:
    if num_partitions <= 0:
        return iter([])  # Empty iterator for invalid partition count

    def partitions(seq: List[float], k: int) -> Iterator[List[List[float]]]:
        if k == 1:
            yield [seq]
        else:
            for i in range(1, len(seq)):
                for part in partitions(seq[i:], k - 1):
                    yield [seq[:i]] + part

    unique_partitions = set()

    for partition in partitions(float_list, num_partitions):
        partition_tuple: Tuple[Tuple[float, ...], ...] = tuple(tuple(sublist) for sublist in partition)
        if partition_tuple not in unique_partitions:
            unique_partitions.add(partition_tuple)
            yield [list(sublist) for sublist in partition_tuple]


if __name__ == "__main__":
    float_list_ = [1.0, 2.0, 2.0, 3.0]
    num_partitions_ = 2
    partitions_ = partition_iterator(num_partitions_, float_list_)
    for p in partitions_:
        print(p)

    float_list_ = [1.0]
    num_partitions_ = 3
    partitions_ = partition_iterator(num_partitions_, float_list_)
    print("Partitions:", list(partitions_))
