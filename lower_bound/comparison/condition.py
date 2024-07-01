from typing import Tuple

from lower_bound.get_quantile import get_quantile
from lower_bound.multinomial_max_cdf import multinomial_max_cdf


def condition_accept(n: int, p: Tuple[float, ...], p1: float, indices: Tuple[Tuple[Tuple[int, ...], ...], ...],
                     alpha: float) -> float:
    x = get_quantile(alpha=alpha, q=p1, n=n, m=len(p), indices=indices)
    print("x:", x)
    print("cdf:", multinomial_max_cdf(x=x, n=n, p=p, indices=indices))
    return multinomial_max_cdf(x=x, n=n, p=p, indices=indices)
