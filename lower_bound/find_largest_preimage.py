from typing import Callable


def find_largest_preimage(callable_func: Callable[[float], float], x: float, tolerance: float = 1e-7) -> float:
    """
    Finds the largest number y such that callable_func(y) <= x.

    :param callable_func: A non-decreasing callable function from float [0, 1] to float.
    :param x: A float value.
    :param tolerance: A tolerance level for binary search termination.
    :return: The largest float y in [0, 1] such that callable_func(y) <= x.
    """
    low, high = 0.0, 1.0

    # Edge case: if callable_func(0) > x, return 0 since no value in [0, 1] can satisfy the condition
    if callable_func(low) > x:
        return 0.0

    # Perform binary search
    while high - low > tolerance:
        mid = (low + high) / 2.0
        if callable_func(mid) <= x:
            low = mid
        else:
            high = mid

    return low


# Example of usage
if __name__ == "__main__":
    # Example callable function
    def example_func(y: float) -> float:
        return y ** 2


    x_ = 0.5
    result = find_largest_preimage(example_func, x_)
    print(f"The largest y such that example_func(y) <= {x_} is approximately: {result}")