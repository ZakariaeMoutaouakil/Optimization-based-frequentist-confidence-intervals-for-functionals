from time import time
from typing import List, Tuple

import cvxpy as cp


def maximize_product(x: List[int], threshold: float = None, fixed_p2: float = None) -> Tuple[float, List[float]]:
    """
    Solves the geometric programming problem to maximize the product p_1^x_1 * p_2^x_2 * ... * p_n^x_n
    subject to the constraints:
    - p_1 >= p_2 >= ... >= p_n
    - p_2, p_3, ..., p_n < threshold
    - p is a probability vector (sum(p) = 1 if fixed_p2 is None, else sum(p) <= 1 - threshold)
    - p_2 can be fixed if specified

    Args:
    - x (List[float]): List of fixed exponents x_i.
    - threshold (float): Predefined threshold for p_i.
    - fixed_p2 (float, optional): Fixed value for p_2, if any. Default is None.

    Returns:
    - Tuple[float, List[float]]: The optimal value and the list of optimal p values.
    """
    n = len(x)

    # Define the variables
    p = cp.Variable(n, pos=True)

    # Define the constraints
    constraints = [
        cp.sum(p) <= 1  # p is a probability vector
    ]

    if threshold is not None:
        constraints.append(p[0] >= threshold)  # p_1 is greater than the threshold
        constraints.append(p[:-1] >= p[1:])  # p_1 >= p_2 >= ... >= p_n

    if fixed_p2 is not None:
        constraints.append(p[1] == fixed_p2)  # p_2 is fixed in advance

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
    # Example usage with fixed p_2
    x_ = [0, 4, 1]
    threshold_ = 0.9
    p2_fixed = 0.05

    start_time = time()
    optimal_value, optimal_p = maximize_product(x_, threshold_, p2_fixed)
    end_time = time()

    print("Optimal value with fixed p_2:", optimal_value)
    print("Optimal p values with fixed p_2:", optimal_p)
    print("Sum of p values with fixed p_2:", sum(optimal_p))
    print(f"Time taken with fixed p_2: {end_time - start_time:.6f} seconds\n")

    # Example usage without fixed p_2
    x_ = [2, 5, 2, 1, 5, 1]
    threshold_ = 0.8

    start_time = time()
    optimal_value, optimal_p = maximize_product(x_, threshold_)
    end_time = time()

    print("Optimal value without fixed p_2:", optimal_value)
    print("Optimal p values without fixed p_2:", optimal_p)
    print("Sum of p values without fixed p_2:", sum(optimal_p))
    print(f"Time taken without fixed p_2: {end_time - start_time:.6f} seconds")
