from typing import Tuple


def is_interval_included(interval1: Tuple[float, float], interval2: Tuple[float, float]) -> bool:
    start1, end1 = interval1
    start2, end2 = interval2

    return start2 <= start1 and end1 <= end2


if __name__ == "__main__":
    interval1_ = (2.5, 4.0)
    interval2_ = (2.0, 5.0)
    print(is_interval_included(interval1_, interval2_))  # Outputs: True

    interval1_ = (1.0, 3.0)
    interval2_ = (2.0, 5.0)
    print(is_interval_included(interval1_, interval2_))  # Outputs: False
