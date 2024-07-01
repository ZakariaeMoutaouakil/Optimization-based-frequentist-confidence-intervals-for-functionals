from typing import List

import matplotlib.pyplot as plt

from lower_bound.comparison.clopper_pearson import clopper_pearson
from lower_bound.comparison.mean_over_multinomial import mean_over_multinomial
from lower_bound.generate_multiple_indices import generate_multiple_indices
from lower_bound.get_quantile import get_quantile
from lower_bound.get_quantiles import get_quantiles
from lower_bound.max_first_coordinate import max_first_coordinate
from lower_bound.multinomial_max_cdf import multinomial_max_cdf

alpha = 0.05
delta = 0.05
p = (0., 0.1, 0.9)
N = 1000
# N = 30
step = 0.01

baseline = mean_over_multinomial(lambda x: clopper_pearson(x=x, alpha=alpha), N, p)
print("baseline:", baseline)

n = 100
# indices_dict = {}
probas: List[float] = []
for i in range(n,n+1):
    indices = generate_multiple_indices(maximum=i, dimension=len(p), n=i)
    # print("indices:", indices)
    # print("len(indices):", len(indices))
    print("i:", i)
    # quant = get_quantile(alpha=alpha, q=baseline, n=i, m=len(p), indices=indices)
    # print("quant:", quant)
    # proba = multinomial_max_cdf(x=quant, n=i, p=p, indices=indices)
    # print("proba:", proba)
    # probas.append(1 - proba)
    quantiles = get_quantiles(alpha=alpha, n=i, m=len(p), step=step, indices=indices)
    p1 = lambda x: max_first_coordinate(quantiles=quantiles, maximum=max(x))
    proba = mean_over_multinomial(p1, i, p)
    print("proba:", proba)
    print("proba > baseline:", proba > baseline)
    probas.append(proba)

# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(range(n), probas, marker='o', linestyle='-', color='b', label='Proba vs i')
plt.axhline(y=baseline, color='r', linestyle='--', label='Baseline')
plt.xlabel('i')
plt.ylabel('Proba')
plt.title('Proba vs i with Baseline')
plt.legend()
plt.grid(True)
plt.show()