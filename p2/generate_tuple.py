from typing import Tuple


def generate_tuple(p1: float, q: float, m: int) -> Tuple[float, ...]:
    return (p1,) + (q,) + ((1 - p1 - q) / (m - 2),) * (m - 2)


if __name__ == "__main__":
    # Example usage:
    p1 = 0.9
    q = 0.1
    m = 3

    result = generate_tuple(p1, q, m)
    print(result)
    print(sum(result))
