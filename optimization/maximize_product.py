import itertools
from time import time
from typing import List, Tuple, Dict, Callable, Any, Union, Optional

import numpy as np
from scipy.optimize import minimize


def permutation_sum_product(p: np.ndarray, x: List[int]) -> float:
    m = len(p)
    s_m = list(itertools.permutations(range(m)))
    total_sum = 0
    for sigma in s_m:
        product = 1
        for i in range(m):
            product *= p[i] ** x[sigma[i]]
        total_sum += product
    return total_sum


def objective(p: np.ndarray, x: List[int]) -> float:
    return -permutation_sum_product(p, x)


def constraint_sum(p: np.ndarray) -> float:
    return 1 - float(np.sum(p))


def constraint_order(i: int) -> Callable[[np.ndarray], float]:
    def inner(p: np.ndarray) -> float:
        return float(p[i] - p[i + 1] - 1e-8)
    return inner


def constraint_second_largest(p: np.ndarray, value: float) -> float:
    sorted_p = np.sort(p)[::-1]  # Sort in descending order
    return float(sorted_p[1] - value)


def constraint_maximum(p: np.ndarray, threshold: float) -> float:
    return float(np.max(p) - threshold)


def solve_geometric_problem(x: List[int], second_largest_value: Optional[float] = None, threshold: Optional[float] = None) -> Tuple[List[float], float]:
    m = len(x)
    p0 = np.random.rand(m)
    p0 = p0 / np.sum(p0) * 0.99  # Initial guess close to the boundary condition

    cons: Union[Dict[str, Any], List[Dict[str, Any]], None] = [{'type': 'ineq', 'fun': constraint_sum}]
    cons.extend([{'type': 'ineq', 'fun': constraint_order(i)} for i in range(m - 1)])

    if second_largest_value is not None:
        cons.append({'type': 'eq', 'fun': lambda p: constraint_second_largest(p, second_largest_value)})

    if threshold is not None:
        cons.append({'type': 'ineq', 'fun': lambda p: constraint_maximum(p, threshold)})

    bounds: List[Tuple[float, float]] = [(0.0, 1.0) for _ in range(m)]
    result = minimize(objective, p0, args=(x,), bounds=bounds, constraints=cons)
    return result.x.tolist(), -result.fun


if __name__ == "__main__":
    # Example usage without second_largest_value and threshold
    x_ = [3, 1, 2]  # Example values for x
    start_time = time()
    optimal_p, max_value = solve_geometric_problem(x_)
    end_time = time()
    print("Example without second_largest_value and threshold:")
    print("Optimal p:", optimal_p)
    print(f"Max value: {max_value:.6f}")
    print(f"Sum of optimal p: {sum(optimal_p):.6f}")
    print(f"Time taken: {end_time - start_time:.6f} seconds\n")

    # Example usage with second_largest_value
    second_largest_value_ = 0.1  # Example predefined value for the second-largest coordinate
    start_time = time()
    optimal_p, max_value = solve_geometric_problem(x_, second_largest_value_)
    end_time = time()
    print("Example with second_largest_value:")
    print("Optimal p:", optimal_p)
    print(f"Max value: {max_value:.6f}")
    print(f"Sum of optimal p: {sum(optimal_p):.6f}")
    print(f"Second largest value in optimal p: {sorted(optimal_p, reverse=True)[1]:.6f}")
    print(f"Time taken: {end_time - start_time:.6f} seconds\n")

    # Example usage with threshold
    threshold_ = 0.8  # Example threshold value
    start_time = time()
    optimal_p, max_value = solve_geometric_problem(x_, threshold=threshold_)
    end_time = time()
    print("Example with threshold:")
    print("Optimal p:", optimal_p)
    print(f"Max value: {max_value:.6f}")
    print(f"Sum of optimal p: {sum(optimal_p):.6f}")
    print(f"Maximum value in optimal p: {max(optimal_p):.6f}")
    print(f"Time taken: {end_time - start_time:.6f} seconds\n")

    # Example usage with both second_largest_value and threshold
    start_time = time()
    optimal_p, max_value = solve_geometric_problem(x_, second_largest_value_, threshold_)
    end_time = time()
    print("Example with both second_largest_value and threshold:")
    print("Optimal p:", optimal_p)
    print(f"Max value: {max_value:.6f}")
    print(f"Sum of optimal p: {sum(optimal_p):.6f}")
    print(f"Second largest value in optimal p: {sorted(optimal_p, reverse=True)[1]:.6f}")
    print(f"Maximum value in optimal p: {max(optimal_p):.6f}")
    print(f"Time taken: {end_time - start_time:.6f} seconds")
