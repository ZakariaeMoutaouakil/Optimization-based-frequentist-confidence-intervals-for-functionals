from statsmodels.stats.proportion import proportion_confint

from lower_bound.generate_multiple_indices import generate_multiple_indices
from lower_bound.get_quantiles import get_quantiles
from lower_bound.max_first_coordinate import max_first_coordinate

alpha = 0.05
step = 0.01
x = (1, 5, 30)
n = sum(x)
m = len(x)
indices = generate_multiple_indices(maximum=n, dimension=m, n=n)
print("Real p1:", max(x) / n)
quantiles = get_quantiles(alpha=alpha, n=n, m=m, step=step, indices=indices)
print(quantiles)
p1 = max_first_coordinate(quantiles=quantiles, maximum=max(x))
print("My p1:", p1)
p1_ = proportion_confint(max(x), n, alpha=2 * alpha, method="beta")[0]
print("statsmodels p1:", p1_)

alpha = 0.01
quantiles = get_quantiles(alpha=alpha, n=n, m=m, step=step, indices=indices)
print(quantiles)
p1 = max_first_coordinate(quantiles=quantiles, maximum=max(x))
print("My p1:", p1)
p1_ = proportion_confint(max(x), n, alpha=2 * alpha, method="beta")[0]
print("statsmodels p1:", p1_)
