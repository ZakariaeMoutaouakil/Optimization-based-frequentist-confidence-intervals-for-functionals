from math import log
from time import time
from typing import List, Tuple

from cvxpy import Variable, Minimize, sum, Problem, power


def optimize_posynomial(x: List[int], margin: float = None, debug: bool = False) -> Tuple[float, List[float]]:
    m = len(x)
    p = Variable(m, pos=True)

    # Create the posynomial element-wise
    posynomial_terms = [power(p[i], -x[i]) for i in range(m)]
    posynomial = sum(posynomial_terms)

    constraints = [
                      (p[i] ** (-1)) * p[i + 1] <= 1 for i in range(m - 1)
                  ] + [
                      sum(p) <= 1
                  ]

    if margin is not None:
        constraints.append(p[0] * (p[1] ** (-1)) == margin)

    if debug:
        assert posynomial.is_dgp(), "Posynomial is not DGP"
        assert all(constraint.is_dgp() for constraint in constraints), "Constraints are not DGP"

    objective = Minimize(posynomial)

    prob = Problem(objective, constraints=constraints)
    prob.solve(gp=True)

    return -log(prob.value), p.value.tolist()


if __name__ == "__main__":
    # Example usage with margin
    x_ = [1, 1, 1, 1, 1, 1]
    margin_ = 1.5
    start_time = time()
    optimal_value, optimal_p_values = optimize_posynomial(x_, margin_, debug=True)
    end_time = time()

    print("Optimal value:", optimal_value)
    print("Optimal p values:", optimal_p_values)
    print("Sum of p values:", sum(optimal_p_values))
    print("Margin:", optimal_p_values[0] / optimal_p_values[1])
    print(f"Time taken: {end_time - start_time:.6f} seconds\n")

    # Example usage without margin
    x_ = [1, 1, 1, 1, 1, 1]
    start_time = time()
    optimal_value, optimal_p_values = optimize_posynomial(x_, debug=True)
    end_time = time()

    print("Optimal value:", optimal_value)
    print("Optimal p values:", optimal_p_values)
    print("Sum of p values:", sum(optimal_p_values))
    print(f"Time taken: {end_time - start_time:.6f} seconds")
