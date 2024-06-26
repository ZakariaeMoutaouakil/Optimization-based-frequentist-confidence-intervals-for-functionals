from typing import Tuple

from tqdm import tqdm

from lower_bound.generate_multiple_indices import generate_multiple_indices
from lower_bound.get_quantile import get_quantile
from lower_bound.subdivide_interval import subdivide_interval


def get_quantiles(alpha: float,
                  n: int,
                  m: int,
                  step: float,
                  indices: Tuple[Tuple[Tuple[int, ...], ...], ...]) -> Tuple[Tuple[float, int], ...]:
    """
    Calculate the lower bound of the maximum observed frequency.

    Parameters:
    alpha (float): The significance level.
    m (int): The number of elements in the list.
    n (int): The total number of trials.
    step (float): The step size for subdivision.

    Returns:
    Tuple[int, ...]: The lower bound of the maximum observed frequency.
    """
    interval_iterator = subdivide_interval(start=1 / m, end=1, step=step, include_bounds=False)
    total_steps = int((1 - 1 / m) / step)  # Calculate the total number of steps

    quantiles = tuple(
        (q, get_quantile(alpha=alpha, q=q, n=n, m=m, indices=indices))
        for q in tqdm(interval_iterator, total=total_steps, desc="Calculating quantiles")
    )
    return quantiles


if __name__ == "__main__":
    # Example usage:
    alpha_ = 0.05  # significance level
    n_ = 10  # total number of trials
    m_ = 6  # number of elements in the list
    step_ = 0.1  # step size for subdivision
    indices_ = generate_multiple_indices(maximum=n_, dimension=m_, n=n_)

    quants = get_quantiles(alpha=alpha_, n=n_, m=m_, step=step_, indices=indices_)
    print(quants)
