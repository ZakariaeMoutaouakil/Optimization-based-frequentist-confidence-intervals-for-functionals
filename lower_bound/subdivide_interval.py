from typing import Iterator


def subdivide_interval(start: float, end: float, step: float, include_bounds: bool) -> Iterator[float]:
    """
    Subdivide an interval into points.

    :param start: Start of the interval.
    :param end: End of the interval.
    :param step: Step size for subdivision.
    :param include_bounds: Whether to include the bounds.
    :return: Generator of subdivision points.
    """
    if step <= 0:
        raise ValueError("Step size must be positive.")

    current = start
    if include_bounds:
        yield current

    current += step
    while current < end:
        yield current
        current += step

    if include_bounds and current - step != end:
        yield end


if __name__ == "__main__":
    # Example usage:
    start_ = 0.0
    end_ = 10.0
    step_ = 0.1
    include_bounds_ = False

    points_set = subdivide_interval(start_, end_, step_, include_bounds_)
    print(list(points_set))
