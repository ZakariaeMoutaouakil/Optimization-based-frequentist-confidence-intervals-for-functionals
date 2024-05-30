import matplotlib.pyplot as plt

# Data
n1 = [25, 30, 35]
final_result1 = [0.16, 0.13, 0.14]

n2 = [25, 30, 35]
final_result2 = [0.0970873786407767, 0.0970873786407767, 0.0970873786407767]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(n1, final_result1, marker='o', linestyle='-', color='b', label='MVC')
plt.plot(n2, final_result2, marker='x', linestyle='--', color='r', label='LLR Optimization')

# Adding titles and labels
plt.title('Comparison of Lower bounds')
plt.xlabel('n')
plt.ylabel('Lower bound of p2')
plt.legend()

# Display the plot
plt.grid(True)
plt.show()
