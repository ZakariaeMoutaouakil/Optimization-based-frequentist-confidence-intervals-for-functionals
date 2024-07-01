from typing import Tuple

from statsmodels.stats.proportion import proportion_confint


def clopper_pearson(x: Tuple[float, ...], alpha: float) -> float:
    return proportion_confint(max(x), sum(x), alpha=2 * alpha, method="beta")[0]


if __name__ == "__main__":
    x_ = (0, 5, 30)
    alpha_ = 0.05
    print("Real p1:", max(x_) / sum(x_))
    p1 = clopper_pearson(x=x_, alpha=alpha_)
    print("My p1:", p1)
