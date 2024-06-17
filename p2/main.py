from typing import List

from higher_bound.get_quantiles import get_quantiles as get_quantiles_higher_bound
from lower_bound.generate_multiple_indices import generate_multiple_indices
from lower_bound.get_quantiles import get_quantiles as get_quantiles_lower_bound
from lower_bound.max_first_coordinate import max_first_coordinate
from lower_bound.subdivide_interval import subdivide_interval
from p2.generate_tuple import generate_tuple
from p2.is_interval_included import is_interval_included
from p2.reject_test import reject_test
from p2.solve_quadratic import solve_quadratic
from utils.factorial import factorial_list
from utils.multinomial_coefficients import multinomial_coefficient
from utils.sample_space import sample_space

x = (1, 0, 0, 0, 3, 7)
m = len(x)
n = sum(x)
sample_space_ = sample_space(k=m, n=n)
factorials = factorial_list(n=n)
multinomial_coefficients = multinomial_coefficient(vectors=sample_space_, factorials=factorials)
alpha = 0.05
step = 0.1
print("p1:", max(x) / n)
indices = generate_multiple_indices(maximum=n, dimension=m, n=n)
solutions = solve_quadratic(m=m)
print(solutions)
lower_quantiles = get_quantiles_lower_bound(alpha=alpha, n=n, m=m, step=step, indices=indices)
# a = 0.3666666666666667
a = max_first_coordinate(quantiles=lower_quantiles, maximum=max(x))
print("Lower bound:", a)
higher_quantiles = get_quantiles_higher_bound(alpha=a, n=n, m=m, step=step, indices=indices)
# b = 0.6666666666666666
b = max_first_coordinate(quantiles=higher_quantiles, maximum=max(x))
print("Higher bound:", b)
assert is_interval_included((a, b), solutions), "The interval is not included between the solutions"

values: List[float] = []
for c in subdivide_interval(start=a, end=b, step=step, include_bounds=False):
    print("c:", c)
    print("q1:", 1 / ((m - 1) * c))
    print("q2:", 1 - c)
    for q in subdivide_interval(start=1 / ((m - 1) * c), end=1 - c, step=step, include_bounds=False):
        print("q:", q)
        q_ = generate_tuple(p1=c, m=m, q=q)
        print("q_:", q_)
        if reject_test(
                q=q_, x=x, sample_space=sample_space_, multinomial_coefficients=multinomial_coefficients, alpha=alpha
        ):
            print("Reject")
            values.append(q)

print(values)
print("Final result: ", max(values))
