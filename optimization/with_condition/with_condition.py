from time import time
from typing import List, Tuple

import cvxpy as cp


def maximize_product_under_condition(x: List[float], fixed_p2: float) -> Tuple[float, List[float]]:
    """
    Solves the geometric programming problem to maximize the product p_1^x_1 * p_2^x_2 * ... * p_n^x_n
    subject to the constraints:
    - p_1 >= p_2 >= ... >= p_n
    - p_2, p_3, ..., p_n < fixed_p2
    - p is a probability vector (sum(p) = 1)

    Args:
    - x (List[float]): List of fixed exponents x_i.
    - threshold (float): Predefined threshold for p_i (except p_1).

    Returns:
    - Tuple[float, List[float]]: The optimal value and the list of optimal p values.
    """
    n = len(x)

    # Define the variables
    p = cp.Variable(n, pos=True)

    # Define the constraints
    constraints = [
        p[0] >= fixed_p2,  # p_1 is greater than the threshold
        p[1] <= fixed_p2,  # p_2 is less than the threshold
        p[:-1] >= p[1:],  # p_1 >= p_2 >= ... >= p_n
        cp.sum(p) <= 1 - fixed_p2  # p is a probability vector
    ]

    # Define the objective function: maximize the product of p_i^x_i
    # which is equivalent to maximizing the sum of x_i * log(p_i) (since log is monotonic)
    objective = cp.Maximize(cp.sum(cp.multiply(x, cp.log(p))))

    # Define the problem
    problem = cp.Problem(objective, constraints)

    # Solve the problem
    problem.solve(solver=cp.SCS)  # You can use other solvers like ECOS, MOSEK, etc.

    # Return the optimal value and the optimal p values
    return problem.value, p.value.tolist()


if __name__ == "__main__":
    # Example usage
    x_ = [2, 4, 1]
    p2 = 0.3

    start_time = time()
    optimal_value, optimal_p = maximize_product_under_condition(x_, p2)
    end_time = time()

    print("Optimal value:", optimal_value)
    print("Optimal p values:", optimal_p)
    print("Sum of p values:", sum(optimal_p) + p2)
    print(f"Time taken: {end_time - start_time:.6f} seconds")
