from typing import Callable


def find_largest_false(func: Callable[[int], bool]) -> int:
    # Define an initial range to search within
    low, high = 0, 1

    # First, find an upper bound where func(high) returns True
    while not func(high):
        low = high
        high *= 2

    # Now perform binary search between low and high
    while low < high:
        mid = (low + high) // 2
        if func(mid):
            high = mid
        else:
            low = mid + 1

    return low - 1


if __name__ == "__main__":
    # Example usage
    def example_func(x: int) -> bool:
        return x > 100


    result = find_largest_false(example_func)
    print(result)  # Should print 100
