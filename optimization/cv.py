import itertools

import cvxpy as cp

# Define parameters
# n = 5
m = 3
x = [0, 2, 3]
s_m = list(itertools.permutations(range(m)))
print("s_m=", s_m)

# Define variables
variables = cp.Variable(m, pos=True)

# Define the objective function
objective_fn = sum(cp.prod([variables[j] ** (-x[i]) for i, j in enumerate(perm)]) for perm in s_m)

# Define constraints
constraints = [cp.sum(variables) <= 1] + [variables[i] >= variables[i + 1] for i in range(m - 1)]

# Define and solve the problem
problem = cp.Problem(cp.Minimize(objective_fn), constraints)
problem.solve(gp=True)

# Print the optimal value
print("Optimal value: ", 1 / problem.value)
print("Optimal variables: ", variables.value)
print("Sum of variables: ", cp.sum(variables).value)

threshold = 0.8

# Define constraints
constraints += [variables[0]>=threshold]

# Define and solve the problem
problem = cp.Problem(cp.Minimize(objective_fn), constraints)
problem.solve(gp=True)

# Print the optimal value
print("Optimal value: ", 1 / problem.value)
print("Optimal variables: ", variables.value)
print("Sum of variables: ", cp.sum(variables).value)
