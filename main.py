import sys
import os

# Define the parent directory
parent_dir = '/home/pc/Projects/Geometry of the Minimum Volume Confidence Sets'

# Add the parent directory to sys.path
sys.path.append(parent_dir)

# Walk through the directory and add each subdirectory to sys.path
for root, dirs, files in os.walk(parent_dir):
    for dir in dirs:
        sys.path.append(os.path.join(root, dir))
        
from factorial import factorial_list

# Now you can call your function
print(factorial_list(n=5))

sys.path.append('/home/pc/Projects/Geometry of the Minimum Volume Confidence Sets/utils/')

from discrete_simplex import discrete_simplex

print(discrete_simplex(k=3, n=4))

sys.path.append('/home/pc/Projects/Geometry of the Minimum Volume Confidence Sets/algorithm/')

from final_result import final_result

print(final_result)