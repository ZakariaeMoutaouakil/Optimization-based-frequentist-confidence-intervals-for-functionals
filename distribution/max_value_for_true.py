from typing import List


def max_value_for_true(booleans: List[bool], values: List[float]) -> float:
    """
    Returns the biggest float among the values that correspond to true in the boolean list.

    Args:
    - booleans (List[bool]): A list of boolean values.
    - values (List[float]): A list of float values.

    Returns:
    - float: The biggest float among the values that correspond to true in the boolean list.
    """
    if len(booleans) != len(values):
        raise ValueError("The length of booleans and values lists must be the same")

    # Filter the values based on the boolean list
    filtered_values = [value for bool_value, value in zip(booleans, values) if bool_value]

    if not filtered_values:
        raise ValueError("No true values in the boolean list")

    # Return the maximum value among the filtered values
    return max(filtered_values)


if __name__ == "__main__":
    # Example usage
    bools = [False, True, False, True, True]
    vals = [1.2, 3.4, 4.2, 2.6, 2.8]

    max_value = max_value_for_true(bools, vals)
    print("The biggest value corresponding to true is:", max_value)
