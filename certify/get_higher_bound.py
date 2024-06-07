from time import time
from typing import List

from distribution.final_filter import final_filter
from distribution.find_closest_indices import find_closest_indices
from distribution.quantile import quantile_1_minus_alpha
from distribution.second_largest_value import bin_second_largest_values
from margin import seconds_to_minutes
from optimization.log_likelihood import log_likelihood_grid
from utils.discrete_simplex import discrete_simplex
from utils.enlarge_matrix import enlarge_matrix
from utils.factorial import factorial_list
from utils.filter_vectors_by_max_value import filter_vectors_by_max_value
from utils.multinomial_coefficients import multinomial_coefficient
from utils.multinomial_probability import calculate_multinomial_probability_grid
from utils.sample_space import sample_space
from utils.unique_vector_indices import unique_vector_indices
from utils.unique_vectors import unique_vectors


def get_higher_bound(observation: List[int],
                     alpha: float = 0.05,
                     precision: int = 101,
                     threshold=0.8,
                     bin_width=0.00001) -> float:
    n = sum(observation)
    m = len(observation)
    assert max(observation) >= threshold * n
    # Calculate the constraint set
    simplex: List[List[float]] = discrete_simplex(k=m, n=precision, normalize=True)
    # print("simplex:", simplex)
    filtered_simplex = filter_vectors_by_max_value(simplex, threshold=threshold)
    # print("filtered_simplex:", filtered_simplex)
    constraint_set = unique_vectors(filtered_simplex)
    # print("constraint_set:", constraint_set)

    # Calculate the fixed p_2 values
    fixed_p2s = bin_second_largest_values(constraint_set, bin_width=bin_width)
    print("fixed_p2s:", fixed_p2s)

    # Calculate the likelihood
    ordered_x = sample_space(k=m, n=n)
    # print("ordered_x:", ordered_x)
    likelihood = log_likelihood_grid(ordered_x, threshold, fixed_p2s)
    # print("likelihood:", likelihood)
    # print("length of likelihood:", len(likelihood))
    full_x: List[List[int]] = discrete_simplex(k=m, n=n, normalize=False)
    # print("full_x:", full_x)
    x_indices = unique_vector_indices(full_x, ordered_x)
    full_likelihood = enlarge_matrix(likelihood, x_indices)
    assert len(likelihood) == len(fixed_p2s)

    # Calculate the multinomial coefficients
    factorials = factorial_list(n)
    multinomial_coefficients = multinomial_coefficient(vectors=ordered_x, factorials=factorials)
    # print("multinomial coefficients:", max(multinomial_coefficients))
    probabilities = calculate_multinomial_probability_grid(multinomial_coefficients, constraint_set, ordered_x)
    # print("probabilities:", probabilities)
    # print("length of probabilities:", len(probabilities))

    # Calculate the quantiles
    indices = find_closest_indices(vectors=constraint_set, second_values=fixed_p2s)
    # print("indices:", indices)
    assert len(indices) == len(probabilities)
    quantiles = [quantile_1_minus_alpha(full_likelihood[indices[i]], probabilities[i], alpha) for i in
                 range(len(probabilities))]
    # print("quantiles:", quantiles)

    # index_of_observation = ordered_x.index(observation)
    # print("observation:", observation)
    # assert len(observation) == m
    # sample_probability = [x / n for x in observation]
    # print("sample_probability:", sample_probability)
    # assert max(sample_probability) >= threshold

    final_result = final_filter(vectors=constraint_set, quantiles=quantiles, x=observation, threshold=threshold)

    return final_result


if __name__ == "__main__":
    # Example usage
    x_ = [19, 1, 2]
    start_time = time()  # Start time
    print("Final Result:", get_higher_bound(observation=x_, alpha=0.1))
    print("Actual p2:", sorted(x_, reverse=True)[1] / sum(x_))
    end_time = time()  # End time
    time_taken = end_time - start_time
    if time_taken > 60:
        minutes_taken, seconds_taken = seconds_to_minutes(time_taken)
        print(f"Time taken: {minutes_taken:.0f} minutes and {seconds_taken:.6f} seconds")
    else:
        print(f"Time taken: {time_taken:.6f} seconds")
