from time import time
from typing import List, Tuple

from tqdm import tqdm

from distribution.filter_close_elements import filter_close_elements
from distribution.final_filter_margin import final_filter
from distribution.find_closest_indices_margin import find_closest_indices
from distribution.quantile_1_minus_alpha import quantile_1_minus_alpha
from distribution.vector_margins import vector_margins
from optimization.log_likelihood_margin import log_likelihood_grid
from utils.discrete_simplex import discrete_simplex
from utils.enlarge_matrix import enlarge_matrix
from utils.factorial import factorial_list
from utils.multinomial_coefficients import multinomial_coefficient
from utils.multinomial_probability import calculate_multinomial_probability_grid
from utils.sample_space import sample_space
from utils.unique_vector_indices import unique_vector_indices
from utils.unique_vectors import unique_vectors


def seconds_to_minutes(seconds: float) -> Tuple[int, float]:
    # Calculate the minutes
    minutes = int(seconds // 60)
    # Calculate the leftover seconds
    leftover_seconds = seconds % 60
    return minutes, leftover_seconds


n = 20
m = 3

start_time = time()

precision = 101

# Calculate the constraint set
simplex: List[List[float]] = discrete_simplex(k=m, n=precision, normalize=True)
# print("simplex:", simplex)
filtered_simplex = [vector for vector in tqdm(simplex, desc="Filtering vectors") if min(vector) > 0]
# print("filtered_simplex:", filtered_simplex)
constraint_set = unique_vectors(filtered_simplex)
# print("constraint_set:", constraint_set)

# Calculate the fixed p_2 values
margins_unfiltered = vector_margins(constraint_set)
margins = filter_close_elements(margins_unfiltered, precision=0.01)
# print("margins:", sorted(margins))

# Calculate the likelihood
ordered_x = sample_space(k=m, n=n)
# print("ordered_x:", ordered_x)
likelihood = log_likelihood_grid(ordered_x, margins=margins)
# print("likelihood:", likelihood)
# print("length of likelihood:", len(likelihood))
full_x: List[List[int]] = discrete_simplex(k=m, n=n, normalize=False)
# print("full_x:", full_x)
x_indices = unique_vector_indices(full_x, ordered_x)
full_likelihood = enlarge_matrix(likelihood, x_indices)
assert len(likelihood) == len(margins)

# Calculate the multinomial coefficients
factorials = factorial_list(n)
multinomial_coefficients = multinomial_coefficient(vectors=ordered_x, factorials=factorials)
# print("multinomial coefficients:", max(multinomial_coefficients))
probabilities = calculate_multinomial_probability_grid(multinomial_coefficients, constraint_set, ordered_x)
# print("probabilities:", probabilities)
# print("length of probabilities:", len(probabilities))

# Calculate the quantiles
indices = find_closest_indices(vectors=constraint_set, margins=margins)
print("indices:", indices)
assert len(indices) == len(probabilities)
alpha = 0.05
quantiles = [quantile_1_minus_alpha(likelihood[indices[i]], probabilities[i], alpha) for i in range(len(probabilities))]
print("Maximum quantile:", max(quantiles))
# print("quantiles:", quantiles)

observation = [10, 9, 1]
assert sum(observation) == n
# index_of_observation = ordered_x.index(observation)
# print("observation:", observation)
# assert len(observation) == m
sample_probability = [x / n for x in observation]
# print("sample_probability:", sample_probability)
# assert max(sample_probability) >= threshold

final_result = final_filter(vectors=constraint_set, quantiles=quantiles, x=observation)
print("final result:", final_result)
print("Actual margin:", vector_margins([sample_probability])[0])
# assert final_result >= sorted(observation, reverse=True)[1] / n

end_time = time()
time_taken = end_time - start_time
