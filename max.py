from time import time
from typing import Tuple, List, Callable

from cvxpy import Variable
from statsmodels.stats.proportion import proportion_confint

from distribution.final_step import final_step
from distribution.generate_quantiles import generate_quantiles
from utils.discrete_simplex import discrete_simplex


def seconds_to_minutes(seconds: float) -> Tuple[int, float]:
    # Calculate the minutes
    minutes = int(seconds // 60)
    # Calculate the leftover seconds
    leftover_seconds = seconds % 60
    return minutes, leftover_seconds


observation = [7, 3, 1, 2]

n = sum(observation)
m = len(observation)

start_time = time()

grid = 121
precision = 0.001
alpha = 0.05

constraint_set: List[List[float]] = discrete_simplex(k=m, n=grid, normalize=True)

phi: Callable[[Variable], float] = lambda p: p[0]
filter_func: Callable[[float], bool] = lambda x: 0 < x < 1
quantiles = generate_quantiles(constraint_set=constraint_set, filter_value=filter_func,
                               func=max, n=n, phi=phi, alpha=alpha,
                               precision=precision, debug=False)

final_result = final_step(constraint_set=constraint_set, quantiles=quantiles, observation=observation,
                          func=max, minimize=True, debug=True)
print("final result:", final_result)
print("Actual p1:", sorted(observation, reverse=True)[0] / n)
p1_ = proportion_confint(max(observation), n, alpha=2 * alpha, method="beta")[0]
print("Clopper Pearson p1:", p1_)
end_time = time()
time_taken = end_time - start_time
if time_taken >= 60:
    minutes_taken, seconds_taken = seconds_to_minutes(time_taken)
    print(f"Time taken: {minutes_taken:.0f} minutes and {seconds_taken:.6f} seconds")
else:
    print(f"Time taken: {time_taken:.6f} seconds")
