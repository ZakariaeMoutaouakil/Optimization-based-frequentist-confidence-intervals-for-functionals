from time import time
from typing import Tuple, Callable

from statsmodels.stats.proportion import proportion_confint

from lower_bound.find_largest_preimage import find_largest_preimage
from lower_bound.generate_nonnegative_vectors import generate_nonnegative_vectors
from lower_bound.generate_sorted_tuples import generate_sorted_tuples
from lower_bound.get_quantile import get_quantile


def final_result(alpha: float, x: Tuple[int, ...]) -> float:
    """
    Calculate the final result.

    Parameters:
    alpha (float): The significance level.
    x (Tuple[int, ...]): The tuple of observed frequencies.

    Returns:
    float: The final result.
    """
    n = sum(x)
    m = len(x)
    lower_bounds: Callable[[float], float] = lambda q: get_quantile(alpha=alpha, q=q, n=n, m=m)
    return find_largest_preimage(lower_bounds, max(x), len(x))


if __name__ == "__main__":
    # Example usage
    x_ = (10, 3, 0)
    alpha_ = 0.01
    print("Maximum observed frequency :", max(x_) / sum(x_))
    start_time = time()  # Start time
    result1 = final_result(alpha=alpha_, x=x_)
    print("My lower bound             :", result1)
    end_time = time()  # End time
    p1_ = proportion_confint(max(x_), sum(x_), alpha=2 * alpha_, method="beta")[0]
    print("Clopper Pearson lower bound:", p1_)
    print(f"Time taken: {end_time - start_time:.6f} seconds")

    alpha_ = 0.001
    print("Maximum observed frequency :", max(x_) / sum(x_))
    start_time = time()  # Start time
    result2 = final_result(alpha=alpha_, x=x_)
    print("My lower bound             :", result2)
    end_time = time()  # End time
    p1_ = proportion_confint(max(x_), sum(x_), alpha=2 * alpha_, method="beta")[0]
    print("Clopper Pearson lower bound:", p1_)
    print(f"Time taken: {end_time - start_time:.6f} seconds")
    assert result1 > result2, "Smaller alphas should give better lower bounds"

    dim = 3
    max_coord_ = 2
    max_iterations_ = 100
    iterator = generate_sorted_tuples(dim, max_coord_, max_iterations_)
    for x_ in iterator:
        print("x_                         :", x_)
        print("Maximum observed frequency :", max(x_) / sum(x_))
        start_time = time()  # Start time
        result = final_result(alpha=alpha_, x=x_)
        print("My lower bound             :", result)
        end_time = time()  # End time
        p1_ = proportion_confint(max(x_), sum(x_), alpha=2 * alpha_, method="beta")[0]
        print("Clopper Pearson lower bound:", p1_)
        print("Gain                       :", f"{result - p1_:.2f}")
        print(f"Time taken: {end_time - start_time:.6f} seconds")
        assert (result > 0 and result > p1_) or (result == 0 and p1_ < 0.5), \
            "My estimate should be better than the Clopper Pearson estimate"

    num_iters = 100
    dim = 3
    max_coord = 30
    alpha_ = 0.001
    bias = 4.5
    iterator = generate_nonnegative_vectors(num_iters, dim, max_coord, bias)
    for x_ in iterator:
        print("x_                         :", x_)
        print("Maximum observed frequency :", max(x_) / sum(x_))
        start_time = time()  # Start time
        result = final_result(alpha=alpha_, x=x_)
        print("My lower bound             :", result)
        end_time = time()  # End time
        p1_ = proportion_confint(max(x_), sum(x_), alpha=2 * alpha_, method="beta")[0]
        print("Clopper Pearson lower bound:", p1_)
        print(f"Time taken: {end_time - start_time:.6f} seconds")
        assert (result > 0 and result > p1_) or (result == 0 and p1_ < 0.5), \
            "My estimate should be better than the Clopper Pearson estimate"
