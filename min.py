from time import time
from typing import Tuple, Callable

from cvxpy import Variable
from statsmodels.stats.proportion import proportion_confint

from distribution.final_step import final_step
from distribution.generate_quantiles import generate_quantiles
from distribution.sort_callable_values import second_largest
from lower_bound.final_result import final_result
from utils.discrete_simplex import discrete_simplex


def seconds_to_minutes(seconds: float) -> Tuple[int, float]:
    # Calculate the minutes
    minutes = int(seconds // 60)
    # Calculate the leftover seconds
    leftover_seconds = seconds % 60
    return minutes, leftover_seconds


observation = (10, 3, 0)

n = sum(observation)
m = len(observation)

start_time = time()

grid = 101
precision = 0.001
alpha = 0.001

constraint_set: Tuple[Tuple[float, ...], ...] = discrete_simplex(k=m, n=grid, normalize=True)

phi: Callable[[Variable], float] = lambda p: p[1]
filter_func: Callable[[float], bool] = lambda x: x > 0
quantiles = generate_quantiles(constraint_set=constraint_set, filter_value=filter_func,
                               func=second_largest, n=n, phi=phi, alpha=alpha,
                               precision=precision, debug=False)

final_res = final_step(constraint_set=constraint_set, quantiles=quantiles, observation=observation,
                       func=second_largest, minimize=False, debug=True)
print("Actual p2         :", sorted(observation, reverse=True)[1] / n)
print("Expected p2       :", final_res)
assert final_res >= sorted(observation, reverse=True)[1] / n
p1_ = proportion_confint(max(observation), n, alpha=2 * alpha, method="beta")[0]
print("Clopper Pearson p2:", 1 - p1_)
p1 = final_result(alpha=alpha, x=observation)
print("Maximum method    :", 1 - p1)
print("p1_:", p1_)
end_time = time()
time_taken = end_time - start_time
if time_taken >= 60:
    minutes_taken, seconds_taken = seconds_to_minutes(time_taken)
    print(f"Time taken: {minutes_taken:.0f} minutes and {seconds_taken:.6f} seconds")
else:
    print(f"Time taken: {time_taken:.6f} seconds")
