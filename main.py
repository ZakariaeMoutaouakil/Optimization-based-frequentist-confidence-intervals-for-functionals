from time import time
from typing import Tuple, List, Callable

from cvxpy import Variable
from tqdm import tqdm

from distribution.final_step import final_step
from distribution.generate_quantiles import generate_quantiles
from distribution.sort_callable_values import second_largest
from utils.discrete_simplex import discrete_simplex


def seconds_to_minutes(seconds: float) -> Tuple[int, float]:
    # Calculate the minutes
    minutes = int(seconds // 60)
    # Calculate the leftover seconds
    leftover_seconds = seconds % 60
    return minutes, leftover_seconds


n = 14
m = 3

start_time = time()

grid = 101
precision = 0.001
alpha = 0.05
threshold = 0.4

# Calculate the constraint set
constraint_set_unfiltered: List[List[float]] = discrete_simplex(k=m, n=grid, normalize=True)
constraint_set = [vector for vector in tqdm(constraint_set_unfiltered, desc="Filtering vectors") if
                  max(vector) > threshold and sorted(vector, reverse=True)[1] > 2 / n]

phi: Callable[[Variable], float] = lambda p: p[1]
filter_func: Callable[[float], bool] = lambda x: 0 < x < 1 - threshold
quantiles = generate_quantiles(constraint_set=constraint_set, filter_value=filter_func,
                               func=second_largest, n=n, phi=phi, alpha=alpha,
                               precision=precision, threshold=threshold, debug=False)

observation = [9, 0, 5]
assert (sorted(observation, reverse=True)[1] / n) < 1 - threshold

final_result = final_step(constraint_set=constraint_set, quantiles=quantiles, observation=observation,
                          func=second_largest, minimize=False, threshold=threshold, debug=True)
print("final result:", final_result)
print("Actual p2:", sorted(observation, reverse=True)[1] / n)
assert final_result >= sorted(observation, reverse=True)[1] / n

end_time = time()
time_taken = end_time - start_time
if time_taken >= 60:
    minutes_taken, seconds_taken = seconds_to_minutes(time_taken)
    print(f"Time taken: {minutes_taken:.0f} minutes and {seconds_taken:.6f} seconds")
else:
    print(f"Time taken: {time_taken:.6f} seconds")
