from statsmodels.stats.proportion import proportion_confint

from higher_bound.get_quantiles import get_quantiles as get_quantiles_p2
from lower_bound.generate_multiple_indices import generate_multiple_indices
from lower_bound.get_quantiles import get_quantiles as get_quantiles_p1
from lower_bound.max_first_coordinate import max_first_coordinate

alpha = 0.05
step = 0.01
x = (4, 5, 25)
n = sum(x)
m = len(x)
indices_p1 = generate_multiple_indices(maximum=n, dimension=m, n=n)
print("Real p1:", max(x) / n)
quantiles_p1 = get_quantiles_p1(alpha=alpha, n=n, m=m, step=step, indices=indices_p1)
print(quantiles_p1)
a = max_first_coordinate(quantiles=quantiles_p1, maximum=max(x))
print("My p1:", a)
p1_ = proportion_confint(max(x), n, alpha=2 * alpha, method="beta")[0]
print("Clopper-Pearson p1:", p1_)

y = x[:len(x) - 1]
n = sum(y)
m = len(y)
print("y:", y)
print("Real p2:", max(y) / n)
indices_p2 = generate_multiple_indices(maximum=n, dimension=m, n=n)
quantiles_p2 = get_quantiles_p2(alpha=alpha, n=n, m=m, step=step, indices=indices_p2)
print(quantiles_p2)
q = max_first_coordinate(quantiles=quantiles_p2, maximum=max(y))
print("My p2:", q)

p2 = q * (1 - a)
print("My p2:", p2)
print("Pessimistic p2:", 1 - a)
