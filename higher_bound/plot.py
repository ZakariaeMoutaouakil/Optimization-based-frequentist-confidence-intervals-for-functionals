import matplotlib.pyplot as plt
from numpy import linspace
from scipy.stats import norm

from higher_bound.get_quantiles import get_quantiles as get_quantiles_p2
from lower_bound.generate_multiple_indices import generate_multiple_indices
from lower_bound.get_quantiles import get_quantiles as get_quantiles_p1
from lower_bound.max_first_coordinate import max_first_coordinate

# Initial parameters
alpha = 0.001
step = 0.01
x = (3, 7, 30)
n = sum(x)
m = len(x)

# Store results
k_values = linspace(0.7, 0.9, 3)
radius1_values = []
radius2_values = []

for k in k_values:
    beta = k * alpha
    print("beta:", beta)
    indices_p1 = generate_multiple_indices(maximum=n, dimension=m, n=n)
    quantiles_p1 = get_quantiles_p1(alpha=beta, n=n, m=m, step=step, indices=indices_p1)
    a = max_first_coordinate(quantiles=quantiles_p1, maximum=max(x))

    y = x[:len(x) - 1]
    n_y = sum(y)
    m_y = len(y)
    gamma = (1 - k) * alpha / (1 - k * alpha)
    indices_p2 = generate_multiple_indices(maximum=n_y, dimension=m_y, n=n_y)
    quantiles_p2 = get_quantiles_p2(alpha=gamma, n=n_y, m=m_y, step=step, indices=indices_p2)
    q = max_first_coordinate(quantiles=quantiles_p2, maximum=max(y))

    p2 = q * (1 - a)
    radius1 = 0.5 * (norm.ppf(a) - norm.ppf(p2))
    radius1_values.append(radius1)

    quantiles_p1 = get_quantiles_p1(alpha=alpha, n=n, m=m, step=step, indices=indices_p1)
    a = max_first_coordinate(quantiles=quantiles_p1, maximum=max(x))
    radius2 = norm.ppf(a)
    radius2_values.append(radius2)

# Plotting the results
plt.figure(figsize=(12, 6))
plt.plot(k_values, radius1_values, label='Radius 1', marker='o')
plt.plot(k_values, radius2_values, label='Radius 2', marker='x')
plt.xlabel('k')
plt.ylabel('Radius')
plt.title('Variation of Radius 1 and Radius 2 with k')
plt.legend()
plt.grid(True)
plt.show()
