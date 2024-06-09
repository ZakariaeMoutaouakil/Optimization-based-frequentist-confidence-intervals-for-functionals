from typing import List

from distribution.find_closest_indices import find_closest_indices
from distribution.quantile import quantile_1_minus_alpha
from distribution.second_largest_value import bin_second_largest_values
from optimization.log_likelihood import log_likelihood_grid
from utils.discrete_simplex import discrete_simplex
from utils.enlarge_matrix import enlarge_matrix
from utils.factorial import factorial_list
from utils.filter_vectors_by_max_value import filter_vectors_by_max_value
from utils.multinomial_coefficients import multinomial_coefficient
from utils.multinomial_probability import calculate_multinomial_probability_grid
from utils.sample_space import sample_space
from utils.unique_vector_indices import unique_vector_indices


def generate_quantiles(n: int,
                     m: int,
                     alpha: float = 0.05,
                     precision: int = 101,
                     threshold=0.8,
                     bin_width=0.00001) -> list[float]:
    # Calculate the constraint set
    simplex: List[List[float]] = discrete_simplex(k=m, n=precision, normalize=True)
    constraint_set = filter_vectors_by_max_value(simplex, threshold=threshold)

    # Calculate the fixed p_2 values
    fixed_p2s = bin_second_largest_values(constraint_set, bin_width=bin_width)

    # Calculate the likelihood
    ordered_x = sample_space(k=m, n=n)
    likelihood = log_likelihood_grid(ordered_x, threshold, fixed_p2s)
    full_x: List[List[int]] = discrete_simplex(k=m, n=n, normalize=False)
    x_indices = unique_vector_indices(full_x, ordered_x)
    full_likelihood = enlarge_matrix(likelihood, x_indices)

    # Calculate the multinomial coefficients
    factorials = factorial_list(n)
    multinomial_coefficients = multinomial_coefficient(vectors=ordered_x, factorials=factorials)
    probabilities = calculate_multinomial_probability_grid(multinomial_coefficients, constraint_set, ordered_x)

    # Calculate the quantiles
    indices = find_closest_indices(vectors=constraint_set, second_values=fixed_p2s)
    quantiles = [quantile_1_minus_alpha(full_likelihood[indices[i]], probabilities[i], alpha) for i in
                 range(len(probabilities))]

    return quantiles
