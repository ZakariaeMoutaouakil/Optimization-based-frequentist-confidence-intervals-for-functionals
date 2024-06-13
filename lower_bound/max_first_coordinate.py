from typing import Tuple


def max_first_coordinate(quantiles: Tuple[Tuple[float, int], ...], maximum: int) -> float:
    max_first = 0.
    for point in quantiles:
        if point[1] <= maximum:
            max_first = max(max_first, point[0])
    return max_first


if __name__ == "__main__":
    # Example usage:
    quants = (
        (0.30000000000000004, 3),
        (0.4, 4),
        (0.5, 5),
        (0.6, 5),
        (0.7, 5),
        (0.7999999999999999, 6),
        (0.8999999999999999, 7),
        (0.9999999999999999, 10)
    )
    maxi = 6
    print(max_first_coordinate(quants, maxi))  # Output: 0.7
    maxi = 2
    print(max_first_coordinate(quants, maxi))  # Output: 0.7
