from typing import Callable


def find_threshold(boolean_function: Callable[[float], bool], end: float = 1., precision: float = 1e-6) -> float:
    """
    Finds the conservative threshold for the given boolean function.

    Parameters:
    - boolean_function: A function that takes a float and returns a boolean.
    - end: The ending value of the search range. Default is 1.0.
    - precision: The precision of the threshold estimation. Default is 1e-6.

    Returns:
    - float: The conservative estimate of the threshold.
    """

    def binary_search_lower_bound(start: float, end_: float, func: Callable[[float], bool], precision_: float) -> float:
        """
        Helper function to perform binary search for the lower bound.

        Parameters:
        - start: The starting value of the search range.
        - end: The ending value of the search range.
        - func: The boolean function to evaluate.
        - precision: The precision of the search.

        Returns:
        - float: The conservative estimate of the threshold.
        """
        while end_ - start > precision_:
            mid = (start + end_) / 2.
            if func(mid):
                end_ = mid
            else:
                start = mid
        return start

    # Start the search from 0 to the end value
    return binary_search_lower_bound(0., end, boolean_function, precision)


if __name__ == "__main__":
    # Find the conservative threshold for the example boolean function
    threshold = 0.7
    conservative_threshold = find_threshold(lambda x: x >= threshold)
    assert conservative_threshold <= threshold
    print(f"The conservative threshold is: {conservative_threshold:.6f}")
