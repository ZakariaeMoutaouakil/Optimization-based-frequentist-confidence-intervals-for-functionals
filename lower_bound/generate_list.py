from math import floor


def generate_list(m: int, q: float) -> list:
    """
    Generate a list based on the given values of m and q.

    Parameters:
    m (int): The number of elements in the list.
    q (float): The first element in the list.

    Returns:
    list: A list with the specified structure.
    """
    assert (1 / m) < q < 1, f"q={q} must be between 1/{m} and 1"
    assert m > 1, "m must be greater than 1"
    k = floor(1 / q)
    r = 1 - q * k
    return [q] * k + [r] + [0] * (m - k - 1)


if __name__ == "__main__":
    # Example usage
    m_ = 5
    q_ = 0.3
    result_list = generate_list(m_, q_)
    print(result_list)
    assert len(result_list) == m_, f"Expected {m_} elements, got {len(result_list)}"

    m_ = 5
    q_ = 0.21
    result_list = generate_list(m_, q_)
    print(result_list)
    assert len(result_list) == m_, f"Expected {m_} elements, got {len(result_list)}"
