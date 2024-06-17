from typing import Tuple


def majorization(x: Tuple[float, ...], y: Tuple[float, ...]) -> bool:
    # Ensure the tuples are of the same length
    if len(x) != len(y):
        raise ValueError("The tuples must be of the same length")

    # Sort both tuples in descending order
    x_sorted = sorted(x, reverse=True)
    y_sorted = sorted(y, reverse=True)

    # Check the cumulative sum conditions
    for k in range(1, len(x) + 1):
        if sum(x_sorted[:k]) > sum(y_sorted[:k]):
            print(f"{x_sorted[:k]} > {y_sorted[:k]}")
            return False

    return True


if __name__ == "__main__":
    # Example usage:
    a = (1.0, 2.0, 3.0)
    b = (3.0, 2.0, 1.0)

    result = majorization(a, b)
    print(result)  # Output: True or False based on the condition
