from higher_bound.get_quantiles import get_quantiles as get_quantiles_higher_bound
from lower_bound.get_quantiles import get_quantiles as get_quantiles_lower_bound
from lower_bound.max_first_coordinate import max_first_coordinate
from p2.is_interval_included import is_interval_included
from p2.solve_quadratic import solve_quadratic

x = (1, 0, 0, 0, 3, 4)
m = len(x)
n = sum(x)
alpha = 0.05
step = 0.1
solutions = solve_quadratic(m=m)
print(solutions)
lower_quantiles = get_quantiles_lower_bound(alpha=alpha, n=n, m=m, step=step)
a = max_first_coordinate(quantiles=lower_quantiles, maximum=max(x))
print("Lower bound:", a)
higher_quantiles = get_quantiles_higher_bound(alpha=a, n=n, m=m, step=step)
b = max_first_coordinate(quantiles=higher_quantiles, maximum=max(x))
print("Higher bound:", b)
assert is_interval_included((a, b), solutions), "The interval is not included between the solutions"
