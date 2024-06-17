from typing import Tuple

from p2.p_value import p_value


def reject_test(q: Tuple[float, ...],
                x: Tuple[int, ...],
                sample_space: Tuple[Tuple[int, ...], ...],
                multinomial_coefficients: Tuple[int, ...],
                alpha: float) -> bool:
    return p_value(q=q, x=x, sample_space=sample_space, multinomial_coefficients=multinomial_coefficients) < alpha
