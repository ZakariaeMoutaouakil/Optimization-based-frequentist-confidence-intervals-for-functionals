def generate_list(m: int, q: float) -> list:
    """
    Generate a list based on the given values of m and q.

    Parameters:
    m (int): The number of elements in the list.
    q (float): The first element in the list.

    Returns:
    list: A list with the specified structure.
    """
    if m <= 1:
        raise ValueError("m must be greater than 1")

    repeated_value = (1 - q) / (m - 1)
    return [q] + [repeated_value] * (m - 1)


if __name__ == "__main__":
    # Example usage
    m_ = 5
    q_ = 0.3
    result_list = generate_list(m_, q_)
    print(result_list)
