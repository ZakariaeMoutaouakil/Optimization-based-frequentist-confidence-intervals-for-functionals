import ast
import re
from typing import List

import pandas as pd
from scipy.stats import norm

from certify.smallest_subset import smallest_subset
from lower_bound.final_result import final_result


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
num_partitions = 3
sigma = 0.12
alpha = 0.05
for i in range(len(df)):
    print("old:", df.iloc[i])
    counts: List[int] = df.iloc[i]['counts']
    observation = [counts[len(counts) - 1]]
    rest = counts[:len(counts) - 1]
    i = smallest_subset(vector=rest, num_partitions=num_partitions - 1, debug=False)
    second_class = counts[:i]
    observation.append(sum(second_class))
    third_classes = counts[i:len(counts) - 1]
    observation.append(sum(third_classes))
    observation = sorted(observation)
    print("observation:", observation)
    p1 = final_result(alpha=alpha, x=observation)
    print("p1:", p1)
    if p1 >= 0.5:
        df.loc[df.index[i], 'radius'] = sigma * norm.ppf(p1)
        prediction: int = df.iloc[i]['prediction']
        df.loc[df.index[i], 'predict'] = prediction
        df.loc[df.index[i], 'correct'] = int(prediction == df.iloc[i]['label'])
    else:
        df.loc[df.index[i], 'radius'] = 0.
        prediction = -1
        df.loc[df.index[i], 'predict'] = prediction
        df.loc[df.index[i], 'correct'] = 0
    print("new:", df.iloc[i])

# Remove the last three columns
df_modified = df.iloc[:, :-3]  # This slices out all rows and all columns except the last three

# Save to TSV file
df_modified.to_csv('modified_data.tsv', sep='\t',
                   index=False)  # Set index=False if you don't want to save the index as a separate column
# raw_vectors: List[List[int]] = df['counts'].to_list()
# for i in range(len(raw_vectors)):
#     print(raw_vectors[i])
#
# vectors = get_unique_vectors(vectors=raw_vectors)
# vectors = [sorted(vector) for vector in vectors]
# indices = unique_vector_indices(raw_vectors=raw_vectors, unique_vectors=vectors)
#
# print("length of vectors:", len(vectors))
# p1s: List[float] = []
# num_partitions = 3
# for vec in vectors:
#     print("vec:", vec)
#     observation = [vec[len(vec) - 1]]
#     rest = vec[:len(vec) - 1]
#     # print("rest:", rest)
#     i = smallest_subset(vector=rest, num_partitions=num_partitions - 1, debug=False)
#     # print("i:", i)
#     # print(i == len(rest) - num_partitions + 1)
#     second_class = vec[:i]
#     observation.append(sum(second_class))
#     # print("second_class:", second_class)
#     third_classes = vec[i:len(vec) - 1]
#     # print("third_classes:", third_classes)
#     observation.append(sum(third_classes))
#     observation = sorted(observation)
#     print("observation:", observation)
#     # partitions_ = partition_iterator(num_partitions=num_partitions-1, third_classes)
#     p1 = final_result(alpha=0.05, x=observation)
#     print("p1:", p1)
#     p1s.append(p1)
# for i in range(len(df)):
#     print(type(df.iloc[i]['counts'][0]))
