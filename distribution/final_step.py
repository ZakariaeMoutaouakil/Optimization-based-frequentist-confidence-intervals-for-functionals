from math import log, factorial
from time import time
from typing import List, Callable

from tqdm import tqdm

from distribution.generate_permutations import generate_permutations
from distribution.sort_callable_values import sort_callable_values, second_largest
from optimization.solve_gp import solve_gp


def final_step(constraint_set: List[List[float]],
               quantiles: List[float],
               observation: List[int],
               func: Callable[[List[float]], float],
               minimize: bool,
               threshold: float,
               debug: bool = False) -> float:
    potential_list = []
    permutations_iterator = generate_permutations(data=observation)
    for permutation in tqdm(permutations_iterator, total=factorial(len(observation)), desc="Evaluating permutations"):
        potential_min = -2. * solve_gp(x=permutation, threshold=threshold, debug=debug)[0]
        if debug:
            print("permutation:", permutation)
            print("potential_max:", potential_min)
        potential_list.append(potential_min)
    maximum_likelihood = min(potential_list)
    if debug:
        print("maximum_likelihood:", maximum_likelihood)
    final_candidates = []
    for i in tqdm(range(len(constraint_set)), desc="Filtering final candidates"):
        likelihood = -2 * sum([xi * log(pi) for pi, xi in zip(constraint_set[i], observation) if pi != 0])
        if debug:
            print("likelihood:", likelihood)
            print("quantile  :", quantiles[i])
        if (likelihood <= (quantiles[i] + maximum_likelihood)) and (max(constraint_set[i]) > threshold):
            if debug:
                print("Adding vector:", constraint_set[i])
            final_candidates.append(constraint_set[i])
    values = sort_callable_values(vectors=final_candidates, func=func, debug=debug)
    return values[0] if minimize else values[-1]


if __name__ == "__main__":
    # Example usage
    vecs = [
        [0.1, 0.5, 0.4],
        [0.2, 0.3, 0.5],
        [0.3, 0.3, 0.4],
        [0.1, 0.2, 0.7]
    ]
    quants = [0.5, 0.6, 0.4, 0.7]
    x_ = [1, 2, 3]

    start_time = time()
    result = final_step(vecs, quants, x_, func=second_largest, minimize=True, debug=True, threshold=0.8)
    end_time = time()
    print("Final result:", result)
    print(f"Time taken: {end_time - start_time:.6f} seconds")
