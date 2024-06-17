from higher_bound.get_quantiles import get_quantiles
from lower_bound.max_first_coordinate import max_first_coordinate

alpha = 0.05
step = 0.01
x = (1, 5, 20)
n = sum(x)
m = len(x)
print("Real p1:", max(x) / n)
quantiles = get_quantiles(alpha=alpha, n=n, m=m, step=step)
print(quantiles)
p1 = max_first_coordinate(quantiles=quantiles, maximum=max(x))
print("My p1:", p1)

alpha = 0.01
quantiles = get_quantiles(alpha=alpha, n=n, m=m, step=step)
print(quantiles)
p1 = max_first_coordinate(quantiles=quantiles, maximum=max(x))
print("My p1:", p1)
