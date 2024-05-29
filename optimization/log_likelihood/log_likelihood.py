from typing import List


def log_likelihood_grid(xs: List[List[float]], fixed_p2s: List[float]) -> List[List[float]]:
    """
    Takes a list of x and a list of y values and returns a 2D array of results
    from the log_likelihood function.

    Args:
    - xs (List[List[float]]): A list of lists of fixed exponents x_i.
    - ys (List[List[float]]): A list of lists of fixed exponents y_i.

    Returns:
    - List[List[float]]: A 2D array of results.
    """
    return [[-2. * log_likelihood(x, y) for x in xs] for y in ys]