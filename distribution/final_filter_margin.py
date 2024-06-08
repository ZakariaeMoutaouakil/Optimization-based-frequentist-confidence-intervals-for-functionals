from math import log
from time import time
from typing import List

from tqdm import tqdm

from distribution.vector_margins import vector_margins
from optimization.optimize_posynomial import optimize_posynomial


def final_filter(vectors: List[List[float]],
                 quantiles: List[float],
                 x: List[int]) -> float:
    maximum_likelihood = -2 * optimize_posynomial(x=x, nondecreasing=False)[0]
    print("maximum_likelihood:", maximum_likelihood)
    final_candidates = []
    for i in tqdm(range(len(vectors)), desc="Filtering vectors"):
        likelihood = -2 * sum([xi * log(pi) for pi, xi in zip(vectors[i], x) if pi != 0])
        if likelihood <= quantiles[i] + maximum_likelihood:# or  True:
            print("likelihood   :", likelihood)
            print("quantiles[i] :", quantiles[i])
            print("Adding vector:", vectors[i])
            print("Margin       :", vector_margins([vectors[i]])[0])
            final_candidates.append(vectors[i])
    margins = vector_margins(final_candidates)
    return min(margins)


if __name__ == "__main__":
    # Example usage
    vecs = [
        [0.1, 0.5, 0.4],
        [0.2, 0.3, 0.5],
        [0.3, 0.3, 0.4],
        [0.1, 0.2, 0.7]
    ]
    quants = [0.5, 0.6, 0.4, 0.7]
    x_ = [8, 2, 3]

    start_time = time()
    result = final_filter(vecs, quants, x_)
    end_time = time()
    print("Final result:", result)
    print(f"Time taken: {end_time - start_time:.6f} seconds")
