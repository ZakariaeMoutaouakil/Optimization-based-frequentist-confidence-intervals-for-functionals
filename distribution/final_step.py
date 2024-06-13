from math import log, isinf
from time import time
from typing import Callable, Tuple

from tqdm import tqdm

from distribution.sort_callable_values import sort_callable_values, second_largest
from optimization.solve_gp import solve_gp


# Define the sum with the modified conditions
def custom_sum(vector: Tuple[float, ...], observation: Tuple[int, ...]) -> float:
    terms = []
    for pi, xi in zip(vector, observation):
        if pi == 0:
            if xi == 0:
                term = 0
            else:
                term = float('-inf')
        else:
            term = xi * log(pi)
        terms.append(term)

    # Check if there's an infinite term
    if any(isinf(term) for term in terms):
        return float('-inf')
    else:
        return sum(terms)


def final_step(constraint_set: Tuple[Tuple[float, ...], ...],
               quantiles: Tuple[float, ...],
               observation: Tuple[int, ...],
               func: Callable[[Tuple[float, ...]], float],
               minimize: bool,
               debug: bool = False) -> float:
    maximum_likelihood = -2. * solve_gp(x=observation, debug=debug)
    if debug:
        print("maximum_likelihood:", maximum_likelihood)

    final_candidates = []
    for i in tqdm(range(len(constraint_set)), desc="Filtering final candidates"):
        likelihood = -2. * custom_sum(vector=constraint_set[i], observation=observation)
        if debug:
            print("constraint:", constraint_set[i])
            print("likelihood:", likelihood)
            print("quantile  :", quantiles[i])
        if likelihood <= (quantiles[i] + maximum_likelihood):
            if debug:
                print("Adding vector:", constraint_set[i])
            final_candidates.append(constraint_set[i])

    values = sort_callable_values(vectors=tuple(final_candidates), func=func, debug=debug)
    return values[0] if minimize else values[-1]


if __name__ == "__main__":
    # Example usage
    vecs = (
        (0.1, 0.5, 0.4),
        (0.2, 0.3, 0.5),
        (0.3, 0.3, 0.4),
        (0.1, 0.2, 0.7)
    )
    quants = (0.5, 0.6, 0.4, 0.7)
    x_ = (1, 2, 3)

    start_time = time()
    result = final_step(vecs, quants, x_, func=second_largest, minimize=True, debug=True)
    end_time = time()
    print("Final result:", result)
    print(f"Time taken: {end_time - start_time:.6f} seconds")
