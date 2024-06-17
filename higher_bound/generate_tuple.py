from typing import Tuple


def generate_tuple(m: int, q: float) -> Tuple[float, ...]:
    """
    Generate a tuple based on the given values of m and q.

    Parameters:
    m (int): The number of elements in the list.
    q (float): The first element in the list.

    Returns:
    Tuple[float, ...]: A tuple of length m, where the first element is q and the rest are
    (1 - q) / (m - 1) for each element in the list.
    """
    return (q,) + ((1 - q) / (m - 1),) * (m - 1)


if __name__ == "__main__":
    # Example usage
    m_ = 5
    q_ = 0.3
    result = generate_tuple(m_, q_)
    print("result:", result)
    print("sum:", sum(result))
    assert len(result) == m_, f"Expected {m_} elements, got {len(result)}"
    assert result[1] == (1 - q_) / (m_ - 1), f"Expected {(1 - q_) / (m_ - 1)} in the second element, got {result[1]}"
