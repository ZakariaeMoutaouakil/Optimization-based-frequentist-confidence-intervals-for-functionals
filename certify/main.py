import ast
import re
from typing import List

import pandas as pd

from certify.get_higher_bound import get_higher_bound
from certify.smallest_subset import smallest_subset
from lower_bound.final_result import final_result
from utils.unique_vector_indices import unique_vector_indices, get_unique_vectors


# Function to preprocess the counts column
def add_commas_to_counts(line: str) -> str:
    return re.sub(r'\[\s*(.*?)\s*\]', lambda m: '[' + ', '.join(m.group(1).split()) + ']', line)


# Path to your TSV file
file_path = '../certification_output.tsv'

# Read and preprocess the file
with open(file_path, 'r') as file:
    lines = file.readlines()

# Apply preprocessing to each line
preprocessed_lines = [add_commas_to_counts(line) for line in lines]

# Write the preprocessed lines to a new file (optional, or you can use StringIO to avoid creating a new file)
preprocessed_file_path = 'preprocessed_data.tsv'
with open(preprocessed_file_path, 'w') as file:
    file.writelines(preprocessed_lines)

# Define the data types for each column
dtype_dict = {
    'idx': int,
    'label': int,
    'predict': int,
    'radius': float,
    'correct': int,
    'time': str
}

# Read the preprocessed TSV data into a DataFrame with specified dtypes
df = pd.read_csv(preprocessed_file_path, sep='\t', dtype=dtype_dict, converters={'counts': ast.literal_eval})

# Display the DataFrame with correct types
print(df)
print(df.dtypes)

raw_vectors: List[List[int]] = df['counts'].to_list()
for i in range(len(raw_vectors)):
    print(raw_vectors[i])

vectors = get_unique_vectors(vectors=raw_vectors)
vectors = [sorted(vector) for vector in vectors]
indices = unique_vector_indices(raw_vectors=raw_vectors, unique_vectors=vectors)

# print(vectors)
# print(indices)
num_partitions = 3
for vec in vectors:
    print("vec:", vec)
    observation = [vec[len(vec) - 1]]
    rest = vec[:len(vec) - 1]
    # print("rest:", rest)
    i = smallest_subset(vector=rest, num_partitions=num_partitions - 1, debug=False)
    # print("i:", i)
    # print(i == len(rest) - num_partitions + 1)
    second_class = vec[:i]
    observation.append(sum(second_class))
    # print("second_class:", second_class)
    third_classes = vec[i:len(vec) - 1]
    # print("third_classes:", third_classes)
    observation.append(sum(third_classes))
    observation = sorted(observation)
    print("observation:", observation)
    # partitions_ = partition_iterator(num_partitions=num_partitions-1, third_classes)
    p1 = final_result(alpha=0.05 / 2, x=observation)
    print("p1:", p1)
    try:
        p2 = get_higher_bound(observation=observation, threshold=p1, alpha=0.05 / 2)
    except Exception as e:
        p2 = 1 - p1
    print("p2:", p2)
# for i in range(len(df)):
#     print(type(df.iloc[i]['counts'][0]))
