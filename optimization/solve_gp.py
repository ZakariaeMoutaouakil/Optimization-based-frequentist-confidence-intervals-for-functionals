from inspect import getsource
from math import log
from time import time
from typing import Tuple, Callable

from cvxpy import Variable, Minimize, sum, Problem, power


def solve_gp(x: Tuple[int, ...],
             phi: Callable[[Variable], float] = None,
             level_set: float = None,
             debug: bool = False) -> float:
    start_time = time() if debug else None
    if debug:
        print("x:", x)
        print("phi:", getsource(phi).strip() if phi is not None else None)
        print("level_set:", level_set)

    m = len(x)
    p = Variable(m, pos=True)

    # Create the posynomial element-wise
    posynomial_terms = [power(p[i], -x[i]) for i in range(m)]
    posynomial = sum(posynomial_terms)

    constraints = [sum(p) <= 1]

    if phi is not None:
        if debug:
            assert level_set is not None, "Level set must be provided if phi is provided"
            assert x == tuple(sorted(x, reverse=True)), "x must be sorted in descending order if phi is provided"
        constraints += [(p[i] ** (-1)) * p[i + 1] <= 1 for i in range(m - 1)]
        constraints.append(phi(p) == level_set)

    if debug:
        assert posynomial.is_dgp(), "Posynomial is not DGP"
        assert all(constraint.is_dgp() for constraint in constraints), "Constraints are not DGP"

    objective = Minimize(posynomial)

    problem = Problem(objective=objective, constraints=constraints)
    problem.solve(gp=True)

    if debug:
        print("Returned value:", -log(problem.value))
        print("Optimal value:", problem.value)
        print("Optimal p values:", p.value.tolist())
        print("Sum of p values:", sum(p.value.tolist()))
        if phi is not None:
            print("Empirical Level set:", phi(p.value))
            print("Expected Level set:", level_set)
        end_time = time()
        print(f"Time taken: {end_time - start_time:.6f} seconds\n")

    return -log(problem.value)


if __name__ == "__main__":
    # Example usage with margin
    x_ = (1, 1, 1, 1, 1, 1)
    margin_ = 1.5
    func: Callable[[Variable], float] = lambda p: p[0] * (p[1] ** (-1))
    solve_gp(x_, phi=func, level_set=margin_, debug=True)

    # Example usage without margin
    x_ = (10, 5, 3, 1)
    solve_gp(x_, debug=True)

    # Example usage with fixed second largest p
    x_ = (1, 1, 1, 1, 1, 1)
    second_largest = 0.4
    func: Callable[[Variable], float] = lambda p: p[1]
    solve_gp(x_, phi=func, level_set=second_largest, debug=True)

    # Example usage with fixed second largest p
    x_ = (10, 5, 3, 1)
    second_largest = 0.1
    func: Callable[[Variable], float] = lambda p: p[1]
    solve_gp(x_, phi=func, level_set=second_largest, debug=True)
