from time import time
from typing import List, Tuple

from tqdm import tqdm

from distribution.filter_close_elements import filter_close_elements
from distribution.final_filter_margin import final_filter
from distribution.find_closest_indices_margin import find_closest_indices
from distribution.quantile import quantile_1_minus_alpha
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


def calculate_distribution(observation: List[int],
                           alpha: float = 0.05,
                           precision: int = 51,
                           margin_width: float = 0.01) -> float:
    n = sum(observation)
    m = len(observation)

    # Calculate the constraint set
    simplex: List[List[float]] = discrete_simplex(k=m, n=precision, normalize=True)
    filtered_simplex = [vector for vector in tqdm(simplex, desc="Filtering vectors") if min(vector) > 0]
    constraint_set = unique_vectors(filtered_simplex)

    # Calculate the fixed p_2 values
    margins_unfiltered = vector_margins(constraint_set)
    margins = filter_close_elements(margins_unfiltered, precision=margin_width)

    # Calculate the likelihood
    ordered_x = sample_space(k=m, n=n)
    likelihood = log_likelihood_grid(ordered_x, margins=margins)
    full_x: List[List[int]] = discrete_simplex(k=m, n=n, normalize=False)
    x_indices = unique_vector_indices(full_x, ordered_x)
    full_likelihood = enlarge_matrix(likelihood, x_indices)
    assert len(likelihood) == len(margins)

    # Calculate the multinomial coefficients
    factorials = factorial_list(n)
    multinomial_coefficients = multinomial_coefficient(vectors=ordered_x, factorials=factorials)
    probabilities = calculate_multinomial_probability_grid(multinomial_coefficients, constraint_set, ordered_x)
    # assert len(indices) == len(probabilities)

    # Calculate the quantiles
    indices = find_closest_indices(vectors=constraint_set, margins=margins)
    quantiles = [quantile_1_minus_alpha(full_likelihood[indices[i]], probabilities[i], alpha) for i in
                 range(len(probabilities))]

    final_result = final_filter(vectors=constraint_set, quantiles=quantiles, x=observation)

    return final_result


if __name__ == "__main__":
    # Example usage
    x_ = [10, 9, 1]
    sample_probability = [x / sum(x_) for x in x_]
    margin = vector_margins([sample_probability])[0]

    start_time = time()  # Start time
    final_res = calculate_distribution(x_)
    end_time = time()  # End time
    time_taken = end_time - start_time
    if time_taken > 60:
        minutes_taken, seconds_taken = seconds_to_minutes(time_taken)
        print(f"Time taken: {minutes_taken:.0f} minutes and {seconds_taken:.6f} seconds")
    else:
        print(f"Time taken: {time_taken:.6f} seconds")
