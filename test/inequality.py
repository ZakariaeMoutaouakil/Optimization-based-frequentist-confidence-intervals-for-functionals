from typing import Tuple


def inequality(p: Tuple[float, ...], p1: float, q: float) -> bool:
    """Check if p_1 == p1 and p_2 >= q."""
    p_sorted = sorted(p, reverse=True)
    return (p_sorted[0] == p1) and (p_sorted[1] >= q)


if __name__ == "__main__":
    # Example usage:
    p1 = 0.4
    q = 0.2
    p = (0.1, 0.2, 0.3, 0.4)
    result = inequality(p, p1, q)
    print(result)
