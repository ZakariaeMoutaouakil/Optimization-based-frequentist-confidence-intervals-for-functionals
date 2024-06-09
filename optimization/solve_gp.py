from math import log
from time import time
from typing import List, Tuple, Callable

from cvxpy import Variable, Minimize, sum, Problem, power


def solve_gp(x: List[int],
             phi: Callable[[Variable], float] = None,
             level_set: float = None,
             threshold: float = None,
             non_increasing: bool = True,
             debug: bool = False) -> Tuple[float, List[float]]:
    if debug:
        print("x:", x)
        print("phi:", phi)
        print("level_set:", level_set)
        print("non_increasing:", non_increasing)

    m = len(x)
    p = Variable(m, pos=True)

    # Create the posynomial element-wise
    posynomial_terms = [power(p[i], -x[i]) for i in range(m)]
    posynomial = sum(posynomial_terms)

    constraints = [
        sum(p) <= 1
    ]

    if non_increasing:
        constraints += [(p[i] ** (-1)) * p[i + 1] <= 1 for i in range(m - 1)]

    if threshold is not None:
        if debug:
            assert non_increasing, "Non-increasing constraint must be enabled if threshold is provided"
        constraints.append(sum(p[1:]) <= 1 - threshold)

    if phi is not None:
        if debug:
            assert level_set is not None, "Level set must be provided if phi is provided"
        constraints.append(phi(p) == level_set)

    if debug:
        assert posynomial.is_dgp(), "Posynomial is not DGP"
        assert all(constraint.is_dgp() for constraint in constraints), "Constraints are not DGP"

    objective = Minimize(posynomial)

    problem = Problem(objective=objective, constraints=constraints)
    problem.solve(gp=True)

    return -log(problem.value), p.value.tolist()


if __name__ == "__main__":
    # Example usage with margin
    x_ = [1, 1, 1, 1, 1, 1]
    margin_ = 1.5
    func: Callable[[Variable], float] = lambda p: p[0] * (p[1] ** (-1))

    start_time = time()
    optimal_value, optimal_p_values = solve_gp(x_, phi=func, level_set=margin_, debug=True)
    end_time = time()

    print("Optimal value:", optimal_value)
    print("Optimal p values:", optimal_p_values)
    print("Sum of p values:", sum(optimal_p_values))
    print("Margin:", func(optimal_p_values))
    print(f"Time taken: {end_time - start_time:.6f} seconds\n")

    # Example usage without margin
    x_ = [1, 1, 1, 1, 1, 1]
    start_time = time()
    optimal_value, optimal_p_values = solve_gp(x_, debug=True)
    end_time = time()

    print("Optimal value:", optimal_value)
    print("Optimal p values:", optimal_p_values)
    print("Sum of p values:", sum(optimal_p_values))
    print(f"Time taken: {end_time - start_time:.6f} seconds\n")

    # Example usage with fixed second largest p
    x_ = [1, 1, 1, 1, 1, 1]
    second_largest = 0.4
    func: Callable[[Variable], float] = lambda p: p[1]

    start_time = time()
    optimal_value, optimal_p_values = solve_gp(x_, phi=func, level_set=second_largest, debug=True)
    end_time = time()

    print("Optimal value:", optimal_value)
    print("Optimal p values:", optimal_p_values)
    print("Sum of p values:", sum(optimal_p_values))
    print("Second largest:", func(optimal_p_values))
    print(f"Time taken: {end_time - start_time:.6f} seconds\n")

    # Example usage with fixed second largest p
    x_ = [1, 1, 1, 1, 1, 1]
    second_largest = 0.1
    func: Callable[[Variable], float] = lambda p: p[1]

    start_time = time()
    optimal_value, optimal_p_values = solve_gp(x_, phi=func, level_set=second_largest, debug=True, threshold=0.8)
    end_time = time()

    print("Optimal value:", optimal_value)
    print("Optimal p values:", optimal_p_values)
    print("Sum of p values:", sum(optimal_p_values))
    print("Second largest:", func(optimal_p_values))
    print(f"Time taken: {end_time - start_time:.6f} seconds\n")
