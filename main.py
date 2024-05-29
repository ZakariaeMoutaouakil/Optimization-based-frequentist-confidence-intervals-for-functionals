from typing import List

from distribution.second_largest_value import bin_second_largest_values
from optimization.log_likelihood import log_likelihood_grid
from utils.discrete_simplex import discrete_simplex
from utils.factorial import factorial_list
from utils.filter_vectors_by_max_value import filter_vectors_by_max_value
from utils.multinomial_coefficients import multinomial_coefficient
from utils.multinomial_probability import calculate_multinomial_probability_grid
from utils.unique_vectors import unique_vectors

n = 10
m = 3

sample_space: List[List[int]] = discrete_simplex(k=m, n=n, normalize=False)

threshold = 0.9
precision = 22
bin_width = 0.01

simplex: List[List[float]] = discrete_simplex(k=m, n=precision, normalize=True)
print("simplex:", simplex)
filtered_simplex = filter_vectors_by_max_value(simplex, threshold=threshold)
print("filtered_simplex:", filtered_simplex)
constraint_set = unique_vectors(filtered_simplex)
print("constraint_set:", constraint_set)

fixed_p2s = bin_second_largest_values(constraint_set, bin_width=bin_width)
print("fixed_p2s:", fixed_p2s)

likelihood = log_likelihood_grid(sample_space, threshold, fixed_p2s)
print("likelihood:", likelihood)

factorials = factorial_list(n)
multinomial_coefficients = multinomial_coefficient(vectors=sample_space, factorials=factorials)
probabilities = calculate_multinomial_probability_grid(multinomial_coefficients, constraint_set, sample_space)
print("probabilities:", probabilities)

alpha = 0.05
