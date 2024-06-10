from typing import List, Callable

from cvxpy import Variable
from tqdm import tqdm

from distribution.filter_close_elements import filter_close_elements
from distribution.find_closest_indices import find_closest_indices
from distribution.quantile_1_minus_alpha import quantile_1_minus_alpha
from distribution.sort_callable_values import sort_callable_values
from optimization.solve_gp_multiple import solve_gp_multiple
from optimization.solve_gp_no_condition import solve_gp_no_condition
from utils.discrete_simplex import discrete_simplex
from utils.enlarge_matrix import enlarge_matrix
from utils.factorial import factorial_list
from utils.multinomial_coefficients import multinomial_coefficient
from utils.multinomial_probability import calculate_multinomial_probability_grid
from utils.sample_space import sample_space
from utils.unique_vector_indices import unique_vector_indices


def generate_quantiles(constraint_set: List[List[float]],
                       n: int,
                       phi: Callable[[Variable], float],
                       func: Callable[[List[float]], float],
                       alpha: float,
                       precision: float,
                       filter_value: Callable[[float], bool] = lambda x: True,
                       debug: bool = False) -> List[float]:
    m = len(constraint_set[0])

    # Calculate the level sets
    values = sort_callable_values(vectors=constraint_set, func=func, debug=debug)
    level_sets_unfiltered = filter_close_elements(values=values, precision=precision)
    level_sets = [x for x in tqdm(level_sets_unfiltered, desc="Filtering level sets") if filter_value(x)]

    # Calculate the likelihood
    ordered_x = sample_space(k=m, n=n)
    second_terms = solve_gp_no_condition(sample_space=ordered_x, debug=debug)
    likelihood = solve_gp_multiple(sample_space=ordered_x, phi=phi, level_sets=level_sets, second_terms=second_terms,
                                   debug=debug)
    full_x: List[List[int]] = discrete_simplex(k=m, n=n, normalize=False)
    x_indices = unique_vector_indices(raw_vectors=full_x, unique_vectors=ordered_x)
    full_likelihood = enlarge_matrix(unique_matrix=likelihood, mapping=x_indices)

    # Calculate the multinomial coefficients
    factorials = factorial_list(n=n)
    multinomial_coefficients = multinomial_coefficient(vectors=full_x, factorials=factorials)
    probabilities = calculate_multinomial_probability_grid(
        multinomial_coefficients=multinomial_coefficients, probability_vectors=constraint_set, x_values=full_x
    )

    # Calculate the quantiles
    indices = find_closest_indices(vectors=constraint_set, values=level_sets, func=func)
    quantiles = [
        quantile_1_minus_alpha(values=full_likelihood[indices[i]], probabilities=probabilities[i], alpha=alpha)
        for i in range(len(probabilities))
    ]

    return quantiles
